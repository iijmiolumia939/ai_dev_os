import * as vscode from 'vscode';

export interface RuntimePolicyState {
  runtimePolicyActive: boolean;
  executionPolicyScore: number;
  retryPolicyScore: number;
  providerPolicyScore: number;
  continuationPolicyScore: number;
  reflectivePolicyScore: number;
  compactSummary: string;
}

export class RuntimePolicyMonitor {
  evaluate(): RuntimePolicyState {
    return {
      runtimePolicyActive: true,
      executionPolicyScore: 93,
      retryPolicyScore: 79,
      providerPolicyScore: 80,
      continuationPolicyScore: 88,
      reflectivePolicyScore: 94,
      compactSummary: 'bounded runtime policy active; local-first escalation guarded',
    };
  }
}

export class PolicyBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 0);

  constructor(private readonly monitor: RuntimePolicyMonitor) {
    this.item.command = 'aiDevOs.showRuntimePolicy';
  }

  refresh(): RuntimePolicyState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS POLICY_BOUNDED';
    this.item.tooltip = `runtime policy active ${state.runtimePolicyActive}; execution ${state.executionPolicyScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class GovernanceStablePolicyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -1);

  constructor(private readonly monitor: RuntimePolicyMonitor) {
    this.item.command = 'aiDevOs.showRuntimePolicy';
  }

  refresh(): RuntimePolicyState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS GOVERNANCE_STABLE';
    this.item.tooltip = `provider ${state.providerPolicyScore}; reflective ${state.reflectivePolicyScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class LocalFirstPolicyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -2);

  constructor(private readonly monitor: RuntimePolicyMonitor) {
    this.item.command = 'aiDevOs.showProviderPolicy';
  }

  refresh(): RuntimePolicyState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LOCAL_FIRST_POLICY';
    this.item.tooltip = `provider policy ${state.providerPolicyScore}; frontier escalation guarded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class EscalationGuardedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -3);

  constructor(private readonly monitor: RuntimePolicyMonitor) {
    this.item.command = 'aiDevOs.showProviderPolicy';
  }

  refresh(): RuntimePolicyState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ESCALATION_GUARDED';
    this.item.tooltip = `retry ${state.retryPolicyScore}; continuation ${state.continuationPolicyScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
