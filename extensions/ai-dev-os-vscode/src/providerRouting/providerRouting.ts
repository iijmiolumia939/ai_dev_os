import * as vscode from 'vscode';

export type ProviderClass = 'HIGH' | 'MEDIUM' | 'LOW';
export type ProviderPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface ProviderDistributionEntry {
  providerClass: ProviderClass;
  count: number;
}

export interface ProviderRoutingState {
  providerRoutingActive: true;
  recommendedProviderClass: ProviderClass;
  providerBurnPressure: ProviderPressure;
  downgradeReady: boolean;
  compactRouting: boolean;
  distribution: ProviderDistributionEntry[];
  premiumVsCheapRatio: number;
  estimatedAvoidedPremiumProviderBurn: number;
  estimatedAvoidedUnnecessaryHighTierUsage: number;
  localOnly: true;
  deterministic: true;
  summaryOnly: true;
  noRealBillingApi: true;
  noHiddenProviderSwitching: true;
  noAutomaticProviderExecution: true;
  noProviderUpload: true;
  noHiddenEscalation: true;
}

const baseDistribution: ProviderDistributionEntry[] = [
  {providerClass: 'LOW', count: 3},
  {providerClass: 'MEDIUM', count: 2},
  {providerClass: 'HIGH', count: 1},
];

export class ProviderRoutingMonitor {
  private compacted = false;

  evaluate(): ProviderRoutingState {
    const distribution = this.compacted
      ? baseDistribution.filter((entry) => entry.providerClass !== 'HIGH')
      : baseDistribution;
    const premium = distribution.find((entry) => entry.providerClass === 'HIGH')?.count ?? 0;
    const cheap = distribution.find((entry) => entry.providerClass === 'LOW')?.count ?? 1;
    const pressure: ProviderPressure = premium > 1 ? 'HIGH' : premium === 1 ? 'MEDIUM' : 'LOW';
    return {
      providerRoutingActive: true,
      recommendedProviderClass: this.compacted ? 'LOW' : 'MEDIUM',
      providerBurnPressure: pressure,
      downgradeReady: pressure !== 'LOW' || this.compacted,
      compactRouting: this.compacted,
      distribution,
      premiumVsCheapRatio: premium / Math.max(1, cheap),
      estimatedAvoidedPremiumProviderBurn: this.compacted ? 24 : 16,
      estimatedAvoidedUnnecessaryHighTierUsage: this.compacted ? 8 : 4,
      localOnly: true,
      deterministic: true,
      summaryOnly: true,
      noRealBillingApi: true,
      noHiddenProviderSwitching: true,
      noAutomaticProviderExecution: true,
      noProviderUpload: true,
      noHiddenEscalation: true,
    };
  }

  compactRouting(): ProviderRoutingState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class PremiumProviderStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 78);

  constructor(private readonly monitor: ProviderRoutingMonitor) {
    this.item.command = 'aiDevOs.showProviderRouting';
  }

  refresh(): ProviderRoutingState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS PREMIUM_PROVIDER ${state.recommendedProviderClass}`;
    this.item.tooltip = `Provider routing ${state.recommendedProviderClass}; avoided burn ${state.estimatedAvoidedPremiumProviderBurn}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ProviderDowngradeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 77);

  constructor(private readonly monitor: ProviderRoutingMonitor) {
    this.item.command = 'aiDevOs.showDowngradeRecommendations';
  }

  refresh(): ProviderRoutingState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS DOWNGRADE_READY ${state.downgradeReady ? 'YES' : 'NO'}`;
    this.item.tooltip = `Downgrade ready ${state.downgradeReady}; summary-only ${state.summaryOnly}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ProviderPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 76);

  constructor(private readonly monitor: ProviderRoutingMonitor) {
    this.item.command = 'aiDevOs.showProviderBudget';
  }

  refresh(): ProviderRoutingState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS PROVIDER_PRESSURE ${state.providerBurnPressure}`;
    this.item.tooltip = `Premium to cheap ratio ${state.premiumVsCheapRatio}; no provider execution`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}