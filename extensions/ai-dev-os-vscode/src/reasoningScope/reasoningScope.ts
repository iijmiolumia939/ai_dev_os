import * as vscode from 'vscode';

export type PremiumPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface ReasoningScopeState {
  reasoningScopeActive: boolean;
  reasoningDepthActive: boolean;
  architectureGuardActive: boolean;
  localPatchModeActive: boolean;
  reasoningPressure: PremiumPressure;
  depthCap: number;
  taskLocalScope: string[];
  estimatedAvoidedPremiumReasoningBurn: number;
  estimatedAvoidedArchitectureReasoning: number;
  localOnly: true;
  deterministic: true;
  summaryOnly: true;
  boundedCognitionOnly: true;
  noHiddenProviderRouting: true;
}

const localScope = ['reasoning_scope', 'reasoning_routing'];

export class ReasoningScopeMonitor {
  private compacted = false;

  evaluate(): ReasoningScopeState {
    const taskLocalScope = this.compacted ? localScope.slice(0, 1) : localScope;
    const pressure: PremiumPressure = taskLocalScope.length > 1 ? 'MEDIUM' : 'LOW';
    return {
      reasoningScopeActive: true,
      reasoningDepthActive: true,
      architectureGuardActive: true,
      localPatchModeActive: true,
      reasoningPressure: pressure,
      depthCap: 1,
      taskLocalScope,
      estimatedAvoidedPremiumReasoningBurn: 4380,
      estimatedAvoidedArchitectureReasoning: 2200,
      localOnly: true,
      deterministic: true,
      summaryOnly: true,
      boundedCognitionOnly: true,
      noHiddenProviderRouting: true,
    };
  }

  compactScope(): ReasoningScopeState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class ReasoningScopeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 78);

  constructor(private readonly monitor: ReasoningScopeMonitor) {
    this.item.command = 'aiDevOs.showReasoningScope';
  }

  refresh(): ReasoningScopeState {
    const state = this.monitor.evaluate();
    const pressureLabel = state.reasoningPressure === 'LOW' ? '' : ' DEEP_REASONING PREMIUM_PRESSURE';
    this.item.text = `AI_DEV_OS LOCAL_PATCH${pressureLabel}`;
    this.item.tooltip = `Reasoning scope ${state.taskLocalScope.length} runtimes; depth cap ${state.depthCap}; pressure ${state.reasoningPressure}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
