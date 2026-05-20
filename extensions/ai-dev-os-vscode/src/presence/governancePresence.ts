import * as fs from 'fs/promises';
import * as os from 'os';
import * as path from 'path';
import * as vscode from 'vscode';
import {GovernanceHealthState} from '../governance/health';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {PersistenceState, workspaceRoot} from '../persistence/localPersistence';
import {RuntimeGraphState} from '../runtimeGraph/runtimeGraph';

export interface GovernancePresenceState {
  extensionActive: boolean;
  runtimeAuditActive: boolean;
  governanceCoreActive: boolean;
  sessionBoundaryActive: boolean;
  persistenceActive: boolean;
  runtimeGraphActive: boolean;
  currentSessionGeneration: number;
  rolloverPending: boolean;
  staleSessionDetected: boolean;
  boundedPresenceConfirmed: boolean;
  summaryOnly: true;
}

export interface ExtensionVersionState {
  repoVersion: string;
  installedVersion: string;
  versionMatch: boolean;
  staleInstall: boolean;
  missingReinstall: boolean;
  duplicateInstall: boolean;
  staleExtensionDetected: boolean;
  reinstallRecommended: boolean;
  duplicateInstallDetected: boolean;
  installedPaths: string[];
  summaryOnly: true;
}

export interface RuntimeHeartbeatState {
  lastRuntimeAudit: number;
  lastContinuityExport: number;
  lastPersistenceRestore: number;
  lastRolloverEvaluation: number;
  lastGovernanceTrendUpdate: number;
  heartbeatActive: boolean;
  heartbeatAge: number;
  staleHeartbeat: boolean;
  heartbeatSummary: 'ACTIVE' | 'STALE' | 'MISSING';
  summaryOnly: true;
}

export interface GovernanceStatusProjectionState {
  compactStatus: string;
  severity: 'OK' | 'NOTICE' | 'WARNING';
  pressureProjection: string;
  rolloverProjection: string;
  staleProjection: string;
  notificationRequired: boolean;
  summaryOnly: true;
  humanConfirmedOnly: true;
}

export interface StaleExtensionState {
  staleExtensionDetected: boolean;
  missingCapabilities: string[];
  reinstallRequired: boolean;
  visibilityDegraded: boolean;
  staleActivation: boolean;
  staleManifest: boolean;
  summaryOnly: true;
}

export interface GovernancePresenceSnapshot {
  presence: GovernancePresenceState;
  version: ExtensionVersionState;
  heartbeat: RuntimeHeartbeatState;
  status: GovernanceStatusProjectionState;
  staleExtension: StaleExtensionState;
  noBackgroundMutation: true;
  localOnly: true;
}

const requiredCommands = [
  'aiDevOs.showGovernancePresence',
  'aiDevOs.showRuntimeHeartbeat',
  'aiDevOs.checkExtensionVersion',
  'aiDevOs.showPresenceStatus',
  'aiDevOs.showStaleExtensionWarning',
  'aiDevOs.refreshGovernancePresence',
  'aiDevOs.showGovernanceCore',
  'aiDevOs.showRuntimeGraph',
  'aiDevOs.showRuntimeOverlap',
  'aiDevOs.showSimplificationRecommendations',
];

const requiredViews = [
  'aiDevOsSessionBoundary',
  'aiDevOsGovernanceDashboard',
  'aiDevOsGovernanceTrends',
  'aiDevOsRuntimeGraph',
  'aiDevOsRuntimeOverlap',
  'aiDevOsSharedPrimitives',
  'aiDevOsBoundedRetention',
];

export class GovernancePresenceMonitor {
  constructor(private readonly context: vscode.ExtensionContext, private readonly root = workspaceRoot()) {}

  async evaluate(
    restored: PersistenceState,
    health: GovernanceHealthState,
    runtimeGraph: RuntimeGraphState,
  ): Promise<GovernancePresenceSnapshot> {
    const version = await this.detectVersion();
    const staleExtension = await this.detectStaleExtension(version);
    const presence = await this.buildPresence(restored, runtimeGraph);
    const heartbeat = await this.buildHeartbeat();
    const status = this.projectStatus(presence, health, staleExtension);
    return {
      presence,
      version,
      heartbeat,
      status,
      staleExtension,
      noBackgroundMutation: true,
      localOnly: true,
    };
  }

