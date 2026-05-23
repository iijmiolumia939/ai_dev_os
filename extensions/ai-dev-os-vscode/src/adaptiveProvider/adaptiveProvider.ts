import * as vscode from 'vscode';

export interface AdaptiveProviderState {
  adaptiveProviderActive: boolean;
  providerCapabilityScore: number;
  providerFatigueScore: number;
  providerCostPressure: string;
  providerConfidenceScore: number;
  recommendedProvider: string;
  compactSummary: string;
}

export class AdaptiveProviderMonitor {
  evaluate(): AdaptiveProviderState {
    return {
      adaptiveProviderActive: true,
      providerCapabilityScore: 100,
      providerFatigueScore: 39,
      providerCostPressure: 'LOW',
      providerConfidenceScore: 71,
      recommendedProvider: 'local_review',
      compactSummary: 'bounded adaptive provider active; local-first routing guarded',
    };
  }
}

export class ProviderBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 8);

  constructor(private readonly monitor: AdaptiveProviderMonitor) {
    this.item.command = 'aiDevOs.showProviderCapability';
  }

  refresh(): AdaptiveProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PROVIDER_BOUNDED';
    this.item.tooltip = `capability ${state.providerCapabilityScore}; ${state.recommendedProvider}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class LocalFirstStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 7);

  constructor(private readonly monitor: AdaptiveProviderMonitor) {
    this.item.command = 'aiDevOs.showProviderConfidence';
  }

  refresh(): AdaptiveProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LOCAL_FIRST';
    this.item.tooltip = `confidence ${state.providerConfidenceScore}; hidden escalation blocked`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class FatigueTrackedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 6);

  constructor(private readonly monitor: AdaptiveProviderMonitor) {
    this.item.command = 'aiDevOs.showProviderFatigue';
  }

  refresh(): AdaptiveProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS FATIGUE_TRACKED';
    this.item.tooltip = `fatigue ${state.providerFatigueScore}; cooldown bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CostGuardedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 5);

  constructor(private readonly monitor: AdaptiveProviderMonitor) {
    this.item.command = 'aiDevOs.showProviderCost';
  }

  refresh(): AdaptiveProviderState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS COST_GUARDED';
    this.item.tooltip = `cost pressure ${state.providerCostPressure}; local-first recommendation`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
