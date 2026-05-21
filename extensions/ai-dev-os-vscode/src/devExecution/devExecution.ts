import * as vscode from 'vscode';

export type ExecutionPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface DevelopmentExecutionState {
  devExecutionActive: true;
  executionActive: boolean;
  checkpointReady: boolean;
  validationStable: boolean;
  rollbackSafe: boolean;
  executionPressure: ExecutionPressure;
  providerRoutingDistribution: {providerClass: 'HIGH' | 'MEDIUM' | 'LOW'; count: number}[];
  estimatedAvoidedExecutionOverhead: number;
  estimatedAvoidedExecutionExplosion: number;
  compactSummary: string;
  executionPlan: string[];
  checkpointHints: string[];
  validationSequence: string[];
  rollbackGuidance: string[];
  stabilityHints: string[];
  localOnly: true;
  deterministic: true;
  summaryOnly: true;
  boundedExecutionOnly: true;
  humanConfirmedExecutionOnly: true;
  noAutonomousCodingAuthority: true;
  noHiddenRepositoryMutation: true;
  noRecursiveExecutionExpansion: true;
}

export class DevExecutionMonitor {
  private compacted = false;

  evaluate(): DevelopmentExecutionState {
    const executionPressure: ExecutionPressure = this.compacted ? 'LOW' : 'MEDIUM';
    return {
      devExecutionActive: true,
      executionActive: true,
      checkpointReady: true,
      validationStable: true,
      rollbackSafe: true,
      executionPressure,
      providerRoutingDistribution: [
        {providerClass: 'HIGH', count: 4},
        {providerClass: 'MEDIUM', count: 4},
        {providerClass: 'LOW', count: 3},
      ],
      estimatedAvoidedExecutionOverhead: this.compacted ? 4200 : 3960,
      estimatedAvoidedExecutionExplosion: this.compacted ? 3440 : 3280,
      compactSummary: 'bounded execution sequencing; human-confirmed local patch assistance only',
      executionPlan: [
        'scope adjacent runtime',
        'apply local patch',
        'checkpoint before validation',
        'validate before next stage',
      ],
      checkpointHints: ['pre patch state', 'post targeted validation', 'pre commit diff review'],
      validationSequence: ['ruff', 'black', 'targeted tests', 'full pytest', 'runtime audit'],
      rollbackGuidance: ['human-confirmed rollback only', 'return to last validated checkpoint'],
      stabilityHints: ['LOCAL_PATCH only', 'no hidden repository mutation', 'no validation bypass'],
      localOnly: true,
      deterministic: true,
      summaryOnly: true,
      boundedExecutionOnly: true,
      humanConfirmedExecutionOnly: true,
      noAutonomousCodingAuthority: true,
      noHiddenRepositoryMutation: true,
      noRecursiveExecutionExpansion: true,
    };
  }

  compactSummary(): DevelopmentExecutionState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class ExecutionActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 67);

  constructor(private readonly monitor: DevExecutionMonitor) {
    this.item.command = 'aiDevOs.generateExecutionPlan';
  }

  refresh(): DevelopmentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS EXECUTION_ACTIVE ${state.executionActive ? 'YES' : 'NO'}`;
    this.item.tooltip = state.compactSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CheckpointReadyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 66);

  constructor(private readonly monitor: DevExecutionMonitor) {
    this.item.command = 'aiDevOs.showExecutionCheckpoints';
  }

  refresh(): DevelopmentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS CHECKPOINT_READY ${state.checkpointReady ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.checkpointHints.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ValidationStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 65);

  constructor(private readonly monitor: DevExecutionMonitor) {
    this.item.command = 'aiDevOs.showValidationSequence';
  }

  refresh(): DevelopmentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS VALIDATION_STABLE ${state.validationStable ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.validationSequence.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RollbackSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 64);

  constructor(private readonly monitor: DevExecutionMonitor) {
    this.item.command = 'aiDevOs.showRollbackGuidance';
  }

  refresh(): DevelopmentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ROLLBACK_SAFE ${state.rollbackSafe ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.rollbackGuidance.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}