  async detectVersion(): Promise<ExtensionVersionState> {
    const repoPackage = await this.readJson(path.join(this.root, 'extensions', 'ai-dev-os-vscode', 'package.json'));
    const repoVersion = String(repoPackage.version ?? this.context.extension.packageJSON.version ?? '');
    const installedVersion = String(this.context.extension.packageJSON.version ?? '');
    const installedPaths = await this.findInstalledPaths();
    const duplicateInstall = installedPaths.length > 1;
    const versionMatch = Boolean(repoVersion && installedVersion && repoVersion === installedVersion);
    const staleInstall = Boolean(repoVersion && installedVersion && repoVersion !== installedVersion);
    const missingReinstall = Boolean(repoVersion && !installedVersion);
    return {
      repoVersion,
      installedVersion,
      versionMatch,
      staleInstall,
      missingReinstall,
      duplicateInstall,
      staleExtensionDetected: staleInstall || missingReinstall || duplicateInstall,
      reinstallRecommended: staleInstall || missingReinstall || duplicateInstall,
      duplicateInstallDetected: duplicateInstall,
      installedPaths,
      summaryOnly: true,
    };
  }

  private async buildPresence(
    restored: PersistenceState,
    runtimeGraph: RuntimeGraphState,
  ): Promise<GovernancePresenceState> {
    const storageFiles = await Promise.all([
      this.exists(path.join(this.root, '.ai-dev-os', 'session-boundary.json')),
      this.exists(path.join(this.root, '.ai-dev-os', 'rollover-state.json')),
      this.exists(path.join(this.root, '.ai-dev-os', 'continuity-index.json')),
    ]);
    const persistenceActive = storageFiles.every(Boolean);
    const staleState = restored.stale_warning_state;
    const rolloverState = restored.rollover_state;
    const staleSessionDetected = Boolean(staleState.stale_session_detected);
    return {
      extensionActive: true,
      runtimeAuditActive: true,
      governanceCoreActive: true,
      sessionBoundaryActive: persistenceActive,
      persistenceActive,
      runtimeGraphActive: runtimeGraph.summaryOnly,
      currentSessionGeneration: restored.current_session_generation,
      rolloverPending: Boolean(rolloverState.rollover_pending),
      staleSessionDetected,
      boundedPresenceConfirmed: restored.summary_only && restored.bounded && !this.hasRawTranscript(restored),
      summaryOnly: true,
    };
  }

  private async buildHeartbeat(): Promise<RuntimeHeartbeatState> {
    const now = Date.now();
    const stamps = await Promise.all([
      this.mtime(path.join(this.root, '.ai-dev-os', 'session-boundary.json')),
      this.mtime(path.join(this.root, '.ai-dev-os', 'continuity-index.json')),
      this.mtime(path.join(this.root, '.ai-dev-os', 'session-boundary.json')),
      this.mtime(path.join(this.root, '.ai-dev-os', 'rollover-state.json')),
      this.mtime(path.join(this.root, 'extensions', 'ai-dev-os-vscode', 'src', 'governance', 'trends.ts')),
    ]);
    const known = stamps.filter((stamp) => stamp > 0);
    const latest = known.length > 0 ? Math.max(...known) : 0;
    const age = latest > 0 ? now - latest : Number.POSITIVE_INFINITY;
    const staleHeartbeat = latest === 0 || age > 86_400_000;
    return {
      lastRuntimeAudit: stamps[0],
      lastContinuityExport: stamps[1],
      lastPersistenceRestore: stamps[2],
      lastRolloverEvaluation: stamps[3],
      lastGovernanceTrendUpdate: stamps[4],
      heartbeatActive: latest > 0 && !staleHeartbeat,
      heartbeatAge: age,
      staleHeartbeat,
      heartbeatSummary: latest === 0 ? 'MISSING' : staleHeartbeat ? 'STALE' : 'ACTIVE',
      summaryOnly: true,
    };
  }

