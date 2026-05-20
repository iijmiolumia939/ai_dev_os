import * as vscode from 'vscode';
import {registerGovernanceCoreCommands} from './commands/governanceCoreCommands';
import {registerGovernanceCommands} from './commands/governanceCommands';
import {registerGovernanceHealthCommands} from './commands/governanceHealthCommands';
import {registerGovernanceTrendCommands} from './commands/governanceTrendCommands';
import {registerOutputCompressionCommands} from './commands/outputCompressionCommands';
import {registerPersistenceCommands} from './commands/persistenceCommands';
import {registerReasoningRoutingCommands} from './commands/reasoningRoutingCommands';
import {registerRuntimeGraphCommands} from './commands/runtimeGraphCommands';
import {registerRuntimeSimplificationCommands} from './commands/runtimeSimplificationCommands';
import {registerSessionCommands} from './commands/sessionCommands';
import {GovernanceHealthMonitor, GovernanceStatusBar} from './governance/health';
import {GovernanceTrendMonitor, GovernanceTrendStatusBar} from './governance/trends';
import {GovernanceCoreMonitor, GovernanceCoreStatusBar} from './governanceCore/governanceCore';
import {RateLimitedNotifications} from './notifications/rateLimitedNotifications';
import {CompactReportingStatusBar, OutputCompressionMonitor} from './outputCompression/outputCompression';
import {PersistenceGovernance} from './persistence/governance';
import {LocalPersistenceStore} from './persistence/localPersistence';
import {
  GovernancePresenceMonitor,
  GovernancePresenceStatusBar,
  RuntimeHeartbeatStatusBar,
  registerGovernancePresenceCommands,
} from './presence/governancePresence';
import {
  ConsumerRolloutMonitor,
  RolloutTreeProvider,
  registerConsumerRolloutCommands,
} from './rollout/consumerRollout';
import {ReasoningRoutingMonitor, ReasoningTierStatusBar} from './reasoningRouting/reasoningRouting';
import {ArchitecturePressureStatusBar, RuntimeGraphMonitor} from './runtimeGraph/runtimeGraph';
import {RuntimeSimplificationMonitor, SimplificationStatusBar} from './runtimeSimplification/runtimeSimplification';
import {BoundaryStateStore} from './state/boundaryState';
import {BoundedRetentionViewProvider} from './views/boundedRetentionView';
import {ContractOverlapViewProvider} from './views/contractOverlapView';
import {GovernanceDashboardViewProvider} from './views/governanceDashboardView';
import {GovernanceTrendViewProvider} from './views/governanceTrendView';
import {MergeCandidateViewProvider} from './views/mergeCandidateView';
import {PrimitiveReuseViewProvider} from './views/primitiveReuseView';
import {RuntimeClusterViewProvider} from './views/runtimeClusterView';
import {RuntimeGraphViewProvider} from './views/runtimeGraphView';
import {RuntimeOverlapViewProvider} from './views/runtimeOverlapView';
import {SessionBoundaryViewProvider} from './views/sessionBoundaryView';
import {SharedPrimitiveViewProvider} from './views/sharedPrimitiveView';

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
  const governanceCore = new GovernanceCoreMonitor();
  const governanceCoreStatus = new GovernanceCoreStatusBar(governanceCore);
  const sharedPrimitiveView = new SharedPrimitiveViewProvider(governanceCore);
  const primitiveReuseView = new PrimitiveReuseViewProvider(governanceCore);
  const boundedRetentionView = new BoundedRetentionViewProvider(governanceCore);
  const runtimeGraph = new RuntimeGraphMonitor();
  const architectureStatus = new ArchitecturePressureStatusBar(runtimeGraph);
  const runtimeGraphView = new RuntimeGraphViewProvider(runtimeGraph);
  const runtimeClusterView = new RuntimeClusterViewProvider(runtimeGraph);
  const runtimeSimplification = new RuntimeSimplificationMonitor();
  const simplificationStatus = new SimplificationStatusBar(runtimeSimplification);
  const runtimeOverlapView = new RuntimeOverlapViewProvider(runtimeSimplification);
  const contractOverlapView = new ContractOverlapViewProvider(runtimeSimplification);
  const mergeCandidateView = new MergeCandidateViewProvider(runtimeSimplification);
  const presence = new GovernancePresenceMonitor(context);
  const presenceStatus = new GovernancePresenceStatusBar(presence);
  const heartbeatStatus = new RuntimeHeartbeatStatusBar(presence);
  const rollout = new ConsumerRolloutMonitor();
  const rolloutView = new RolloutTreeProvider(rollout, 'rollout');
  const frictionView = new RolloutTreeProvider(rollout, 'friction');
  const readinessView = new RolloutTreeProvider(rollout, 'governance');
  const rollbackView = new RolloutTreeProvider(rollout, 'rollback');
  const reasoningRouting = new ReasoningRoutingMonitor();
  const reasoningStatus = new ReasoningTierStatusBar(reasoningRouting);
  const outputCompression = new OutputCompressionMonitor();
  const compactReportingStatus = new CompactReportingStatusBar(outputCompression);
  await persistence.ensure();
  const restored = await persistence.read();
  const governanceState = await governance.validate();
  const healthState = await governanceStatus.refresh();
  const trendState = await governanceTrendStatus.refresh();
  const coreState = governanceCoreStatus.refresh();
  const runtimeGraphState = architectureStatus.refresh();
  const simplificationState = simplificationStatus.refresh();
  const presenceState = await presenceStatus.refresh(restored, healthState, runtimeGraphState);
  await heartbeatStatus.refresh(restored, healthState, runtimeGraphState);
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
  if (runtimeGraphState.oversizedRuntimes.length > 0) {
    await notifications.warn(
      'startup-runtime-oversized-warning',
      `AI_DEV_OS oversized runtime clusters: ${runtimeGraphState.oversizedRuntimes.join(', ')}.`,
    );
  } else if (runtimeGraphState.crossBoundaryWarnings.length > 0) {
    await notifications.warn(
      'startup-runtime-cross-boundary-warning',
      'AI_DEV_OS runtime graph has cross-boundary pressure. Review the compact graph.',
    );
  }
  if (simplificationState.governanceGroups.length > 0) {
    await notifications.warn(
      'startup-runtime-simplification-governance-warning',
      `AI_DEV_OS governance duplication groups: ${simplificationState.governanceGroups.length}.`,
    );
  }
  if (coreState.duplicatedGovernanceWarningsReduced) {
    await notifications.info(
      'startup-governance-core-reuse',
      `AI_DEV_OS governance core primitive reuse targets: ${coreState.reuseTargets.length}.`,
    );
  }
  if (presenceState.staleExtension.staleExtensionDetected) {
    await notifications.warn(
      'startup-presence-stale-extension',
      'AI_DEV_OS installed extension is stale or missing visibility capabilities.',
    );
  }
  if (presenceState.heartbeat.staleHeartbeat) {
    await notifications.warn(
      'startup-presence-heartbeat-warning',
      'AI_DEV_OS runtime heartbeat is stale or unavailable.',
    );
  }
  const rolloutState = await rollout.evaluate();
  const reasoningState = reasoningStatus.refresh();
  const compactReportingState = compactReportingStatus.refresh();
  if (rolloutState.migrationFriction === 'HIGH' || rolloutState.migrationFriction === 'BLOCKED') {
    await notifications.warn(
      'startup-rollout-friction-warning',
      'AI_DEV_OS consumer rollout rehearsal found migration friction.',
    );
  }
  if (reasoningState.budgetPressure === 'HIGH' || reasoningState.budgetPressure === 'OVER_BUDGET') {
    await notifications.warn(
      'startup-reasoning-budget-pressure',
      'AI_DEV_OS reasoning budget pressure is elevated. Review cost budget before escalating.',
    );
  }
  if (compactReportingState.verbosityPressure === 'HIGH') {
    await notifications.warn(
      'startup-output-verbosity-pressure',
      'AI_DEV_OS report verbosity pressure is high. Use compact reporting or expand only when needed.',
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
    vscode.window.registerTreeDataProvider('aiDevOsSharedPrimitives', sharedPrimitiveView),
    vscode.window.registerTreeDataProvider('aiDevOsPrimitiveReuse', primitiveReuseView),
    vscode.window.registerTreeDataProvider('aiDevOsBoundedRetention', boundedRetentionView),
    vscode.window.registerTreeDataProvider('aiDevOsRuntimeGraph', runtimeGraphView),
    vscode.window.registerTreeDataProvider('aiDevOsRuntimeClusters', runtimeClusterView),
    vscode.window.registerTreeDataProvider('aiDevOsRuntimeOverlap', runtimeOverlapView),
    vscode.window.registerTreeDataProvider('aiDevOsContractOverlap', contractOverlapView),
    vscode.window.registerTreeDataProvider('aiDevOsMergeCandidates', mergeCandidateView),
    vscode.window.registerTreeDataProvider('aiDevOsRolloutReadiness', rolloutView),
    vscode.window.registerTreeDataProvider('aiDevOsMigrationFriction', frictionView),
    vscode.window.registerTreeDataProvider('aiDevOsGovernanceReadiness', readinessView),
    vscode.window.registerTreeDataProvider('aiDevOsRollbackRehearsal', rollbackView),
    governanceStatus,
    governanceTrendStatus,
    governanceCoreStatus,
    architectureStatus,
    simplificationStatus,
    presenceStatus,
    heartbeatStatus,
    reasoningStatus,
    compactReportingStatus,
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
    ...registerGovernanceCoreCommands(
      governanceCore,
      governanceCoreStatus,
      notifications,
      sharedPrimitiveView,
      primitiveReuseView,
      boundedRetentionView,
    ),
    ...registerRuntimeGraphCommands(
      runtimeGraph,
      architectureStatus,
      notifications,
      runtimeGraphView,
      runtimeClusterView,
    ),
    ...registerRuntimeSimplificationCommands(
      runtimeSimplification,
      simplificationStatus,
      notifications,
      runtimeOverlapView,
      contractOverlapView,
      mergeCandidateView,
    ),
    ...registerGovernancePresenceCommands(
      presence,
      presenceStatus,
      heartbeatStatus,
      notifications,
      restored,
      healthState,
      runtimeGraphState,
    ),
    ...registerConsumerRolloutCommands(
      rollout,
      notifications,
      [rolloutView, frictionView, readinessView, rollbackView],
    ),
    ...registerReasoningRoutingCommands(reasoningRouting, reasoningStatus, notifications),
    ...registerOutputCompressionCommands(outputCompression, compactReportingStatus, notifications),
  );
}

export function deactivate(): void {
  return;
}
