import * as vscode from 'vscode';
import {registerGovernanceCommands} from './commands/governanceCommands';
import {registerGovernanceHealthCommands} from './commands/governanceHealthCommands';
import {registerGovernanceTrendCommands} from './commands/governanceTrendCommands';
import {registerPersistenceCommands} from './commands/persistenceCommands';
import {registerSessionCommands} from './commands/sessionCommands';
import {GovernanceHealthMonitor, GovernanceStatusBar} from './governance/health';
import {GovernanceTrendMonitor, GovernanceTrendStatusBar} from './governance/trends';
import {RateLimitedNotifications} from './notifications/rateLimitedNotifications';
import {PersistenceGovernance} from './persistence/governance';
import {LocalPersistenceStore} from './persistence/localPersistence';
import {BoundaryStateStore} from './state/boundaryState';
import {GovernanceDashboardViewProvider} from './views/governanceDashboardView';
import {GovernanceTrendViewProvider} from './views/governanceTrendView';
import {SessionBoundaryViewProvider} from './views/sessionBoundaryView';

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  const store = new BoundaryStateStore(context);
  const notifications = new RateLimitedNotifications(vscode.window);
  const view = new SessionBoundaryViewProvider(store);
  const persistence = new LocalPersistenceStore();
  const governance = new PersistenceGovernance(persistence);
  const governanceHealth = new GovernanceHealthMonitor(persistence, governance);
  const governanceStatus = new GovernanceStatusBar(governanceHealth);
  const governanceView = new GovernanceDashboardViewProvider(governanceHealth);
  const governanceTrend = new GovernanceTrendMonitor(governanceHealth);
  const governanceTrendStatus = new GovernanceTrendStatusBar(governanceTrend);
  const governanceTrendView = new GovernanceTrendViewProvider(governanceTrend);
  await persistence.ensure();
  const restored = await persistence.read();
  const governanceState = await governance.validate();
  const healthState = await governanceStatus.refresh();
  const trendState = await governanceTrendStatus.refresh();
  await store.update(persistence.toBoundaryState(restored));
  if (restored.rollover_state.rollover_pending || restored.stale_warning_state.stale_session_detected) {
    await notifications.warn(
      'startup-persistence-warning',
      'AI_DEV_OS restored a pending rollover or stale session warning from local persistence.',
    );
  } else if (Object.keys(restored.last_continuity_bundle).length > 0) {
    await notifications.info(
      'startup-continuity-restored',
      'AI_DEV_OS compact continuity is available from local persistence.',
    );
  }
  if (governanceState.migrationRequired || governanceState.quarantineDetected) {
    await notifications.warn(
      'startup-schema-governance-warning',
      'AI_DEV_OS local persistence schema needs migration or quarantine review.',
    );
  } else if (governanceState.checkpointRotationRequired || governanceState.compactRecommendation) {
    await notifications.warn(
      'startup-retention-governance-warning',
      'AI_DEV_OS local persistence retention pressure requires compact cleanup.',
    );
  }
  if (healthState.level === 'CRITICAL' || healthState.level === 'HIGH_PRESSURE') {
    await notifications.warn(
      'startup-governance-health-warning',
      `AI_DEV_OS governance health is ${healthState.level}. Review the governance dashboard.`,
    );
  }
  if (trendState.trendLevel === 'DEGRADING' || trendState.trendLevel === 'OSCILLATING') {
    await notifications.warn(
      'startup-governance-trend-warning',
      `AI_DEV_OS governance trend is ${trendState.trendLevel}. Review dashboard delta.`,
    );
  }
  context.subscriptions.push(...registerSessionCommands(context, store, notifications, view));
  context.subscriptions.push(
    ...registerPersistenceCommands(store, persistence, notifications, view),
  );
  context.subscriptions.push(
    ...registerGovernanceCommands(persistence, governance, notifications, view),
  );
  context.subscriptions.push(
    vscode.window.registerTreeDataProvider('aiDevOsGovernanceDashboard', governanceView),
    vscode.window.registerTreeDataProvider('aiDevOsGovernanceTrends', governanceTrendView),
    governanceStatus,
    governanceTrendStatus,
    ...registerGovernanceHealthCommands(
      governanceHealth,
      governanceStatus,
      notifications,
      governanceView,
    ),
    ...registerGovernanceTrendCommands(
      governanceTrend,
      governanceTrendStatus,
      notifications,
      governanceTrendView,
    ),
  );
}

export function deactivate(): void {
  return;
}