  private projectStatus(
    presence: GovernancePresenceState,
    health: GovernanceHealthState,
    staleExtension: StaleExtensionState,
  ): GovernanceStatusProjectionState {
    const pressure = health.pressure.toUpperCase();
    const rollover = presence.rolloverPending ? 'ROLLOVER_PENDING' : 'ROLLOVER_OK';
    const stale = presence.staleSessionDetected || staleExtension.staleExtensionDetected ? 'STALE' : 'FRESH';
    const severity = stale === 'STALE' || pressure === 'HIGH' || pressure === 'CRITICAL' ? 'WARNING' : presence.rolloverPending ? 'NOTICE' : 'OK';
    return {
      compactStatus: `AI_DEV_OS ACTIVE GEN:${presence.currentSessionGeneration} ${pressure}_PRESSURE ${rollover}`,
      severity,
      pressureProjection: `${pressure}_PRESSURE`,
      rolloverProjection: rollover,
      staleProjection: stale,
      notificationRequired: severity === 'WARNING',
      summaryOnly: true,
      humanConfirmedOnly: true,
    };
  }

  private async detectStaleExtension(version: ExtensionVersionState): Promise<StaleExtensionState> {
    const packageJson = this.context.extension.packageJSON;
    const commands = new Set<string>((packageJson.contributes?.commands ?? []).map((item: {command?: string}) => item.command ?? ''));
    const views = new Set<string>((packageJson.contributes?.views?.explorer ?? []).map((item: {id?: string}) => item.id ?? ''));
    const activation = new Set<string>(packageJson.activationEvents ?? []);
    const missingCommands = requiredCommands.filter((command) => !commands.has(command)).map((command) => `command:${command}`);
    const missingViews = requiredViews.filter((view) => !views.has(view)).map((view) => `view:${view}`);
    const missingActivation = requiredCommands
      .filter((command) => !activation.has(`onCommand:${command}`))
      .map((command) => `activation:onCommand:${command}`);
    const missingCapabilities = [...missingCommands, ...missingViews, ...missingActivation];
    const staleManifest = missingCapabilities.length > 0;
    const staleExtensionDetected = version.staleExtensionDetected || staleManifest;
    return {
      staleExtensionDetected,
      missingCapabilities,
      reinstallRequired: staleExtensionDetected,
      visibilityDegraded: staleExtensionDetected,
      staleActivation: missingActivation.length > 0,
      staleManifest,
      summaryOnly: true,
    };
  }

  private async findInstalledPaths(): Promise<string[]> {
    const extensionId = `${this.context.extension.packageJSON.publisher}.${this.context.extension.packageJSON.name}`;
    const extensionDir = path.join(os.homedir(), '.vscode', 'extensions');
    try {
      const entries = await fs.readdir(extensionDir, {withFileTypes: true});
      return entries
        .filter((entry) => entry.isDirectory() && entry.name.startsWith(extensionId))
        .map((entry) => path.join(extensionDir, entry.name))
        .sort();
    } catch {
      return [];
    }
  }

