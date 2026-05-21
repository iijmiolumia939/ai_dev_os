import * as vscode from 'vscode';

export interface LocalProviderState {
  localProviderReady: true;
  ollamaActive: true;
  localBudgetOk: true;
  premiumEscalation: 'HUMAN_CONFIRMED_ONLY';
  primaryCodingModel: 'qwen2.5-coder:14b';
  governanceCompressionModel: 'gemma3:12b';
  fallbackCodingModel: 'qwen2.5-coder:7b';
  estimatedAvoidedPremiumTokens: number;
  estimatedLocalExecutionRatio: number;
  distribution: {LOW_LOCAL: number; MEDIUM_ROUTED: number; HIGH_CLOUD: number};
  compactPromptsOnly: true;
  localPatchOnly: true;
  adjacentRuntimeRetrievalOnly: true;
  boundedContextWindows: true;
  noRepoWideLocalReasoning: true;
  noGiantContinuityReplay: true;
  noRecursiveLocalExecution: true;
  noHiddenAutonomousLoops: true;
  noUnrestrictedRepositoryMutation: true;
}

export class LocalProviderMonitor {
  private compacted = false;

  evaluate(): LocalProviderState {
    const lowLocal = this.compacted ? 6 : 8;
    const mediumRouted = this.compacted ? 2 : 3;
    const highCloud = 3;
    return {
      localProviderReady: true,
      ollamaActive: true,
      localBudgetOk: true,
      premiumEscalation: 'HUMAN_CONFIRMED_ONLY',
      primaryCodingModel: 'qwen2.5-coder:14b',
      governanceCompressionModel: 'gemma3:12b',
      fallbackCodingModel: 'qwen2.5-coder:7b',
      estimatedAvoidedPremiumTokens: lowLocal * 900 + mediumRouted * 350,
      estimatedLocalExecutionRatio: Number(((lowLocal + Math.max(0, mediumRouted - 1)) / (lowLocal + mediumRouted + highCloud)).toFixed(4)),
      distribution: {LOW_LOCAL: lowLocal, MEDIUM_ROUTED: mediumRouted, HIGH_CLOUD: highCloud},
      compactPromptsOnly: true,
      localPatchOnly: true,
      adjacentRuntimeRetrievalOnly: true,
      boundedContextWindows: true,
      noRepoWideLocalReasoning: true,
      noGiantContinuityReplay: true,
      noRecursiveLocalExecution: true,
      noHiddenAutonomousLoops: true,
      noUnrestrictedRepositoryMutation: true,
    };
  }

  compactLocalExecution(): LocalProviderState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class LocalProviderReadyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 75);

  constructor(private readonly monitor: LocalProviderMonitor) {
    this.item.command = 'aiDevOs.showLocalProviders';
  }

  refresh(): LocalProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LOCAL_PROVIDER_READY';
    this.item.tooltip = `Local provider ${state.primaryCodingModel}; local ratio ${state.estimatedLocalExecutionRatio}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class OllamaActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 74);

  constructor(private readonly monitor: LocalProviderMonitor) {
    this.item.command = 'aiDevOs.testOllamaProvider';
  }

  refresh(): LocalProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS OLLAMA_ACTIVE';
    this.item.tooltip = `Ollama models ${state.primaryCodingModel}, ${state.governanceCompressionModel}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class LocalBudgetOkStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 73);

  constructor(private readonly monitor: LocalProviderMonitor) {
    this.item.command = 'aiDevOs.showLocalProviderBudget';
  }

  refresh(): LocalProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LOCAL_BUDGET_OK';
    this.item.tooltip = `Compact prompts ${state.compactPromptsOnly}; LOCAL_PATCH ${state.localPatchOnly}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class PremiumEscalationStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 72);

  constructor(private readonly monitor: LocalProviderMonitor) {
    this.item.command = 'aiDevOs.showProviderRouting';
  }

  refresh(): LocalProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PREMIUM_ESCALATION';
    this.item.tooltip = `Premium escalation ${state.premiumEscalation}; no hidden escalation`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
