import * as vscode from 'vscode';
import {registerAdaptiveProviderCommands} from './commands/adaptiveProviderCommands';
import {registerCognitiveStateCommands} from './commands/cognitiveStateCommands';
import {registerDevExecutionCommands} from './commands/devExecutionCommands';
import {registerDevPolicyCommands} from './commands/devPolicyCommands';
import {registerDevStrategyCommands} from './commands/devStrategyCommands';
import {registerDevLoopCommands} from './commands/devLoopCommands';
import {registerExecutionCoordinationCommands} from './commands/executionCoordinationCommands';
import {registerExecutionContinuationCommands} from './commands/executionContinuationCommands';
import {registerExecutionMemoryCommands} from './commands/executionMemoryCommands';
import {registerExecutionIntentCommands} from './commands/executionIntentCommands';
import {registerExecutionQualityCommands} from './commands/executionQualityCommands';
import {registerExecutionRecoveryCommands} from './commands/executionRecoveryCommands';
import {registerExecutionSaturationCommands} from './commands/executionSaturationCommands';
import {registerExecutionSessionCommands} from './commands/executionSessionCommands';
import {registerExecutionStabilityCommands} from './commands/executionStabilityCommands';
import {registerGovernanceCoreCommands} from './commands/governanceCoreCommands';
import {registerGovernanceCommands} from './commands/governanceCommands';
import {registerGovernanceHealthCommands} from './commands/governanceHealthCommands';
import {registerGovernanceTrendCommands} from './commands/governanceTrendCommands';
import {registerIntentionalPlanningCommands} from './commands/intentionalPlanningCommands';
import {registerIncrementalContextCommands} from './commands/incrementalContextCommands';
import {registerLocalProviderCommands} from './commands/localProviderCommands';
import {registerOutputCompressionCommands} from './commands/outputCompressionCommands';
import {registerPersistenceCommands} from './commands/persistenceCommands';
import {registerProviderExperimentalCommands} from './commands/providerExperimentalCommands';
import {registerProviderRoutingCommands} from './commands/providerRoutingCommands';
import {registerReasoningRoutingCommands} from './commands/reasoningRoutingCommands';
import {registerReasoningScopeCommands} from './commands/reasoningScopeCommands';
import {registerReflectiveEvaluationCommands} from './commands/reflectiveEvaluationCommands';
import {registerRetrievalBudgetCommands} from './commands/retrievalBudgetCommands';
import {registerRuntimeGraphCommands} from './commands/runtimeGraphCommands';
import {registerRuntimeMediationCommands} from './commands/runtimeMediationCommands';
import {registerRuntimeOrchestratorCommands} from './commands/runtimeOrchestratorCommands';
import {registerRuntimePolicyCommands} from './commands/runtimePolicyCommands';
import {registerRuntimeSimplificationCommands} from './commands/runtimeSimplificationCommands';
import {registerSessionCommands} from './commands/sessionCommands';
import {registerSprintLoopCommands} from './commands/sprintLoopCommands';
import {registerSprintMemoryCommands} from './commands/sprintMemoryCommands';
import {registerSubagentExecutionCommands} from './commands/subagentExecutionCommands';
import {registerVerifiedExecutionCommands} from './commands/verifiedExecutionCommands';
import {
  AdaptiveProviderMonitor,
  CostGuardedStatusBar,
  FatigueTrackedStatusBar,
  LocalFirstStatusBar,
  ProviderBoundedStatusBar,
} from './adaptiveProvider/adaptiveProvider';
import {
  ExecutionMemoryMonitor,
  ExecutionMemoryStatusBar,
  ProviderMemoryStatusBar,
  RetryMemoryStatusBar,
  ReuseBoundedStatusBar,
} from './executionMemory/executionMemory';
import {GovernanceHealthMonitor, GovernanceStatusBar} from './governance/health';
import {GovernanceTrendMonitor, GovernanceTrendStatusBar} from './governance/trends';
import {GovernanceCoreMonitor, GovernanceCoreStatusBar} from './governanceCore/governanceCore';
import {
  AttentionFocusStatusBar,
  CognitiveLoadStatusBar,
  CognitiveStateMemoryPressureStatusBar,
  CognitiveStateMonitor,
} from './cognitiveState/cognitiveState';
import {
  ContinuationStableStatusBar,
  DecayTrackedStatusBar,
  GoalActiveStatusBar,
  IntentionalPlanningMonitor,
  PlanningBoundedStatusBar,
} from './intentionalPlanning/intentionalPlanning';
import {
  ContinuationValidStatusBar,
  ExecutionCoherentStatusBar,
  PlanningStableStatusBar,
  ReflectionBoundedStatusBar,
  ReflectiveEvaluationMonitor,
} from './reflectiveEvaluation/reflectiveEvaluation';
import {IncrementalContextMonitor, IncrementalContextStatusBar} from './incrementalContext/incrementalContext';
import {RateLimitedNotifications} from './notifications/rateLimitedNotifications';
import {CompactReportingStatusBar, OutputCompressionMonitor} from './outputCompression/outputCompression';
import {PersistenceGovernance} from './persistence/governance';
import {LocalPersistenceStore} from './persistence/localPersistence';
import {
  LocalBudgetOkStatusBar,
  LocalProviderMonitor,
  LocalProviderReadyStatusBar,
  OllamaActiveStatusBar,
  PremiumEscalationStatusBar,
} from './localProvider/localProvider';
import {
  PremiumProviderStatusBar,
  ProviderDowngradeStatusBar,
  ProviderPressureStatusBar,
  ProviderRoutingMonitor,
} from './providerRouting/providerRouting';
import {
  AdaptiveRoutingStatusBar,
  BenchmarkActiveStatusBar,
  CognitiveMemoryPressureStatusBar,
  CompactnessDecayStatusBar,
  ContinuityInflationStatusBar,
  DriftAwareRoutingStatusBar,
  DriftRiskStatusBar,
  EntropyGuardedStatusBar,
  ExperimentalProviderStatusBar,
  FatigueEscalationPressureStatusBar,
  FatigueLowStatusBar,
  GovernanceWeightedRoutingStatusBar,
  GovernanceStableStatusBar,
  ProviderExperimentalMonitor,
  RecoveryAvailableStatusBar,
  RetrievalBoundedStatusBar,
  StableLocalStatusBar,
} from './providerExperimental/providerExperimental';
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
import {
  EscalationGuardedStatusBar,
  GovernanceStablePolicyStatusBar,
  LocalFirstPolicyStatusBar,
  PolicyBoundedStatusBar,
  RuntimePolicyMonitor,
} from './runtimePolicy/runtimePolicy';
import {
  ContinuationOrderedStatusBar,
  OrchestrationBoundedStatusBar,
  RetryOrderedStatusBar,
  RuntimeOrchestratorMonitor,
  SchedulingStableStatusBar,
} from './runtimeOrchestrator/runtimeOrchestrator';
import {ArchitecturePressureStatusBar, RuntimeGraphMonitor} from './runtimeGraph/runtimeGraph';
import {RuntimeSimplificationMonitor, SimplificationStatusBar} from './runtimeSimplification/runtimeSimplification';
import {
  CommitReadyStatusBar,
  RegressionTrackedStatusBar,
  SprintBoundedStatusBar,
  SprintLoopMonitor,
  SprintValidationStableStatusBar,
} from './sprintLoop/sprintLoop';
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
  CheckpointReadyStatusBar,
  DevExecutionMonitor,
  ExecutionActiveStatusBar,
  RollbackSafeStatusBar,
  ValidationStableStatusBar,
} from './devExecution/devExecution';
import {
  BoundedExecutionStatusBar,
  ContinuationSafeStatusBar,
  ExecutionContinuationMonitor,
  ExecutionContinuingStatusBar,
  LoopGuardedStatusBar,
} from './executionContinuation/executionContinuation';
import {
  ConflictsBoundedStatusBar,
  CoordinationGuardedStatusBar,
  CoordinationStableStatusBar,
  ExecutionCoordinationMonitor,
  RuntimePrioritySafeStatusBar,
} from './executionCoordination/executionCoordination';
import {
  ExecutionIntentMonitor,
  ExecutionSemanticsActiveStatusBar,
  IntentStableStatusBar,
  PriorityBoundedStatusBar,
  TransitionsSafeStatusBar,
} from './executionIntent/executionIntent';
import {
  ExecutionQualityMonitor,
  ExecutionSignalStableStatusBar,
  QualityBoundedStatusBar,
  QualityDriftSafeStatusBar,
  RedundancyLowStatusBar,
} from './executionQuality/executionQuality';
import {
  ExecutionSessionMonitor,
  LifecycleBoundedStatusBar,
  PersistenceGuardedStatusBar,
  SessionIntegritySafeStatusBar,
  SessionStableStatusBar,
} from './executionSession/executionSession';
import {
  DriftLowStatusBar,
  ExecutionStabilityMonitor,
  OscillationStableStatusBar,
  PersistenceSafeStatusBar,
  StabilityBoundedStatusBar,
} from './executionStability/executionStability';
import {
  CheckpointValidStatusBar,
  ExecutionRecoveryMonitor,
  RecoveryCooldownStatusBar,
  RecoverySafeStatusBar,
  RollbackBoundedStatusBar,
} from './executionRecovery/executionRecovery';
import {
  ContinuationBoundedStatusBar,
  ExecutionSaturationMonitor,
  RetryStableStatusBar,
  SaturationLowStatusBar,
  ToolPressureSafeStatusBar,
} from './executionSaturation/executionSaturation';
import {
  DevPolicyMonitor,
  EscalationPressureStatusBar,
  GovernancePressureStatusBar,
  PolicyStableStatusBar,
  RealismProtectedStatusBar,
} from './devPolicy/devPolicy';
import {
  CostPressureStatusBar,
  DevStrategyMonitor,
  ProviderEfficiencyStatusBar,
  RoadmapPressureStatusBar,
  StrategyStableStatusBar,
} from './devStrategy/devStrategy';
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
import {
  FallbackReadyStatusBar,
  LocalDelegationStatusBar,
  SubagentActiveStatusBar,
  SubagentExecutionMonitor,
  SwarmBlockedStatusBar,
} from './subagentExecution/subagentExecution';
import {
  CommandGroundedStatusBar,
  GitEvidenceSafeStatusBar,
  PytestVerifiedStatusBar,
  VerifiedExecutionMonitor,
  VerifiedExecutionStatusBar,
} from './verifiedExecution/verifiedExecution';
import {
  CooldownStableStatusBar,
  ExecutionBoundedStatusBar,
  MediationActiveStatusBar,
  RetryGovernedStatusBar,
  RuntimeMediationMonitor,
} from './runtimeMediation/runtimeMediation';

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
  const providerExperimental = new ProviderExperimentalMonitor();
  const experimentalProviderStatus = new ExperimentalProviderStatusBar(providerExperimental);
  const driftRiskStatus = new DriftRiskStatusBar(providerExperimental);
  const governanceStableStatus = new GovernanceStableStatusBar(providerExperimental);
  const benchmarkActiveStatus = new BenchmarkActiveStatusBar(providerExperimental);
  const adaptiveRoutingStatus = new AdaptiveRoutingStatusBar(providerExperimental);
  const stableLocalStatus = new StableLocalStatusBar(providerExperimental);
  const driftAwareRoutingStatus = new DriftAwareRoutingStatusBar(providerExperimental);
  const governanceWeightedRoutingStatus = new GovernanceWeightedRoutingStatusBar(providerExperimental);
  const fatigueLowStatus = new FatigueLowStatusBar(providerExperimental);
  const fatigueEscalationPressureStatus = new FatigueEscalationPressureStatusBar(providerExperimental);
  const compactnessDecayStatus = new CompactnessDecayStatusBar(providerExperimental);
  const recoveryAvailableStatus = new RecoveryAvailableStatusBar(providerExperimental);
  const cognitiveMemoryPressureStatus = new CognitiveMemoryPressureStatusBar(providerExperimental);
  const continuityInflationStatus = new ContinuityInflationStatusBar(providerExperimental);
  const retrievalBoundedStatus = new RetrievalBoundedStatusBar(providerExperimental);
  const entropyGuardedStatus = new EntropyGuardedStatusBar(providerExperimental);
  const localProvider = new LocalProviderMonitor();
  const localProviderReadyStatus = new LocalProviderReadyStatusBar(localProvider);
  const ollamaActiveStatus = new OllamaActiveStatusBar(localProvider);
  const localBudgetOkStatus = new LocalBudgetOkStatusBar(localProvider);
  const premiumEscalationStatus = new PremiumEscalationStatusBar(localProvider);
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
  const devStrategy = new DevStrategyMonitor();
  const strategyStableStatus = new StrategyStableStatusBar(devStrategy);
  const costPressureStatus = new CostPressureStatusBar(devStrategy);
  const providerEfficiencyStatus = new ProviderEfficiencyStatusBar(devStrategy);
  const roadmapPressureStatus = new RoadmapPressureStatusBar(devStrategy);
  const devPolicy = new DevPolicyMonitor();
  const policyStableStatus = new PolicyStableStatusBar(devPolicy);
  const governancePressureStatus = new GovernancePressureStatusBar(devPolicy);
  const escalationPressureStatus = new EscalationPressureStatusBar(devPolicy);
  const realismProtectedStatus = new RealismProtectedStatusBar(devPolicy);
  const devExecution = new DevExecutionMonitor();
  const executionActiveStatus = new ExecutionActiveStatusBar(devExecution);
  const checkpointReadyStatus = new CheckpointReadyStatusBar(devExecution);
  const validationStableStatus = new ValidationStableStatusBar(devExecution);
  const rollbackSafeStatus = new RollbackSafeStatusBar(devExecution);
  const executionContinuation = new ExecutionContinuationMonitor();
  const executionContinuingStatus = new ExecutionContinuingStatusBar(executionContinuation);
  const continuationSafeStatus = new ContinuationSafeStatusBar(executionContinuation);
  const loopGuardedStatus = new LoopGuardedStatusBar(executionContinuation);
  const boundedExecutionStatus = new BoundedExecutionStatusBar(executionContinuation);
  const executionSaturation = new ExecutionSaturationMonitor();
  const saturationLowStatus = new SaturationLowStatusBar(executionSaturation);
  const retryStableStatus = new RetryStableStatusBar(executionSaturation);
  const toolPressureSafeStatus = new ToolPressureSafeStatusBar(executionSaturation);
  const continuationBoundedStatus = new ContinuationBoundedStatusBar(executionSaturation);
  const executionRecovery = new ExecutionRecoveryMonitor();
  const recoverySafeStatus = new RecoverySafeStatusBar(executionRecovery);
  const checkpointValidStatus = new CheckpointValidStatusBar(executionRecovery);
  const recoveryCooldownStatus = new RecoveryCooldownStatusBar(executionRecovery);
  const rollbackBoundedStatus = new RollbackBoundedStatusBar(executionRecovery);
  const executionCoordination = new ExecutionCoordinationMonitor();
  const coordinationStableStatus = new CoordinationStableStatusBar(executionCoordination);
  const conflictsBoundedStatus = new ConflictsBoundedStatusBar(executionCoordination);
  const runtimePrioritySafeStatus = new RuntimePrioritySafeStatusBar(executionCoordination);
  const coordinationGuardedStatus = new CoordinationGuardedStatusBar(executionCoordination);
  const executionIntent = new ExecutionIntentMonitor();
  const intentStableStatus = new IntentStableStatusBar(executionIntent);
  const priorityBoundedStatus = new PriorityBoundedStatusBar(executionIntent);
  const transitionsSafeStatus = new TransitionsSafeStatusBar(executionIntent);
  const executionSemanticsActiveStatus = new ExecutionSemanticsActiveStatusBar(executionIntent);
  const executionSession = new ExecutionSessionMonitor();
  const sessionStableStatus = new SessionStableStatusBar(executionSession);
  const lifecycleBoundedStatus = new LifecycleBoundedStatusBar(executionSession);
  const sessionIntegritySafeStatus = new SessionIntegritySafeStatusBar(executionSession);
  const persistenceGuardedStatus = new PersistenceGuardedStatusBar(executionSession);
  const executionStabilityRuntime = new ExecutionStabilityMonitor();
  const stabilityBoundedStatus = new StabilityBoundedStatusBar(executionStabilityRuntime);
  const driftLowStatus = new DriftLowStatusBar(executionStabilityRuntime);
  const oscillationStableStatus = new OscillationStableStatusBar(executionStabilityRuntime);
  const persistenceSafeStatus = new PersistenceSafeStatusBar(executionStabilityRuntime);
  const executionQuality = new ExecutionQualityMonitor();
  const qualityBoundedStatus = new QualityBoundedStatusBar(executionQuality);
  const redundancyLowStatus = new RedundancyLowStatusBar(executionQuality);
  const qualityDriftSafeStatus = new QualityDriftSafeStatusBar(executionQuality);
  const executionSignalStableStatus = new ExecutionSignalStableStatusBar(executionQuality);
  const subagentExecution = new SubagentExecutionMonitor();
  const subagentActiveStatus = new SubagentActiveStatusBar(subagentExecution);
  const localDelegationStatus = new LocalDelegationStatusBar(subagentExecution);
  const fallbackReadyStatus = new FallbackReadyStatusBar(subagentExecution);
  const swarmBlockedStatus = new SwarmBlockedStatusBar(subagentExecution);
  const verifiedExecution = new VerifiedExecutionMonitor();
  const verifiedExecutionStatus = new VerifiedExecutionStatusBar(verifiedExecution);
  const commandGroundedStatus = new CommandGroundedStatusBar(verifiedExecution);
  const pytestVerifiedStatus = new PytestVerifiedStatusBar(verifiedExecution);
  const gitEvidenceSafeStatus = new GitEvidenceSafeStatusBar(verifiedExecution);
  const runtimeMediation = new RuntimeMediationMonitor();
  const mediationActiveStatus = new MediationActiveStatusBar(runtimeMediation);
  const executionBoundedStatus = new ExecutionBoundedStatusBar(runtimeMediation);
  const retryGovernedStatus = new RetryGovernedStatusBar(runtimeMediation);
  const cooldownStableStatus = new CooldownStableStatusBar(runtimeMediation);
  const cognitiveState = new CognitiveStateMonitor();
  const cognitiveLoadStatus = new CognitiveLoadStatusBar(cognitiveState);
  const attentionFocusStatus = new AttentionFocusStatusBar(cognitiveState);
  const cognitiveStateMemoryPressureStatus = new CognitiveStateMemoryPressureStatusBar(
    cognitiveState,
  );
  const intentionalPlanning = new IntentionalPlanningMonitor();
  const goalActiveStatus = new GoalActiveStatusBar(intentionalPlanning);
  const planningBoundedStatus = new PlanningBoundedStatusBar(intentionalPlanning);
  const decayTrackedStatus = new DecayTrackedStatusBar(intentionalPlanning);
  const continuationStableStatus = new ContinuationStableStatusBar(intentionalPlanning);
  const reflectiveEvaluation = new ReflectiveEvaluationMonitor();
  const reflectionBoundedStatus = new ReflectionBoundedStatusBar(reflectiveEvaluation);
  const executionCoherentStatus = new ExecutionCoherentStatusBar(reflectiveEvaluation);
  const continuationValidStatus = new ContinuationValidStatusBar(reflectiveEvaluation);
  const planningStableStatus = new PlanningStableStatusBar(reflectiveEvaluation);
  const adaptiveProvider = new AdaptiveProviderMonitor();
  const providerBoundedStatus = new ProviderBoundedStatusBar(adaptiveProvider);
  const localFirstStatus = new LocalFirstStatusBar(adaptiveProvider);
  const fatigueTrackedStatus = new FatigueTrackedStatusBar(adaptiveProvider);
  const costGuardedStatus = new CostGuardedStatusBar(adaptiveProvider);
  const executionMemory = new ExecutionMemoryMonitor();
  const executionMemoryStatus = new ExecutionMemoryStatusBar(executionMemory);
  const retryMemoryStatus = new RetryMemoryStatusBar(executionMemory);
  const reuseBoundedStatus = new ReuseBoundedStatusBar(executionMemory);
  const providerMemoryStatus = new ProviderMemoryStatusBar(executionMemory);
  const runtimePolicy = new RuntimePolicyMonitor();
  const policyBoundedStatus = new PolicyBoundedStatusBar(runtimePolicy);
  const governanceStablePolicyStatus = new GovernanceStablePolicyStatusBar(runtimePolicy);
  const localFirstPolicyStatus = new LocalFirstPolicyStatusBar(runtimePolicy);
  const escalationGuardedStatus = new EscalationGuardedStatusBar(runtimePolicy);
  const sprintLoop = new SprintLoopMonitor();
  const sprintBoundedStatus = new SprintBoundedStatusBar(sprintLoop);
  const sprintValidationStableStatus = new SprintValidationStableStatusBar(sprintLoop);
  const regressionTrackedStatus = new RegressionTrackedStatusBar(sprintLoop);
  const commitReadyStatus = new CommitReadyStatusBar(sprintLoop);
  const runtimeOrchestrator = new RuntimeOrchestratorMonitor();
  const orchestrationBoundedStatus = new OrchestrationBoundedStatusBar(runtimeOrchestrator);
  const schedulingStableStatus = new SchedulingStableStatusBar(runtimeOrchestrator);
  const retryOrderedStatus = new RetryOrderedStatusBar(runtimeOrchestrator);
  const continuationOrderedStatus = new ContinuationOrderedStatusBar(runtimeOrchestrator);
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
  experimentalProviderStatus.refresh();
  driftRiskStatus.refresh();
  governanceStableStatus.refresh();
  benchmarkActiveStatus.refresh();
  adaptiveRoutingStatus.refresh();
  stableLocalStatus.refresh();
  driftAwareRoutingStatus.refresh();
  governanceWeightedRoutingStatus.refresh();
  fatigueLowStatus.refresh();
  fatigueEscalationPressureStatus.refresh();
  compactnessDecayStatus.refresh();
  recoveryAvailableStatus.refresh();
  cognitiveMemoryPressureStatus.refresh();
  continuityInflationStatus.refresh();
  retrievalBoundedStatus.refresh();
  entropyGuardedStatus.refresh();
  const localProviderState = localProviderReadyStatus.refresh();
  ollamaActiveStatus.refresh();
  localBudgetOkStatus.refresh();
  premiumEscalationStatus.refresh();
  const devLoopState = sprintActiveStatus.refresh();
  sprintRolloverStatus.refresh();
  sprintPressureStatus.refresh();
  localPatchRequiredStatus.refresh();
  const sprintMemoryState = sprintMemoryStatus.refresh();
  memoryPressureStatus.refresh();
  patternStableStatus.refresh();
  memoryEvictionStatus.refresh();
  const strategyState = strategyStableStatus.refresh();
  costPressureStatus.refresh();
  providerEfficiencyStatus.refresh();
  roadmapPressureStatus.refresh();
  const policyState = policyStableStatus.refresh();
  governancePressureStatus.refresh();
  escalationPressureStatus.refresh();
  realismProtectedStatus.refresh();
  const executionState = executionActiveStatus.refresh();
  checkpointReadyStatus.refresh();
  sprintValidationStableStatus.refresh();
  rollbackSafeStatus.refresh();
  executionContinuingStatus.refresh();
  continuationSafeStatus.refresh();
  loopGuardedStatus.refresh();
  boundedExecutionStatus.refresh();
  saturationLowStatus.refresh();
  retryStableStatus.refresh();
  toolPressureSafeStatus.refresh();
  continuationBoundedStatus.refresh();
  recoverySafeStatus.refresh();
  checkpointValidStatus.refresh();
  recoveryCooldownStatus.refresh();
  rollbackBoundedStatus.refresh();
  coordinationStableStatus.refresh();
  conflictsBoundedStatus.refresh();
  runtimePrioritySafeStatus.refresh();
  coordinationGuardedStatus.refresh();
  intentStableStatus.refresh();
  priorityBoundedStatus.refresh();
  transitionsSafeStatus.refresh();
  executionSemanticsActiveStatus.refresh();
  sessionStableStatus.refresh();
  lifecycleBoundedStatus.refresh();
  sessionIntegritySafeStatus.refresh();
  persistenceGuardedStatus.refresh();
  stabilityBoundedStatus.refresh();
  driftLowStatus.refresh();
  oscillationStableStatus.refresh();
  persistenceSafeStatus.refresh();
  qualityBoundedStatus.refresh();
  redundancyLowStatus.refresh();
  qualityDriftSafeStatus.refresh();
  executionSignalStableStatus.refresh();
  const subagentState = subagentActiveStatus.refresh();
  localDelegationStatus.refresh();
  fallbackReadyStatus.refresh();
  swarmBlockedStatus.refresh();
  verifiedExecutionStatus.refresh();
  commandGroundedStatus.refresh();
  pytestVerifiedStatus.refresh();
  gitEvidenceSafeStatus.refresh();
  mediationActiveStatus.refresh();
  executionBoundedStatus.refresh();
  retryGovernedStatus.refresh();
  cooldownStableStatus.refresh();
  cognitiveLoadStatus.refresh();
  attentionFocusStatus.refresh();
  cognitiveStateMemoryPressureStatus.refresh();
  goalActiveStatus.refresh();
  planningBoundedStatus.refresh();
  decayTrackedStatus.refresh();
  continuationStableStatus.refresh();
  reflectionBoundedStatus.refresh();
  executionCoherentStatus.refresh();
  continuationValidStatus.refresh();
  planningStableStatus.refresh();
  providerBoundedStatus.refresh();
  localFirstStatus.refresh();
  fatigueTrackedStatus.refresh();
  costGuardedStatus.refresh();
  executionMemoryStatus.refresh();
  retryMemoryStatus.refresh();
  reuseBoundedStatus.refresh();
  providerMemoryStatus.refresh();
  policyBoundedStatus.refresh();
  governanceStablePolicyStatus.refresh();
  localFirstPolicyStatus.refresh();
  escalationGuardedStatus.refresh();
  sprintBoundedStatus.refresh();
  validationStableStatus.refresh();
  regressionTrackedStatus.refresh();
  commitReadyStatus.refresh();
  orchestrationBoundedStatus.refresh();
  schedulingStableStatus.refresh();
  retryOrderedStatus.refresh();
  continuationOrderedStatus.refresh();
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
  if (!localProviderState.localBudgetOk) {
    await notifications.warn(
      'startup-local-provider-budget-warning',
      'AI_DEV_OS local provider budget is not ready. Compact local execution before routing LOW tasks.',
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
  if (strategyState.roadmapPressure === 'HIGH' || strategyState.costPressure === 'HIGH') {
    await notifications.warn(
      'startup-development-strategy-pressure-warning',
      'AI_DEV_OS development strategy pressure is high. Compact strategy summary before planning.',
    );
  }
  if (
    policyState.governancePressure === 'HIGH' ||
    policyState.escalationPressure === 'HIGH'
  ) {
    await notifications.warn(
      'startup-development-policy-pressure-warning',
      'AI_DEV_OS development policy pressure is high. Compact policy summary before gating.',
    );
  }
  if (executionState.executionPressure === 'HIGH' || !executionState.rollbackSafe) {
    await notifications.warn(
      'startup-development-execution-pressure-warning',
      'AI_DEV_OS development execution pressure is high. Compact execution summary before continuing.',
    );
  }
  if (!subagentState.swarmBlocked || !subagentState.fallbackReady) {
    await notifications.warn(
      'startup-subagent-execution-warning',
      'AI_DEV_OS subagent delegation is not bounded. Compact delegation summary before continuing.',
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
    experimentalProviderStatus,
    driftRiskStatus,
    governanceStableStatus,
    benchmarkActiveStatus,
    adaptiveRoutingStatus,
    stableLocalStatus,
    driftAwareRoutingStatus,
    governanceWeightedRoutingStatus,
    fatigueLowStatus,
    fatigueEscalationPressureStatus,
    compactnessDecayStatus,
    recoveryAvailableStatus,
    cognitiveMemoryPressureStatus,
    continuityInflationStatus,
    retrievalBoundedStatus,
    entropyGuardedStatus,
    localProviderReadyStatus,
    ollamaActiveStatus,
    localBudgetOkStatus,
    premiumEscalationStatus,
    sprintActiveStatus,
    sprintRolloverStatus,
    sprintPressureStatus,
    localPatchRequiredStatus,
    sprintMemoryStatus,
    memoryPressureStatus,
    patternStableStatus,
    memoryEvictionStatus,
    strategyStableStatus,
    costPressureStatus,
    providerEfficiencyStatus,
    roadmapPressureStatus,
    policyStableStatus,
    governancePressureStatus,
    escalationPressureStatus,
    realismProtectedStatus,
    executionActiveStatus,
    checkpointReadyStatus,
    sprintValidationStableStatus,
    rollbackSafeStatus,
    executionContinuingStatus,
    continuationSafeStatus,
    loopGuardedStatus,
    boundedExecutionStatus,
    saturationLowStatus,
    retryStableStatus,
    toolPressureSafeStatus,
    continuationBoundedStatus,
    recoverySafeStatus,
    checkpointValidStatus,
    recoveryCooldownStatus,
    rollbackBoundedStatus,
    coordinationStableStatus,
    conflictsBoundedStatus,
    runtimePrioritySafeStatus,
    coordinationGuardedStatus,
    intentStableStatus,
    priorityBoundedStatus,
    transitionsSafeStatus,
    executionSemanticsActiveStatus,
    sessionStableStatus,
    lifecycleBoundedStatus,
    sessionIntegritySafeStatus,
    persistenceGuardedStatus,
    stabilityBoundedStatus,
    driftLowStatus,
    oscillationStableStatus,
    persistenceSafeStatus,
    qualityBoundedStatus,
    redundancyLowStatus,
    qualityDriftSafeStatus,
    executionSignalStableStatus,
    subagentActiveStatus,
    localDelegationStatus,
    fallbackReadyStatus,
    swarmBlockedStatus,
    verifiedExecutionStatus,
    commandGroundedStatus,
    pytestVerifiedStatus,
    gitEvidenceSafeStatus,
    mediationActiveStatus,
    executionBoundedStatus,
    retryGovernedStatus,
    cooldownStableStatus,
    cognitiveLoadStatus,
    attentionFocusStatus,
    cognitiveStateMemoryPressureStatus,
    goalActiveStatus,
    planningBoundedStatus,
    decayTrackedStatus,
    continuationStableStatus,
    reflectionBoundedStatus,
    executionCoherentStatus,
    continuationValidStatus,
    planningStableStatus,
    providerBoundedStatus,
    localFirstStatus,
    fatigueTrackedStatus,
    costGuardedStatus,
    executionMemoryStatus,
    retryMemoryStatus,
    reuseBoundedStatus,
    providerMemoryStatus,
    policyBoundedStatus,
    governanceStablePolicyStatus,
    localFirstPolicyStatus,
    escalationGuardedStatus,
    sprintBoundedStatus,
    validationStableStatus,
    regressionTrackedStatus,
    commitReadyStatus,
    orchestrationBoundedStatus,
    schedulingStableStatus,
    retryOrderedStatus,
    continuationOrderedStatus,
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
    ...registerProviderExperimentalCommands(
      providerExperimental,
      experimentalProviderStatus,
      driftRiskStatus,
      governanceStableStatus,
      benchmarkActiveStatus,
      adaptiveRoutingStatus,
      stableLocalStatus,
      driftAwareRoutingStatus,
      governanceWeightedRoutingStatus,
      fatigueLowStatus,
      fatigueEscalationPressureStatus,
      compactnessDecayStatus,
      recoveryAvailableStatus,
      cognitiveMemoryPressureStatus,
      continuityInflationStatus,
      retrievalBoundedStatus,
      entropyGuardedStatus,
      notifications,
    ),
    ...registerLocalProviderCommands(
      localProvider,
      localProviderReadyStatus,
      ollamaActiveStatus,
      localBudgetOkStatus,
      premiumEscalationStatus,
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
    ...registerDevStrategyCommands(
      devStrategy,
      strategyStableStatus,
      costPressureStatus,
      providerEfficiencyStatus,
      roadmapPressureStatus,
      notifications,
    ),
    ...registerDevPolicyCommands(
      devPolicy,
      policyStableStatus,
      governancePressureStatus,
      escalationPressureStatus,
      realismProtectedStatus,
      notifications,
    ),
    ...registerDevExecutionCommands(
      devExecution,
      executionActiveStatus,
      checkpointReadyStatus,
      validationStableStatus,
      rollbackSafeStatus,
      notifications,
    ),
    ...registerExecutionContinuationCommands(
      executionContinuation,
      executionContinuingStatus,
      continuationSafeStatus,
      loopGuardedStatus,
      boundedExecutionStatus,
      notifications,
    ),
    ...registerExecutionSaturationCommands(
      executionSaturation,
      saturationLowStatus,
      retryStableStatus,
      toolPressureSafeStatus,
      continuationBoundedStatus,
      notifications,
    ),
    ...registerExecutionRecoveryCommands(
      executionRecovery,
      recoverySafeStatus,
      checkpointValidStatus,
      recoveryCooldownStatus,
      rollbackBoundedStatus,
      notifications,
    ),
    ...registerExecutionCoordinationCommands(
      executionCoordination,
      coordinationStableStatus,
      conflictsBoundedStatus,
      runtimePrioritySafeStatus,
      coordinationGuardedStatus,
      notifications,
    ),
    ...registerExecutionIntentCommands(
      executionIntent,
      intentStableStatus,
      priorityBoundedStatus,
      transitionsSafeStatus,
      executionSemanticsActiveStatus,
      notifications,
    ),
    ...registerExecutionSessionCommands(
      executionSession,
      sessionStableStatus,
      lifecycleBoundedStatus,
      sessionIntegritySafeStatus,
      persistenceGuardedStatus,
      notifications,
    ),
    ...registerExecutionStabilityCommands(
      executionStabilityRuntime,
      stabilityBoundedStatus,
      driftLowStatus,
      oscillationStableStatus,
      persistenceSafeStatus,
      notifications,
    ),
    ...registerExecutionQualityCommands(
      executionQuality,
      qualityBoundedStatus,
      redundancyLowStatus,
      qualityDriftSafeStatus,
      executionSignalStableStatus,
      notifications,
    ),
    ...registerSubagentExecutionCommands(
      subagentExecution,
      subagentActiveStatus,
      localDelegationStatus,
      fallbackReadyStatus,
      swarmBlockedStatus,
      notifications,
    ),
    ...registerVerifiedExecutionCommands(
      verifiedExecution,
      verifiedExecutionStatus,
      commandGroundedStatus,
      pytestVerifiedStatus,
      gitEvidenceSafeStatus,
      notifications,
    ),
    ...registerRuntimeMediationCommands(
      runtimeMediation,
      mediationActiveStatus,
      executionBoundedStatus,
      retryGovernedStatus,
      cooldownStableStatus,
      notifications,
    ),
    ...registerCognitiveStateCommands(
      cognitiveState,
      cognitiveLoadStatus,
      attentionFocusStatus,
      cognitiveStateMemoryPressureStatus,
      notifications,
    ),
    ...registerIntentionalPlanningCommands(
      intentionalPlanning,
      goalActiveStatus,
      planningBoundedStatus,
      decayTrackedStatus,
      continuationStableStatus,
      notifications,
    ),
    ...registerReflectiveEvaluationCommands(
      reflectiveEvaluation,
      reflectionBoundedStatus,
      executionCoherentStatus,
      continuationValidStatus,
      planningStableStatus,
      notifications,
    ),
    ...registerAdaptiveProviderCommands(
      adaptiveProvider,
      providerBoundedStatus,
      localFirstStatus,
      fatigueTrackedStatus,
      costGuardedStatus,
      notifications,
    ),
    ...registerExecutionMemoryCommands(
      executionMemory,
      executionMemoryStatus,
      retryMemoryStatus,
      reuseBoundedStatus,
      providerMemoryStatus,
      notifications,
    ),
    ...registerRuntimePolicyCommands(
      runtimePolicy,
      policyBoundedStatus,
      governanceStablePolicyStatus,
      localFirstPolicyStatus,
      escalationGuardedStatus,
      notifications,
    ),
    ...registerSprintLoopCommands(
      sprintLoop,
      sprintBoundedStatus,
      sprintValidationStableStatus,
      regressionTrackedStatus,
      commitReadyStatus,
      notifications,
    ),
    ...registerRuntimeOrchestratorCommands(
      runtimeOrchestrator,
      orchestrationBoundedStatus,
      schedulingStableStatus,
      retryOrderedStatus,
      continuationOrderedStatus,
      notifications,
    ),
  );
}

export function deactivate(): void {
  return;
}