  private async exists(filePath: string): Promise<boolean> {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  private async mtime(filePath: string): Promise<number> {
    try {
      return (await fs.stat(filePath)).mtimeMs;
    } catch {
      return 0;
    }
  }

  private async readJson(filePath: string): Promise<Record<string, unknown>> {
    try {
      return JSON.parse(await fs.readFile(filePath, 'utf8')) as Record<string, unknown>;
    } catch {
      return {};
    }
  }

  private hasRawTranscript(value: unknown): boolean {
    if (Array.isArray(value)) {
      return value.some((item) => this.hasRawTranscript(item));
    }
    if (value !== null && typeof value === 'object') {
      return Object.entries(value).some(([key, child]) => key === 'raw_transcript' || this.hasRawTranscript(child));
    }
    return false;
  }
}

export class GovernancePresenceStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 92);

  constructor(private readonly monitor: GovernancePresenceMonitor) {
    this.item.command = 'aiDevOs.showPresenceStatus';
  }

  async refresh(
    restored: PersistenceState,
    health: GovernanceHealthState,
    runtimeGraph: RuntimeGraphState,
  ): Promise<GovernancePresenceSnapshot> {
    const snapshot = await this.monitor.evaluate(restored, health, runtimeGraph);
    this.item.text = snapshot.status.compactStatus;
    this.item.tooltip = `Presence ${snapshot.status.severity}; heartbeat ${snapshot.heartbeat.heartbeatSummary}; version ${snapshot.version.installedVersion || 'unknown'}`;
    this.item.show();
    return snapshot;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RuntimeHeartbeatStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 91);

  constructor(private readonly monitor: GovernancePresenceMonitor) {
    this.item.command = 'aiDevOs.showRuntimeHeartbeat';
  }

  async refresh(
    restored: PersistenceState,
    health: GovernanceHealthState,
    runtimeGraph: RuntimeGraphState,
  ): Promise<RuntimeHeartbeatState> {
    const snapshot = await this.monitor.evaluate(restored, health, runtimeGraph);
    this.item.text = `AI_DEV_OS HEARTBEAT ${snapshot.heartbeat.heartbeatSummary}`;
    this.item.tooltip = `Last local runtime signal age ${Math.round(snapshot.heartbeat.heartbeatAge / 1000)}s`;
    this.item.show();
    return snapshot.heartbeat;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export function registerGovernancePresenceCommands(
  monitor: GovernancePresenceMonitor,
  presenceStatus: GovernancePresenceStatusBar,
  heartbeatStatus: RuntimeHeartbeatStatusBar,
  notifications: RateLimitedNotifications,
  restored: PersistenceState,
  health: GovernanceHealthState,
  runtimeGraph: RuntimeGraphState,
): vscode.Disposable[] {
  const showGovernancePresence = vscode.commands.registerCommand('aiDevOs.showGovernancePresence', async () => {
    const snapshot = await monitor.evaluate(restored, health, runtimeGraph);
    await vscode.window.showInformationMessage(JSON.stringify(snapshot.presence, undefined, 2));
  });
  const showRuntimeHeartbeat = vscode.commands.registerCommand('aiDevOs.showRuntimeHeartbeat', async () => {
    const snapshot = await monitor.evaluate(restored, health, runtimeGraph);
    await vscode.window.showInformationMessage(JSON.stringify(snapshot.heartbeat, undefined, 2));
  });
  const checkExtensionVersion = vscode.commands.registerCommand('aiDevOs.checkExtensionVersion', async () => {
    const snapshot = await monitor.evaluate(restored, health, runtimeGraph);
    await vscode.window.showInformationMessage(JSON.stringify(snapshot.version, undefined, 2));
  });
  const showPresenceStatus = vscode.commands.registerCommand('aiDevOs.showPresenceStatus', async () => {
    const snapshot = await monitor.evaluate(restored, health, runtimeGraph);
    await vscode.window.showInformationMessage(snapshot.status.compactStatus);
  });
  const showStaleExtensionWarning = vscode.commands.registerCommand('aiDevOs.showStaleExtensionWarning', async () => {
    const snapshot = await monitor.evaluate(restored, health, runtimeGraph);
    if (snapshot.staleExtension.staleExtensionDetected) {
      await notifications.warn('presence-stale-extension', 'AI_DEV_OS installed extension is stale or missing visibility capabilities.');
      return;
    }
    await notifications.info('presence-extension-current', 'AI_DEV_OS extension visibility capabilities are current.');
  });
  const refreshGovernancePresence = vscode.commands.registerCommand('aiDevOs.refreshGovernancePresence', async () => {
    await presenceStatus.refresh(restored, health, runtimeGraph);
    await heartbeatStatus.refresh(restored, health, runtimeGraph);
  });
  return [
    showGovernancePresence,
    showRuntimeHeartbeat,
    checkExtensionVersion,
    showPresenceStatus,
    showStaleExtensionWarning,
    refreshGovernancePresence,
  ];
}
