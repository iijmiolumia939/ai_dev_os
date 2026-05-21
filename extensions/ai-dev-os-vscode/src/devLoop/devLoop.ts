import * as vscode from 'vscode';

export type SprintPressure = 'LOW' | 'MEDIUM' | 'HIGH';
export type SprintLifecycleState = 'PLANNING' | 'ACTIVE' | 'VALIDATING' | 'CLOSING' | 'ROLLOVER_READY';

export interface SprintDevLoopState {
  devLoopActive: true;
  lifecycleState: SprintLifecycleState;
  rolloverReady: boolean;
  sprintPressure: SprintPressure;
  localPatchRequired: true;
  providerRoutingDistribution: {providerClass: 'HIGH' | 'MEDIUM' | 'LOW'; count: number}[];
  estimatedAvoidedManualOrchestrationTokens: number;
  estimatedAvoidedSprintExplosion: number;
  compactBootstrap: string;
  compactClosure: string;
  boundedCognitionOnly: true;
  humanConfirmedOrchestrationOnly: true;
  noAutonomousRoadmapExpansion: true;
  noHiddenProviderSwitching: true;
  noGiantContinuityReplay: true;
}

export class SprintDevLoopMonitor {
  private lifecycleState: SprintLifecycleState = 'PLANNING';
  private compacted = false;

  evaluate(): SprintDevLoopState {
    const rolloverReady = this.lifecycleState === 'ROLLOVER_READY' || this.compacted;
    const sprintPressure: SprintPressure = this.compacted ? 'LOW' : 'MEDIUM';
    return {
      devLoopActive: true,
      lifecycleState: this.lifecycleState,
      rolloverReady,
      sprintPressure,
      localPatchRequired: true,
      providerRoutingDistribution: [
        {providerClass: 'HIGH', count: 3},
        {providerClass: 'MEDIUM', count: 3},
        {providerClass: 'LOW', count: 3},
      ],
      estimatedAvoidedManualOrchestrationTokens: this.compacted ? 3000 : 2520,
      estimatedAvoidedSprintExplosion: this.compacted ? 2400 : 2000,
      compactBootstrap: 'Enter-only continuation; adjacent runtimes only; LOCAL_PATCH_REQUIRED.',
      compactClosure: 'Compact closure keeps validation summary and delta carryover only.',
      boundedCognitionOnly: true,
      humanConfirmedOrchestrationOnly: true,
      noAutonomousRoadmapExpansion: true,
      noHiddenProviderSwitching: true,
      noGiantContinuityReplay: true,
    };
  }

  generatePlan(): SprintDevLoopState {
    this.lifecycleState = 'PLANNING';
    return this.evaluate();
  }

  activateSprint(): SprintDevLoopState {
    this.lifecycleState = 'ACTIVE';
    return this.evaluate();
  }

  generateNextSprint(): SprintDevLoopState {
    this.lifecycleState = 'PLANNING';
    return this.evaluate();
  }

  generateBootstrap(): SprintDevLoopState {
    this.lifecycleState = 'ROLLOVER_READY';
    return this.evaluate();
  }

  compactClosure(): SprintDevLoopState {
    this.compacted = true;
    this.lifecycleState = 'ROLLOVER_READY';
    return this.evaluate();
  }
}

export class SprintActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 75);

  constructor(private readonly monitor: SprintDevLoopMonitor) {
    this.item.command = 'aiDevOs.showSprintLifecycle';
  }

  refresh(): SprintDevLoopState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS SPRINT_ACTIVE ${state.lifecycleState}`;
    this.item.tooltip = `Sprint lifecycle ${state.lifecycleState}; bounded cognition only`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class SprintRolloverStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 74);

  constructor(private readonly monitor: SprintDevLoopMonitor) {
    this.item.command = 'aiDevOs.generateSprintBootstrap';
  }

  refresh(): SprintDevLoopState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ROLLOVER_READY ${state.rolloverReady ? 'YES' : 'NO'}`;
    this.item.tooltip = state.compactBootstrap;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class SprintPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 73);

  constructor(private readonly monitor: SprintDevLoopMonitor) {
    this.item.command = 'aiDevOs.showSprintGovernance';
  }

  refresh(): SprintDevLoopState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS SPRINT_PRESSURE ${state.sprintPressure}`;
    this.item.tooltip = `Avoided sprint explosion ${state.estimatedAvoidedSprintExplosion}; no roadmap expansion`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class LocalPatchRequiredStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 72);

  constructor(private readonly monitor: SprintDevLoopMonitor) {
    this.item.command = 'aiDevOs.generateSprintPlan';
  }

  refresh(): SprintDevLoopState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LOCAL_PATCH_REQUIRED';
    this.item.tooltip = `Human-confirmed orchestration ${state.humanConfirmedOrchestrationOnly}; hidden provider switching forbidden`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
