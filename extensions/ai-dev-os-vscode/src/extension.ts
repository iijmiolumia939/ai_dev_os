import * as vscode from 'vscode';
import {registerDevLoopCommands} from './commands/devLoopCommands';
import {registerGovernanceCoreCommands} from './commands/governanceCoreCommands';
import {registerGovernanceCommands} from './commands/governanceCommands';
import {registerGovernanceHealthCommands} from './commands/governanceHealthCommands';
import {registerGovernanceTrendCommands} from './commands/governanceTrendCommands';
import {registerIncrementalContextCommands} from './commands/incrementalContextCommands';
import {registerOutputCompressionCommands} from './commands/outputCompressionCommands';
import {registerPersistenceCommands} from './commands/persistenceCommands';
import {registerProviderRoutingCommands} from './commands/providerRoutingCommands';
import {registerReasoningRoutingCommands} from './commands/reasoningRoutingCommands';
import {registerReasoningScopeCommands} from './commands/reasoningScopeCommands';
import {registerRetrievalBudgetCommands} from './commands/retrievalBudgetCommands';
import {registerRuntimeGraphCommands} from './commands/runtimeGraphCommands';
import {registerRuntimeSimplificationCommands} from './commands/runtimeSimplificationCommands';
import {registerSessionCommands} from './commands/sessionCommands';
import {registerSprintMemoryCommands} from './commands/sprintMemoryCommands';
import {GovernanceHealthMonitor, GovernanceStatusBar} from './governance/health';
import {GovernanceTrendMonitor, GovernanceTrendStatusBar} from './governance/trends';
import {GovernanceCoreMonitor, GovernanceCoreStatusBar} from './governanceCore/governanceCore';
import {IncrementalContextMonitor, IncrementalContextStatusBar} from './incrementalContext/incrementalContext';
import {RateLimitedNotifications} from './notifications/rateLimitedNotifications';
import {CompactReportingStatusBar, OutputCompressionMonitor} from './outputCompression/outputCompression';
import {PersistenceGovernance} from './persistence/governance';
import {LocalPersistenceStore} from './persistence/localPersistence';
import {
  PremiumProviderStatusBar,
  ProviderDowngradeStatusBar,
  ProviderPressureStatusBar,
  ProviderRoutingMonitor,
} from './providerRouting/providerRouting';
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
import {ReasoningScopeMonitor, ReasoningScopeStatusBar} from './reasoningScope/reasoningScope';
import {RetrievalBudgetMonitor, RetrievalBudgetStatusBar} from './retrievalBudget/retrievalBudget';
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
import {
  LocalPatchRequiredStatusBar,
  SprintActiveStatusBar,
  SprintDevLoopMonitor,
  SprintPressureStatusBar,
  SprintRolloverStatusBar,
} from './devLoop/devLoop';
import {
  MemoryEvictionStatusBar,
  MemoryPressureStatusBar,
  PatternStableStatusBar,
  SprintMemoryMonitor,
  SprintMemoryStatusBar,
} from './sprintMemory/sprintMemory';

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
  const reasoningScope = new ReasoningScopeMonitor();
  const reasoningScopeStatus = new ReasoningScopeStatusBar(reasoningScope);
  const outputCompression = new OutputCompressionMonitor();
  const compactReportingStatus = new CompactReportingStatusBar(outputCompression);
  const retrievalBudget = new RetrievalBudgetMonitor();
  const retrievalBudgetStatus = new RetrievalBudgetStatusBar(retrievalBudget);
  const incrementalContext = new IncrementalContextMonitor();
  const incrementalContextStatus = new IncrementalContextStatusBar(incrementalContext);
  const providerRouting = new ProviderRoutingMonitor();
  const premiumProviderStatus = new PremiumProviderStatusBar(providerRouting);
  const providerDowngradeStatus = new ProviderDowngradeStatusBar(providerRouting);
  const providerPressureStatus = new ProviderPressureStatusBar(providerRouting);
  const devLoop = new SprintDevLoopMonitor();
  const sprintActiveStatus = new SprintActiveStatusBar(devLoop);
  const sprintRolloverStatus = new SprintRolloverStatusBar(devLoop);
  const sprintPressureStatus = new SprintPressureStatusBar(devLoop);
  const localPatchRequiredStatus = new LocalPatchRequiredStatusBar(devLoop);
  const sprintMemory = new SprintMemoryMonitor();
  const sprintMemoryStatus = new SprintMemoryStatusBar(sprintMemory);
  const memoryPressureStatus = new MemoryPressureStatusBar(sprintMemory);
  const patternStableStatus = new PatternStableStatusBar(sprintMemory);
  const memoryEvictionStatus = new MemoryEvictionStatusBar(sprintMemory);
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
  const reasoningScopeState = reasoningScopeStatus.refresh();
  const compactReportingState = compactReportingStatus.refresh();
  const retrievalBudgetState = retrievalBudgetStatus.refresh();
  const incrementalContextState = incrementalContextStatus.refresh();
  const providerRoutingState = premiumProviderStatus.refresh();
  providerDowngradeStatus.refresh();
  providerPressureStatus.refresh();
  const devLoopState = sprintActiveStatus.refresh();
  sprintRolloverStatus.refresh();
  sprintPressureStatus.refresh();
  localPatchRequiredStatus.refresh();
  const sprintMemoryState = sprintMemoryStatus.refresh();
  memoryPressureStatus.refresh();
  patternStableStatus.refresh();
  memoryEvictionStatus.refresh();
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
  if (reasoningScopeState.reasoningPressure === 'HIGH') {
    await notifications.warn(
      'startup-premium-reasoning-pressure',
      'AI_DEV_OS premium reasoning pressure is high. Use local patch mode before escalating.',
    );
  }
  if (compactReportingState.verbosityPressure === 'HIGH') {
    await notifications.warn(
      'startup-output-verbosity-pressure',
      'AI_DEV_OS report verbosity pressure is high. Use compact reporting or expand only when needed.',
    );
  }
  if (retrievalBudgetState.retrievalPressure === 'HIGH') {
    await notifications.warn(
      'startup-retrieval-pressure-warning',
      'AI_DEV_OS retrieval pressure is high. Compact retrieval scope before broad reasoning.',
    );
  }
  if (incrementalContextState.replayPressure === 'HIGH') {
    await notifications.warn(
      'startup-replay-pressure-warning',
      'AI_DEV_OS replay pressure is high. Continue with delta context only.',
    );
  }
  if (providerRoutingState.providerBurnPressure === 'HIGH') {
    await notifications.warn(
      'startup-provider-routing-pressure-warning',
      'AI_DEV_OS provider pressure is high. Review downgrade recommendations before premium use.',
    );
  }
  if (devLoopState.sprintPressure === 'HIGH') {
    await notifications.warn(
      'startup-sprint-pressure-warning',
      'AI_DEV_OS sprint pressure is high. Compact sprint closure before generating the next sprint.',
    );
  }
  if (sprintMemoryState.memoryPressure === 'HIGH') {
    await notifications.warn(
      'startup-sprint-memory-pressure-warning',
      'AI_DEV_OS sprint memory pressure is high. Cleanup stale sprint memory before continuing.',
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
    reasoningScopeStatus,
    compactReportingStatus,
    retrievalBudgetStatus,
    incrementalContextStatus,
    premiumProviderStatus,
    providerDowngradeStatus,
    providerPressureStatus,
    sprintActiveStatus,
    sprintRolloverStatus,
    sprintPressureStatus,
    localPatchRequiredStatus,
    sprintMemoryStatus,
    memoryPressureStatus,
    patternStableStatus,
    memoryEvictionStatus,
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
    ...registerReasoningScopeCommands(reasoningScope, reasoningScopeStatus, notifications),
    ...registerOutputCompressionCommands(outputCompression, compactReportingStatus, notifications),
    ...registerRetrievalBudgetCommands(retrievalBudget, retrievalBudgetStatus, notifications),
    ...registerIncrementalContextCommands(
      incrementalContext,
      incrementalContextStatus,
      notifications,
    ),
    ...registerProviderRoutingCommands(
      providerRouting,
      premiumProviderStatus,
      providerDowngradeStatus,
      providerPressureStatus,
      notifications,
    ),
    ...registerDevLoopCommands(
      devLoop,
      sprintActiveStatus,
      sprintRolloverStatus,
      sprintPressureStatus,
      localPatchRequiredStatus,
      notifications,
    ),
    ...registerSprintMemoryCommands(
      sprintMemory,
      sprintMemoryStatus,
      memoryPressureStatus,
      patternStableStatus,
      memoryEvictionStatus,
      notifications,
    ),
  );
}

export function deactivate(): void {
  return;
}
