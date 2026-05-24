import * as vscode from 'vscode';
import {registerAdaptiveProviderCommands} from './commands/adaptiveProviderCommands';
import {registerCognitiveStateCommands} from './commands/cognitiveStateCommands';
import {registerContinuousRuntimeAuditCommands} from './commands/continuousRuntimeAuditCommands';
import {registerDevExecutionCommands} from './commands/devExecutionCommands';
import {registerFailureInjectionCommands} from './commands/failureInjectionCommands';
import {registerMainMergeRehearsalCommands} from './commands/mainMergeRehearsalCommands';
import {registerMainMergeQualificationCommands} from './commands/mainMergeQualificationCommands';
import {registerProviderCostStabilizationCommands} from './commands/providerCostStabilizationCommands';
import {registerSoakStabilityCommands} from './commands/soakStabilityCommands';
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
import {registerRuntimeHardeningCommands} from './commands/runtimeHardeningCommands';
import {registerRuntimeMediationCommands} from './commands/runtimeMediationCommands';
import {registerRuntimeOrchestratorCommands} from './commands/runtimeOrchestratorCommands';
import {registerRuntimePolicyCommands} from './commands/runtimePolicyCommands';
import {registerRuntimeSimplificationCommands} from './commands/runtimeSimplificationCommands';
import {registerSessionCommands} from './commands/sessionCommands';
import {registerSprintLoopCommands} from './commands/sprintLoopCommands';
import {registerSprintMemoryCommands} from './commands/sprintMemoryCommands';
import {registerSprintContinuationCommands} from './commands/sprintContinuationCommands';
import {registerSubagentExecutionCommands} from './commands/subagentExecutionCommands';
import {registerStreamingCognitionCommands} from './commands/streamingCognitionCommands';
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
import {
  CommandRegistrationRegistry,
  StatusBarRegistrationRegistry,
} from './registration/registrationRegistry';
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
  ContinuousRuntimeAuditMonitor,
  ContinuousRuntimeHealthStatusBar,
  OrchestrationVisibleStatusBar,
  ProviderVisibleStatusBar,
  RetryVisibleStatusBar,
} from './continuousRuntimeAudit/continuousRuntimeAudit';
import {
  FailureInjectionMonitor,
  FailureTestingStatusBar,
  OrchestrationResilientStatusBar,
  RecoveryStableStatusBar,
  RetryResilientStatusBar,
} from './failureInjection/failureInjection';
import {
  DriftBoundedStatusBar,
  EntropyVisibleStatusBar,
  LongSessionSafeStatusBar,
  SoakStabilityMonitor,
  SoakStableStatusBar,
} from './soakStability/soakStability';
import {
  CostStableStatusBar,
  FrontierBoundedStatusBar,
  LocalFirstEfficiencyStatusBar,
  OverheadFlatStatusBar,
  ProviderCostStabilizationMonitor,
} from './providerCostStabilization/providerCostStabilization';
import {
  GovernanceCompleteStatusBar,
  MainMergeQualificationMonitor,
  MergeReadyStatusBar,
  QualificationValidationStableStatusBar,
  RiskBoundedStatusBar,
} from './mainMergeQualification/mainMergeQualification';
import {
  CIReadyStatusBar,
  MainMergeRehearsalMonitor,
  MergeRehearsedStatusBar,
  PostMergeSafeStatusBar,
  RollbackReadyStatusBar,
} from './mainMergeRehearsal/mainMergeRehearsal';
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
  EscalationStableStatusBar,
  HardeningActiveStatusBar,
  OrchestrationSafeStatusBar,
  RetryStableHardeningStatusBar,
  RuntimeHardeningMonitor,
} from './runtimeHardening/runtimeHardening';
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
  BacklogStableStatusBar,
  ContinuationReadyStatusBar,
  DependencyStableStatusBar,
  RegressionVisibleStatusBar,
  SprintContinuationMonitor,
} from './sprintContinuation/sprintContinuation';
import {
  FallbackReadyStatusBar,
  LocalDelegationStatusBar,
  SubagentActiveStatusBar,
  SubagentExecutionMonitor,
  SwarmBlockedStatusBar,
} from './subagentExecution/subagentExecution';
import {
  ContinuationStreamingStatusBar,
  InterruptionSafeStatusBar,
  ProviderStreamingStatusBar,
  StreamingActiveStatusBar,
  StreamingCognitionMonitor,
} from './streamingCognition/streamingCognition';
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
  const sprintContinuation = new SprintContinuationMonitor();
  const continuationReadyStatus = new ContinuationReadyStatusBar(sprintContinuation);
  const backlogStableStatus = new BacklogStableStatusBar(sprintContinuation);
  const dependencyStableStatus = new DependencyStableStatusBar(sprintContinuation);
  const regressionVisibleStatus = new RegressionVisibleStatusBar(sprintContinuation);
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
  const streamingCognition = new StreamingCognitionMonitor();
  const streamingActiveStatus = new StreamingActiveStatusBar(streamingCognition);
  const interruptionSafeStatus = new InterruptionSafeStatusBar(streamingCognition);
  const providerStreamingStatus = new ProviderStreamingStatusBar(streamingCognition);
  const continuationStreamingStatus = new ContinuationStreamingStatusBar(streamingCognition);
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
  const runtimeHardening = new RuntimeHardeningMonitor();
  const hardeningActiveStatus = new HardeningActiveStatusBar(runtimeHardening);
  const retryStableHardeningStatus = new RetryStableHardeningStatusBar(runtimeHardening);
  const orchestrationSafeStatus = new OrchestrationSafeStatusBar(runtimeHardening);
  const escalationStableStatus = new EscalationStableStatusBar(runtimeHardening);
  const continuousRuntimeAudit = new ContinuousRuntimeAuditMonitor();
  const continuousRuntimeHealthStatus = new ContinuousRuntimeHealthStatusBar(continuousRuntimeAudit);
  const retryVisibleStatus = new RetryVisibleStatusBar(continuousRuntimeAudit);
  const orchestrationVisibleStatus = new OrchestrationVisibleStatusBar(continuousRuntimeAudit);
  const providerVisibleStatus = new ProviderVisibleStatusBar(continuousRuntimeAudit);
  const failureInjection = new FailureInjectionMonitor();
  const failureTestingStatus = new FailureTestingStatusBar(failureInjection);
  const recoveryStableStatus = new RecoveryStableStatusBar(failureInjection);
  const retryResilientStatus = new RetryResilientStatusBar(failureInjection);
  const orchestrationResilientStatus = new OrchestrationResilientStatusBar(failureInjection);
  const soakStability = new SoakStabilityMonitor();
  const soakStableStatus = new SoakStableStatusBar(soakStability);
  const driftBoundedStatus = new DriftBoundedStatusBar(soakStability);
  const entropyVisibleStatus = new EntropyVisibleStatusBar(soakStability);
  const longSessionSafeStatus = new LongSessionSafeStatusBar(soakStability);
  const providerCostStabilization = new ProviderCostStabilizationMonitor();
  const costStableStatus = new CostStableStatusBar(providerCostStabilization);
  const frontierBoundedStatus = new FrontierBoundedStatusBar(providerCostStabilization);
  const localFirstEfficiencyStatus = new LocalFirstEfficiencyStatusBar(providerCostStabilization);
  const overheadFlatStatus = new OverheadFlatStatusBar(providerCostStabilization);
  const mainMergeQualification = new MainMergeQualificationMonitor();
  const mergeReadyStatus = new MergeReadyStatusBar(mainMergeQualification);
  const governanceCompleteStatus = new GovernanceCompleteStatusBar(mainMergeQualification);
  const validationStableQualificationStatus = new QualificationValidationStableStatusBar(mainMergeQualification);
  const riskBoundedStatus = new RiskBoundedStatusBar(mainMergeQualification);
  const mainMergeRehearsal = new MainMergeRehearsalMonitor();
  const mergeRehearsedStatus = new MergeRehearsedStatusBar(mainMergeRehearsal);
  const rollbackReadyRehearsalStatus = new RollbackReadyStatusBar(mainMergeRehearsal);
  const postMergeSafeStatus = new PostMergeSafeStatusBar(mainMergeRehearsal);
  const ciReadyStatus = new CIReadyStatusBar(mainMergeRehearsal);
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
  const sprintContinuationState = continuationReadyStatus.refresh();
  backlogStableStatus.refresh();
  dependencyStableStatus.refresh();
  regressionVisibleStatus.refresh();
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
  const streamingState = streamingActiveStatus.refresh();
  interruptionSafeStatus.refresh();
  providerStreamingStatus.refresh();
  continuationStreamingStatus.refresh();
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
  hardeningActiveStatus.refresh();
  retryStableHardeningStatus.refresh();
  orchestrationSafeStatus.refresh();
  escalationStableStatus.refresh();
  continuousRuntimeHealthStatus.refresh();
  retryVisibleStatus.refresh();
  orchestrationVisibleStatus.refresh();
  providerVisibleStatus.refresh();
  failureTestingStatus.refresh();
  recoveryStableStatus.refresh();
  retryResilientStatus.refresh();
  orchestrationResilientStatus.refresh();
  soakStableStatus.refresh();
  driftBoundedStatus.refresh();
  entropyVisibleStatus.refresh();
  longSessionSafeStatus.refresh();
  costStableStatus.refresh();
  frontierBoundedStatus.refresh();
  localFirstEfficiencyStatus.refresh();
  overheadFlatStatus.refresh();
  mergeReadyStatus.refresh();
  governanceCompleteStatus.refresh();
  validationStableQualificationStatus.refresh();
  riskBoundedStatus.refresh();
  mergeRehearsedStatus.refresh();
  rollbackReadyRehearsalStatus.refresh();
  postMergeSafeStatus.refresh();
  ciReadyStatus.refresh();
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
  if (sprintContinuationState.continuationPressure === 'HIGH') {
    await notifications.warn(
      'startup-sprint-continuation-pressure-warning',
      'AI_DEV_OS sprint continuation pressure is high. Compact continuation summary before chaining.',
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
  if (streamingState.streamingPressure === 'HIGH') {
    await notifications.warn(
      'startup-streaming-cognition-pressure-warning',
      'AI_DEV_OS streaming cognition pressure is high. Compact streaming summary before realtime continuation.',
    );
  }
  if (!subagentState.swarmBlocked || !subagentState.fallbackReady) {
    await notifications.warn(
      'startup-subagent-execution-warning',
      'AI_DEV_OS subagent delegation is not bounded. Compact delegation summary before continuing.',
    );
  }
  const commandRegistry = new CommandRegistrationRegistry();
  const earlyCommands = commandRegistry.register([
    {order: 10, namespace: 'session', commandIds: ['aiDevOs.sessionAudit', 'aiDevOs.generateHandoff', 'aiDevOs.copyContinuityBundle', 'aiDevOs.openNewSessionPrompt', 'aiDevOs.confirmSessionRollover', 'aiDevOs.showSessionBoundaryState', 'aiDevOs.startNewSprintSession', 'aiDevOs.openBootstrapChat', 'aiDevOs.previewBootstrapDraft', 'aiDevOs.retryDraftInjection', 'aiDevOs.showEnterOnlyState', 'aiDevOs.checkPrefillSupport', 'aiDevOs.retryCopilotInjection', 'aiDevOs.showPrefillStatus', 'aiDevOs.showClipboardFallback', 'aiDevOs.compactCurrentSession', 'aiDevOs.showStaleSessionWarning'], register: () => registerSessionCommands(context, store, notifications, view)},
    {order: 20, namespace: 'persistence', commandIds: ['aiDevOs.restoreSessionState', 'aiDevOs.showPersistenceState', 'aiDevOs.cleanupStalePersistence', 'aiDevOs.exportLocalContinuityIndex', 'aiDevOs.resetLocalSessionState'], register: () => registerPersistenceCommands(store, persistence, notifications, view)},
    {order: 30, namespace: 'governance', commandIds: ['aiDevOs.showPersistenceBudget', 'aiDevOs.rotateCheckpoints'], register: () => registerGovernanceCommands(persistence, governance, notifications, view)},
  ]);
  const commandProjection = commandRegistry.snapshot();
  if (commandProjection.conflicts.length > 0) {
    await notifications.warn(
      'registration-command-conflict-warning',
      'AI_DEV_OS extension command registration conflict detected. Duplicate registrations were skipped.',
    );
  }
  const statusRegistry = new StatusBarRegistrationRegistry();
  const boundedStatusBars = statusRegistry.register([
    {order: 10, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_STATUS', disposable: governanceStatus},
    {order: 11, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_TREND_STATUS', disposable: governanceTrendStatus},
    {order: 12, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_CORE_STATUS', disposable: governanceCoreStatus},
    {order: 13, namespace: 'activation.status', statusId: 'AI_DEV_OS ARCHITECTURE_STATUS', disposable: architectureStatus},
    {order: 14, namespace: 'activation.status', statusId: 'AI_DEV_OS SIMPLIFICATION_STATUS', disposable: simplificationStatus},
    {order: 15, namespace: 'activation.status', statusId: 'AI_DEV_OS PRESENCE_STATUS', disposable: presenceStatus},
    {order: 16, namespace: 'activation.status', statusId: 'AI_DEV_OS HEARTBEAT_STATUS', disposable: heartbeatStatus},
    {order: 17, namespace: 'activation.status', statusId: 'AI_DEV_OS REASONING_STATUS', disposable: reasoningStatus},
    {order: 18, namespace: 'activation.status', statusId: 'AI_DEV_OS REASONING_SCOPE_STATUS', disposable: reasoningScopeStatus},
    {order: 19, namespace: 'activation.status', statusId: 'AI_DEV_OS COMPACT_REPORTING_STATUS', disposable: compactReportingStatus},
    {order: 20, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRIEVAL_BUDGET_STATUS', disposable: retrievalBudgetStatus},
    {order: 21, namespace: 'activation.status', statusId: 'AI_DEV_OS INCREMENTAL_CONTEXT_STATUS', disposable: incrementalContextStatus},
    {order: 22, namespace: 'activation.status', statusId: 'AI_DEV_OS PREMIUM_PROVIDER_STATUS', disposable: premiumProviderStatus},
    {order: 23, namespace: 'activation.status', statusId: 'AI_DEV_OS PROVIDER_DOWNGRADE_STATUS', disposable: providerDowngradeStatus},
    {order: 24, namespace: 'activation.status', statusId: 'AI_DEV_OS PROVIDER_PRESSURE_STATUS', disposable: providerPressureStatus},
    {order: 25, namespace: 'activation.status', statusId: 'AI_DEV_OS EXPERIMENTAL_PROVIDER_STATUS', disposable: experimentalProviderStatus},
    {order: 26, namespace: 'activation.status', statusId: 'AI_DEV_OS DRIFT_RISK_STATUS', disposable: driftRiskStatus},
    {order: 27, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_STABLE_STATUS', disposable: governanceStableStatus},
    {order: 28, namespace: 'activation.status', statusId: 'AI_DEV_OS BENCHMARK_ACTIVE_STATUS', disposable: benchmarkActiveStatus},
    {order: 29, namespace: 'activation.status', statusId: 'AI_DEV_OS ADAPTIVE_ROUTING_STATUS', disposable: adaptiveRoutingStatus},
    {order: 30, namespace: 'activation.status', statusId: 'AI_DEV_OS STABLE_LOCAL_STATUS', disposable: stableLocalStatus},
    {order: 31, namespace: 'activation.status', statusId: 'AI_DEV_OS DRIFT_AWARE_ROUTING_STATUS', disposable: driftAwareRoutingStatus},
    {order: 32, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_WEIGHTED_ROUTING_STATUS', disposable: governanceWeightedRoutingStatus},
    {order: 33, namespace: 'activation.status', statusId: 'AI_DEV_OS FATIGUE_LOW_STATUS', disposable: fatigueLowStatus},
    {order: 34, namespace: 'activation.status', statusId: 'AI_DEV_OS FATIGUE_ESCALATION_PRESSURE_STATUS', disposable: fatigueEscalationPressureStatus},
    {order: 35, namespace: 'activation.status', statusId: 'AI_DEV_OS COMPACTNESS_DECAY_STATUS', disposable: compactnessDecayStatus},
    {order: 36, namespace: 'activation.status', statusId: 'AI_DEV_OS RECOVERY_AVAILABLE_STATUS', disposable: recoveryAvailableStatus},
    {order: 37, namespace: 'activation.status', statusId: 'AI_DEV_OS COGNITIVE_MEMORY_PRESSURE_STATUS', disposable: cognitiveMemoryPressureStatus},
    {order: 38, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUITY_INFLATION_STATUS', disposable: continuityInflationStatus},
    {order: 39, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRIEVAL_BOUNDED_STATUS', disposable: retrievalBoundedStatus},
    {order: 40, namespace: 'activation.status', statusId: 'AI_DEV_OS ENTROPY_GUARDED_STATUS', disposable: entropyGuardedStatus},
    {order: 41, namespace: 'activation.status', statusId: 'AI_DEV_OS LOCAL_PROVIDER_READY_STATUS', disposable: localProviderReadyStatus},
    {order: 42, namespace: 'activation.status', statusId: 'AI_DEV_OS OLLAMA_ACTIVE_STATUS', disposable: ollamaActiveStatus},
    {order: 43, namespace: 'activation.status', statusId: 'AI_DEV_OS LOCAL_BUDGET_OK_STATUS', disposable: localBudgetOkStatus},
    {order: 44, namespace: 'activation.status', statusId: 'AI_DEV_OS PREMIUM_ESCALATION_STATUS', disposable: premiumEscalationStatus},
    {order: 45, namespace: 'activation.status', statusId: 'AI_DEV_OS SPRINT_ACTIVE_STATUS', disposable: sprintActiveStatus},
    {order: 46, namespace: 'activation.status', statusId: 'AI_DEV_OS SPRINT_ROLLOVER_STATUS', disposable: sprintRolloverStatus},
    {order: 47, namespace: 'activation.status', statusId: 'AI_DEV_OS SPRINT_PRESSURE_STATUS', disposable: sprintPressureStatus},
    {order: 48, namespace: 'activation.status', statusId: 'AI_DEV_OS LOCAL_PATCH_REQUIRED_STATUS', disposable: localPatchRequiredStatus},
    {order: 49, namespace: 'activation.status', statusId: 'AI_DEV_OS SPRINT_MEMORY_STATUS', disposable: sprintMemoryStatus},
    {order: 50, namespace: 'activation.status', statusId: 'AI_DEV_OS MEMORY_PRESSURE_STATUS', disposable: memoryPressureStatus},
    {order: 51, namespace: 'activation.status', statusId: 'AI_DEV_OS PATTERN_STABLE_STATUS', disposable: patternStableStatus},
    {order: 52, namespace: 'activation.status', statusId: 'AI_DEV_OS MEMORY_EVICTION_STATUS', disposable: memoryEvictionStatus},
    {order: 53, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUATION_READY_STATUS', disposable: continuationReadyStatus},
    {order: 54, namespace: 'activation.status', statusId: 'AI_DEV_OS BACKLOG_STABLE_STATUS', disposable: backlogStableStatus},
    {order: 55, namespace: 'activation.status', statusId: 'AI_DEV_OS DEPENDENCY_STABLE_STATUS', disposable: dependencyStableStatus},
    {order: 56, namespace: 'activation.status', statusId: 'AI_DEV_OS REGRESSION_VISIBLE_STATUS', disposable: regressionVisibleStatus},
    {order: 57, namespace: 'activation.status', statusId: 'AI_DEV_OS STRATEGY_STABLE_STATUS', disposable: strategyStableStatus},
    {order: 58, namespace: 'activation.status', statusId: 'AI_DEV_OS COST_PRESSURE_STATUS', disposable: costPressureStatus},
    {order: 59, namespace: 'activation.status', statusId: 'AI_DEV_OS PROVIDER_EFFICIENCY_STATUS', disposable: providerEfficiencyStatus},
    {order: 60, namespace: 'activation.status', statusId: 'AI_DEV_OS ROADMAP_PRESSURE_STATUS', disposable: roadmapPressureStatus},
    {order: 61, namespace: 'activation.status', statusId: 'AI_DEV_OS POLICY_STABLE_STATUS', disposable: policyStableStatus},
    {order: 62, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_PRESSURE_STATUS', disposable: governancePressureStatus},
    {order: 63, namespace: 'activation.status', statusId: 'AI_DEV_OS ESCALATION_PRESSURE_STATUS', disposable: escalationPressureStatus},
    {order: 64, namespace: 'activation.status', statusId: 'AI_DEV_OS REALISM_PROTECTED_STATUS', disposable: realismProtectedStatus},
    {order: 65, namespace: 'activation.status', statusId: 'AI_DEV_OS EXECUTION_ACTIVE_STATUS', disposable: executionActiveStatus},
    {order: 66, namespace: 'activation.status', statusId: 'AI_DEV_OS CHECKPOINT_READY_STATUS', disposable: checkpointReadyStatus},
    {order: 67, namespace: 'activation.status', statusId: 'AI_DEV_OS SPRINT_VALIDATION_STABLE_STATUS', disposable: sprintValidationStableStatus},
    {order: 68, namespace: 'activation.status', statusId: 'AI_DEV_OS ROLLBACK_SAFE_STATUS', disposable: rollbackSafeStatus},
    {order: 69, namespace: 'activation.status', statusId: 'AI_DEV_OS EXECUTION_CONTINUING_STATUS', disposable: executionContinuingStatus},
    {order: 70, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUATION_SAFE_STATUS', disposable: continuationSafeStatus},
    {order: 71, namespace: 'activation.status', statusId: 'AI_DEV_OS LOOP_GUARDED_STATUS', disposable: loopGuardedStatus},
    {order: 72, namespace: 'activation.status', statusId: 'AI_DEV_OS BOUNDED_EXECUTION_STATUS', disposable: boundedExecutionStatus},
    {order: 73, namespace: 'activation.status', statusId: 'AI_DEV_OS SATURATION_LOW_STATUS', disposable: saturationLowStatus},
    {order: 74, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRY_STABLE_STATUS', disposable: retryStableStatus},
    {order: 75, namespace: 'activation.status', statusId: 'AI_DEV_OS TOOL_PRESSURE_SAFE_STATUS', disposable: toolPressureSafeStatus},
    {order: 76, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUATION_BOUNDED_STATUS', disposable: continuationBoundedStatus},
    {order: 77, namespace: 'activation.status', statusId: 'AI_DEV_OS RECOVERY_SAFE_STATUS', disposable: recoverySafeStatus},
    {order: 78, namespace: 'activation.status', statusId: 'AI_DEV_OS CHECKPOINT_VALID_STATUS', disposable: checkpointValidStatus},
    {order: 79, namespace: 'activation.status', statusId: 'AI_DEV_OS RECOVERY_COOLDOWN_STATUS', disposable: recoveryCooldownStatus},
    {order: 80, namespace: 'activation.status', statusId: 'AI_DEV_OS ROLLBACK_BOUNDED_STATUS', disposable: rollbackBoundedStatus},
    {order: 81, namespace: 'activation.status', statusId: 'AI_DEV_OS COORDINATION_STABLE_STATUS', disposable: coordinationStableStatus},
    {order: 82, namespace: 'activation.status', statusId: 'AI_DEV_OS CONFLICTS_BOUNDED_STATUS', disposable: conflictsBoundedStatus},
    {order: 83, namespace: 'activation.status', statusId: 'AI_DEV_OS RUNTIME_PRIORITY_SAFE_STATUS', disposable: runtimePrioritySafeStatus},
    {order: 84, namespace: 'activation.status', statusId: 'AI_DEV_OS COORDINATION_GUARDED_STATUS', disposable: coordinationGuardedStatus},
    {order: 85, namespace: 'activation.status', statusId: 'AI_DEV_OS INTENT_STABLE_STATUS', disposable: intentStableStatus},
    {order: 86, namespace: 'activation.status', statusId: 'AI_DEV_OS PRIORITY_BOUNDED_STATUS', disposable: priorityBoundedStatus},
    {order: 87, namespace: 'activation.status', statusId: 'AI_DEV_OS TRANSITIONS_SAFE_STATUS', disposable: transitionsSafeStatus},
    {order: 88, namespace: 'activation.status', statusId: 'AI_DEV_OS EXECUTION_SEMANTICS_ACTIVE_STATUS', disposable: executionSemanticsActiveStatus},
    {order: 89, namespace: 'activation.status', statusId: 'AI_DEV_OS SESSION_STABLE_STATUS', disposable: sessionStableStatus},
    {order: 90, namespace: 'activation.status', statusId: 'AI_DEV_OS LIFECYCLE_BOUNDED_STATUS', disposable: lifecycleBoundedStatus},
    {order: 91, namespace: 'activation.status', statusId: 'AI_DEV_OS SESSION_INTEGRITY_SAFE_STATUS', disposable: sessionIntegritySafeStatus},
    {order: 92, namespace: 'activation.status', statusId: 'AI_DEV_OS PERSISTENCE_GUARDED_STATUS', disposable: persistenceGuardedStatus},
    {order: 93, namespace: 'activation.status', statusId: 'AI_DEV_OS STABILITY_BOUNDED_STATUS', disposable: stabilityBoundedStatus},
    {order: 94, namespace: 'activation.status', statusId: 'AI_DEV_OS DRIFT_LOW_STATUS', disposable: driftLowStatus},
    {order: 95, namespace: 'activation.status', statusId: 'AI_DEV_OS OSCILLATION_STABLE_STATUS', disposable: oscillationStableStatus},
    {order: 96, namespace: 'activation.status', statusId: 'AI_DEV_OS PERSISTENCE_SAFE_STATUS', disposable: persistenceSafeStatus},
    {order: 97, namespace: 'activation.status', statusId: 'AI_DEV_OS QUALITY_BOUNDED_STATUS', disposable: qualityBoundedStatus},
    {order: 98, namespace: 'activation.status', statusId: 'AI_DEV_OS REDUNDANCY_LOW_STATUS', disposable: redundancyLowStatus},
    {order: 99, namespace: 'activation.status', statusId: 'AI_DEV_OS QUALITY_DRIFT_SAFE_STATUS', disposable: qualityDriftSafeStatus},
    {order: 100, namespace: 'activation.status', statusId: 'AI_DEV_OS EXECUTION_SIGNAL_STABLE_STATUS', disposable: executionSignalStableStatus},
    {order: 101, namespace: 'activation.status', statusId: 'AI_DEV_OS SUBAGENT_ACTIVE_STATUS', disposable: subagentActiveStatus},
    {order: 102, namespace: 'activation.status', statusId: 'AI_DEV_OS LOCAL_DELEGATION_STATUS', disposable: localDelegationStatus},
    {order: 103, namespace: 'activation.status', statusId: 'AI_DEV_OS FALLBACK_READY_STATUS', disposable: fallbackReadyStatus},
    {order: 104, namespace: 'activation.status', statusId: 'AI_DEV_OS SWARM_BLOCKED_STATUS', disposable: swarmBlockedStatus},
    {order: 105, namespace: 'activation.status', statusId: 'AI_DEV_OS VERIFIED_EXECUTION_STATUS', disposable: verifiedExecutionStatus},
    {order: 106, namespace: 'activation.status', statusId: 'AI_DEV_OS COMMAND_GROUNDED_STATUS', disposable: commandGroundedStatus},
    {order: 107, namespace: 'activation.status', statusId: 'AI_DEV_OS PYTEST_VERIFIED_STATUS', disposable: pytestVerifiedStatus},
    {order: 108, namespace: 'activation.status', statusId: 'AI_DEV_OS GIT_EVIDENCE_SAFE_STATUS', disposable: gitEvidenceSafeStatus},
    {order: 109, namespace: 'activation.status', statusId: 'AI_DEV_OS MEDIATION_ACTIVE_STATUS', disposable: mediationActiveStatus},
    {order: 110, namespace: 'activation.status', statusId: 'AI_DEV_OS EXECUTION_BOUNDED_STATUS', disposable: executionBoundedStatus},
    {order: 111, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRY_GOVERNED_STATUS', disposable: retryGovernedStatus},
    {order: 112, namespace: 'activation.status', statusId: 'AI_DEV_OS COOLDOWN_STABLE_STATUS', disposable: cooldownStableStatus},
    {order: 113, namespace: 'activation.status', statusId: 'AI_DEV_OS COGNITIVE_LOAD_STATUS', disposable: cognitiveLoadStatus},
    {order: 114, namespace: 'activation.status', statusId: 'AI_DEV_OS ATTENTION_FOCUS_STATUS', disposable: attentionFocusStatus},
    {order: 115, namespace: 'activation.status', statusId: 'AI_DEV_OS COGNITIVE_STATE_MEMORY_PRESSURE_STATUS', disposable: cognitiveStateMemoryPressureStatus},
    {order: 116, namespace: 'activation.status', statusId: 'AI_DEV_OS GOAL_ACTIVE_STATUS', disposable: goalActiveStatus},
    {order: 117, namespace: 'activation.status', statusId: 'AI_DEV_OS PLANNING_BOUNDED_STATUS', disposable: planningBoundedStatus},
    {order: 118, namespace: 'activation.status', statusId: 'AI_DEV_OS DECAY_TRACKED_STATUS', disposable: decayTrackedStatus},
    {order: 119, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUATION_STABLE_STATUS', disposable: continuationStableStatus},
    {order: 120, namespace: 'activation.status', statusId: 'AI_DEV_OS REFLECTION_BOUNDED_STATUS', disposable: reflectionBoundedStatus},
    {order: 121, namespace: 'activation.status', statusId: 'AI_DEV_OS EXECUTION_COHERENT_STATUS', disposable: executionCoherentStatus},
    {order: 122, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUATION_VALID_STATUS', disposable: continuationValidStatus},
    {order: 123, namespace: 'activation.status', statusId: 'AI_DEV_OS PLANNING_STABLE_STATUS', disposable: planningStableStatus},
    {order: 124, namespace: 'activation.status', statusId: 'AI_DEV_OS PROVIDER_BOUNDED_STATUS', disposable: providerBoundedStatus},
    {order: 125, namespace: 'activation.status', statusId: 'AI_DEV_OS LOCAL_FIRST_STATUS', disposable: localFirstStatus},
    {order: 126, namespace: 'activation.status', statusId: 'AI_DEV_OS FATIGUE_TRACKED_STATUS', disposable: fatigueTrackedStatus},
    {order: 127, namespace: 'activation.status', statusId: 'AI_DEV_OS COST_GUARDED_STATUS', disposable: costGuardedStatus},
    {order: 128, namespace: 'activation.status', statusId: 'AI_DEV_OS EXECUTION_MEMORY_STATUS', disposable: executionMemoryStatus},
    {order: 129, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRY_MEMORY_STATUS', disposable: retryMemoryStatus},
    {order: 130, namespace: 'activation.status', statusId: 'AI_DEV_OS REUSE_BOUNDED_STATUS', disposable: reuseBoundedStatus},
    {order: 131, namespace: 'activation.status', statusId: 'AI_DEV_OS PROVIDER_MEMORY_STATUS', disposable: providerMemoryStatus},
    {order: 132, namespace: 'activation.status', statusId: 'AI_DEV_OS POLICY_BOUNDED_STATUS', disposable: policyBoundedStatus},
    {order: 133, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_STABLE_POLICY_STATUS', disposable: governanceStablePolicyStatus},
    {order: 134, namespace: 'activation.status', statusId: 'AI_DEV_OS LOCAL_FIRST_POLICY_STATUS', disposable: localFirstPolicyStatus},
    {order: 135, namespace: 'activation.status', statusId: 'AI_DEV_OS ESCALATION_GUARDED_STATUS', disposable: escalationGuardedStatus},
    {order: 136, namespace: 'activation.status', statusId: 'AI_DEV_OS SPRINT_BOUNDED_STATUS', disposable: sprintBoundedStatus},
    {order: 137, namespace: 'activation.status', statusId: 'AI_DEV_OS VALIDATION_STABLE_STATUS', disposable: validationStableStatus},
    {order: 138, namespace: 'activation.status', statusId: 'AI_DEV_OS REGRESSION_TRACKED_STATUS', disposable: regressionTrackedStatus},
    {order: 139, namespace: 'activation.status', statusId: 'AI_DEV_OS COMMIT_READY_STATUS', disposable: commitReadyStatus},
    {order: 140, namespace: 'activation.status', statusId: 'AI_DEV_OS ORCHESTRATION_BOUNDED_STATUS', disposable: orchestrationBoundedStatus},
    {order: 141, namespace: 'activation.status', statusId: 'AI_DEV_OS SCHEDULING_STABLE_STATUS', disposable: schedulingStableStatus},
    {order: 142, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRY_ORDERED_STATUS', disposable: retryOrderedStatus},
    {order: 143, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUATION_ORDERED_STATUS', disposable: continuationOrderedStatus},
    {order: 144, namespace: 'activation.status', statusId: 'AI_DEV_OS HARDENING_ACTIVE_STATUS', disposable: hardeningActiveStatus},
    {order: 145, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRY_STABLE_HARDENING_STATUS', disposable: retryStableHardeningStatus},
    {order: 146, namespace: 'activation.status', statusId: 'AI_DEV_OS ORCHESTRATION_SAFE_STATUS', disposable: orchestrationSafeStatus},
    {order: 147, namespace: 'activation.status', statusId: 'AI_DEV_OS ESCALATION_STABLE_STATUS', disposable: escalationStableStatus},
    {order: 148, namespace: 'activation.status', statusId: 'AI_DEV_OS CONTINUOUS_RUNTIME_HEALTH_STATUS', disposable: continuousRuntimeHealthStatus},
    {order: 149, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRY_VISIBLE_STATUS', disposable: retryVisibleStatus},
    {order: 150, namespace: 'activation.status', statusId: 'AI_DEV_OS ORCHESTRATION_VISIBLE_STATUS', disposable: orchestrationVisibleStatus},
    {order: 151, namespace: 'activation.status', statusId: 'AI_DEV_OS PROVIDER_VISIBLE_STATUS', disposable: providerVisibleStatus},
    {order: 152, namespace: 'activation.status', statusId: 'AI_DEV_OS FAILURE_TESTING_STATUS', disposable: failureTestingStatus},
    {order: 153, namespace: 'activation.status', statusId: 'AI_DEV_OS RECOVERY_STABLE_STATUS', disposable: recoveryStableStatus},
    {order: 154, namespace: 'activation.status', statusId: 'AI_DEV_OS RETRY_RESILIENT_STATUS', disposable: retryResilientStatus},
    {order: 155, namespace: 'activation.status', statusId: 'AI_DEV_OS ORCHESTRATION_RESILIENT_STATUS', disposable: orchestrationResilientStatus},
    {order: 156, namespace: 'activation.status', statusId: 'AI_DEV_OS SOAK_STABLE_STATUS', disposable: soakStableStatus},
    {order: 157, namespace: 'activation.status', statusId: 'AI_DEV_OS DRIFT_BOUNDED_STATUS', disposable: driftBoundedStatus},
    {order: 158, namespace: 'activation.status', statusId: 'AI_DEV_OS ENTROPY_VISIBLE_STATUS', disposable: entropyVisibleStatus},
    {order: 159, namespace: 'activation.status', statusId: 'AI_DEV_OS LONG_SESSION_SAFE_STATUS', disposable: longSessionSafeStatus},
    {order: 160, namespace: 'activation.status', statusId: 'AI_DEV_OS COST_STABLE_STATUS', disposable: costStableStatus},
    {order: 161, namespace: 'activation.status', statusId: 'AI_DEV_OS FRONTIER_BOUNDED_STATUS', disposable: frontierBoundedStatus},
    {order: 162, namespace: 'activation.status', statusId: 'AI_DEV_OS LOCAL_FIRST_EFFICIENCY_STATUS', disposable: localFirstEfficiencyStatus},
    {order: 163, namespace: 'activation.status', statusId: 'AI_DEV_OS OVERHEAD_FLAT_STATUS', disposable: overheadFlatStatus},
    {order: 164, namespace: 'activation.status', statusId: 'AI_DEV_OS MERGE_READY_STATUS', disposable: mergeReadyStatus},
    {order: 165, namespace: 'activation.status', statusId: 'AI_DEV_OS GOVERNANCE_COMPLETE_STATUS', disposable: governanceCompleteStatus},
    {order: 166, namespace: 'activation.status', statusId: 'AI_DEV_OS VALIDATION_STABLE_QUALIFICATION_STATUS', disposable: validationStableQualificationStatus},
    {order: 167, namespace: 'activation.status', statusId: 'AI_DEV_OS RISK_BOUNDED_STATUS', disposable: riskBoundedStatus},
    {order: 168, namespace: 'activation.status', statusId: 'AI_DEV_OS MERGE_REHEARSED_STATUS', disposable: mergeRehearsedStatus},
    {order: 169, namespace: 'activation.status', statusId: 'AI_DEV_OS ROLLBACK_READY_REHEARSAL_STATUS', disposable: rollbackReadyRehearsalStatus},
    {order: 170, namespace: 'activation.status', statusId: 'AI_DEV_OS POST_MERGE_SAFE_STATUS', disposable: postMergeSafeStatus},
    {order: 171, namespace: 'activation.status', statusId: 'AI_DEV_OS CI_READY_STATUS', disposable: ciReadyStatus},
  ]);
  const statusProjection = statusRegistry.snapshot();
  if (statusProjection.conflicts.length > 0) {
    await notifications.warn(
      'registration-status-conflict-warning',
      'AI_DEV_OS extension status registration conflict detected. Duplicate status bars were skipped.',
    );
  }
  const treeDataProviders = [
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
  ];
  context.subscriptions.push(
    ...treeDataProviders,
    ...boundedStatusBars,
    ...earlyCommands,
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
    ...registerSprintContinuationCommands(
      sprintContinuation,
      continuationReadyStatus,
      backlogStableStatus,
      dependencyStableStatus,
      regressionVisibleStatus,
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
    ...registerStreamingCognitionCommands(
      streamingCognition,
      streamingActiveStatus,
      interruptionSafeStatus,
      providerStreamingStatus,
      continuationStreamingStatus,
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
    ...registerRuntimeHardeningCommands(
      runtimeHardening,
      hardeningActiveStatus,
      retryStableHardeningStatus,
      orchestrationSafeStatus,
      escalationStableStatus,
      notifications,
    ),
    ...registerContinuousRuntimeAuditCommands(
      continuousRuntimeAudit,
      continuousRuntimeHealthStatus,
      retryVisibleStatus,
      orchestrationVisibleStatus,
      providerVisibleStatus,
      notifications,
    ),
    ...registerFailureInjectionCommands(
      failureInjection,
      failureTestingStatus,
      recoveryStableStatus,
      retryResilientStatus,
      orchestrationResilientStatus,
      notifications,
    ),
    ...registerSoakStabilityCommands(
      soakStability,
      soakStableStatus,
      driftBoundedStatus,
      entropyVisibleStatus,
      longSessionSafeStatus,
      notifications,
    ),
    ...registerProviderCostStabilizationCommands(
      providerCostStabilization,
      costStableStatus,
      frontierBoundedStatus,
      localFirstEfficiencyStatus,
      overheadFlatStatus,
      notifications,
    ),
    ...registerMainMergeQualificationCommands(
      mainMergeQualification,
      mergeReadyStatus,
      governanceCompleteStatus,
      validationStableQualificationStatus,
      riskBoundedStatus,
      notifications,
    ),
    ...registerMainMergeRehearsalCommands(
      mainMergeRehearsal,
      mergeRehearsedStatus,
      rollbackReadyRehearsalStatus,
      postMergeSafeStatus,
      ciReadyStatus,
      notifications,
    ),
  );
}

export function deactivate(): void {
  return;
}
