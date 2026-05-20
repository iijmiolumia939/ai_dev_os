import * as fs from 'fs/promises';
import * as path from 'path';
import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {workspaceRoot} from '../persistence/localPersistence';

export interface ConsumerRolloutSnapshot {
  rolloutReady: boolean;
  migrationFriction: 'LOW' | 'MEDIUM' | 'HIGH' | 'BLOCKED';
  governanceReadiness: 'READY' | 'TRAINING_REQUIRED';
  rollbackReady: boolean;
  boundedRolloutConfirmed: boolean;
  frictionCategories: string[];
  rollbackRisk: 'LOW' | 'MEDIUM' | 'HIGH';
  summaryOnly: true;
  dryRunOnly: true;
  automaticMigrationUsed: false;
}

export class ConsumerRolloutMonitor {
  constructor(private readonly root = workspaceRoot()) {}

  async evaluate(): Promise<ConsumerRolloutSnapshot> {
    const consumer = path.resolve(this.root, '..', 'AITuber');
    const consumerExists = await this.exists(consumer);
    const gitignore = await this.readText(path.join(consumer, '.gitignore'));
    const docs = await this.readDocs(path.join(consumer, 'docs'));
    const packageJson = await this.readJson(path.join(this.root, 'extensions', 'ai-dev-os-vscode', 'package.json'));
    const commands = new Set<string>((packageJson.contributes?.commands ?? []).map((item: {command?: string}) => item.command ?? ''));
    const frictionCategories = [
      ...(consumerExists ? [] : ['consumer repository missing']),
      ...((await this.exists(path.join(consumer, '.ai-dev-os'))) ? [] : ['missing session lifecycle setup']),
      ...(gitignore.includes('.ai-dev-os/') ? [] : ['missing local persistence ignore rule']),
      ...(commands.has('aiDevOs.showGovernancePresence') ? [] : ['missing governance presence command']),
      ...(docs.includes('governance') || docs.includes('rollout') ? [] : ['stale rollout docs']),
    ];
    const rollbackReady = gitignore.includes('.ai-dev-os/') && commands.has('aiDevOs.resetLocalSessionState');
    const governanceReady = commands.has('aiDevOs.showGovernanceDashboard') && commands.has('aiDevOs.showStaleSessionWarning');
    const migrationFriction = frictionCategories.length >= 4 ? 'HIGH' : frictionCategories.length >= 2 ? 'MEDIUM' : 'LOW';
    return {
      rolloutReady: consumerExists && governanceReady && rollbackReady && migrationFriction !== 'HIGH',
      migrationFriction,
      governanceReadiness: governanceReady ? 'READY' : 'TRAINING_REQUIRED',
      rollbackReady,
      boundedRolloutConfirmed: true,
      frictionCategories,
      rollbackRisk: rollbackReady ? 'LOW' : 'MEDIUM',
      summaryOnly: true,
      dryRunOnly: true,
      automaticMigrationUsed: false,
    };
  }

  private async exists(filePath: string): Promise<boolean> {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  private async readText(filePath: string): Promise<string> {
    try {
      return await fs.readFile(filePath, 'utf8');
    } catch {
      return '';
    }
  }

  private async readJson(filePath: string): Promise<Record<string, any>> {
    try {
      return JSON.parse(await fs.readFile(filePath, 'utf8')) as Record<string, any>;
    } catch {
      return {};
    }
  }

  private async readDocs(dirPath: string): Promise<string> {
    try {
      const entries = await fs.readdir(dirPath, {withFileTypes: true});
      const texts = await Promise.all(
        entries
          .filter((entry) => entry.isFile() && entry.name.endsWith('.md'))
          .map((entry) => this.readText(path.join(dirPath, entry.name))),
      );
      return texts.join('\n').toLowerCase();
    } catch {
      return '';
    }
  }
}

export class RolloutTreeProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.changed.event;

  constructor(
    private readonly monitor: ConsumerRolloutMonitor,
    private readonly kind: 'rollout' | 'friction' | 'governance' | 'rollback',
  ) {}

  refresh(): void {
    this.changed.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  async getChildren(): Promise<vscode.TreeItem[]> {
    const snapshot = await this.monitor.evaluate();
    if (this.kind === 'friction') {
      return [
        new vscode.TreeItem(`Friction: ${snapshot.migrationFriction}`),
        ...snapshot.frictionCategories.slice(0, 5).map((item) => new vscode.TreeItem(item)),
      ];
    }
    if (this.kind === 'governance') {
      return [
        new vscode.TreeItem(`Governance: ${snapshot.governanceReadiness}`),
        new vscode.TreeItem(`Bounded rollout: ${snapshot.boundedRolloutConfirmed}`),
      ];
    }
    if (this.kind === 'rollback') {
      return [
        new vscode.TreeItem(`Rollback ready: ${snapshot.rollbackReady}`),
        new vscode.TreeItem(`Rollback risk: ${snapshot.rollbackRisk}`),
        new vscode.TreeItem('Dry run only: true'),
      ];
    }
    return [
      new vscode.TreeItem(`Rollout ready: ${snapshot.rolloutReady}`),
      new vscode.TreeItem(`Friction: ${snapshot.migrationFriction}`),
      new vscode.TreeItem(`Rollback ready: ${snapshot.rollbackReady}`),
    ];
  }
}

export function registerConsumerRolloutCommands(
  monitor: ConsumerRolloutMonitor,
  notifications: RateLimitedNotifications,
  providers: RolloutTreeProvider[],
): vscode.Disposable[] {
  const showRollout = vscode.commands.registerCommand('aiDevOs.showRolloutReadiness', async () => {
    const snapshot = await monitor.evaluate();
    await vscode.window.showInformationMessage(JSON.stringify(snapshot, undefined, 2));
  });
  const showFriction = vscode.commands.registerCommand('aiDevOs.showMigrationFriction', async () => {
    const snapshot = await monitor.evaluate();
    await vscode.window.showInformationMessage(JSON.stringify({level: snapshot.migrationFriction, categories: snapshot.frictionCategories}, undefined, 2));
  });
  const showGovernance = vscode.commands.registerCommand('aiDevOs.showGovernanceReadiness', async () => {
    const snapshot = await monitor.evaluate();
    await vscode.window.showInformationMessage(`AI_DEV_OS governance readiness: ${snapshot.governanceReadiness}`);
  });
  const showRollback = vscode.commands.registerCommand('aiDevOs.showRollbackRehearsal', async () => {
    const snapshot = await monitor.evaluate();
    await vscode.window.showInformationMessage(`AI_DEV_OS rollback rehearsal: ${snapshot.rollbackRisk}`);
  });
  const refresh = vscode.commands.registerCommand('aiDevOs.refreshRolloutRehearsal', async () => {
    providers.forEach((provider) => provider.refresh());
    const snapshot = await monitor.evaluate();
    if (snapshot.migrationFriction === 'HIGH' || snapshot.migrationFriction === 'BLOCKED') {
      await notifications.warn('rollout-migration-friction', 'AI_DEV_OS consumer rollout rehearsal found migration friction.');
    }
  });
  return [showRollout, showFriction, showGovernance, showRollback, refresh];
}
