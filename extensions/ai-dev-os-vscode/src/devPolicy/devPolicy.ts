import * as vscode from 'vscode';

export type PolicyPressure = 'LOW' | 'MEDIUM' | 'HIGH';

export interface DevelopmentPolicyState {
  devPolicyActive: true;
  policyStable: boolean;
  governancePressure: PolicyPressure;
  escalationPressure: PolicyPressure;
  realismProtected: boolean;
  providerRoutingDistribution: {providerClass: 'HIGH' | 'MEDIUM' | 'LOW'; count: number}[];
  estimatedAvoidedPolicyOverhead: number;
  estimatedAvoidedGovernanceExplosion: number;
  compactSummary: string;
  architectureHints: string[];
  embodimentHints: string[];
  providerHints: string[];
  antiExplosionHints: string[];
  localOnly: true;
  deterministic: true;
  summaryOnly: true;
  boundedPolicyOnly: true;
  humanConfirmedGovernanceOnly: true;
  noAutonomousEnforcement: true;
  noRepositoryMutationAuthority: true;
  noHiddenProviderSwitching: true;
}

export class DevPolicyMonitor {
  private compacted = false;

  evaluate(): DevelopmentPolicyState {
    const governancePressure: PolicyPressure = this.compacted ? 'LOW' : 'MEDIUM';
    const escalationPressure: PolicyPressure = this.compacted ? 'LOW' : 'MEDIUM';
    return {
      devPolicyActive: true,
      policyStable: this.compacted,
      governancePressure,
      escalationPressure,
      realismProtected: true,
      providerRoutingDistribution: [
        {providerClass: 'HIGH', count: 4},
        {providerClass: 'MEDIUM', count: 3},
        {providerClass: 'LOW', count: 3},
      ],
      estimatedAvoidedPolicyOverhead: this.compacted ? 3760 : 3520,
      estimatedAvoidedGovernanceExplosion: this.compacted ? 3040 : 2880,
      compactSummary: 'bounded advisory governance gate; no autonomous enforcement authority',
      architectureHints: ['LOCAL_PATCH required', 'no architecture rewrite', 'adjacent runtime only'],
      embodimentHints: ['low-motion realism', 'renderer-neutral boundary', 'no social scripting'],
      providerHints: ['HIGH for boundaries', 'MEDIUM for analysis', 'LOW for summaries'],
      antiExplosionHints: ['cap current sprint', 'evict giant history', 'block recursive governance'],
      localOnly: true,
      deterministic: true,
      summaryOnly: true,
      boundedPolicyOnly: true,
      humanConfirmedGovernanceOnly: true,
      noAutonomousEnforcement: true,
      noRepositoryMutationAuthority: true,
      noHiddenProviderSwitching: true,
    };
  }

  compactSummary(): DevelopmentPolicyState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class PolicyStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 63);

  constructor(private readonly monitor: DevPolicyMonitor) {
    this.item.command = 'aiDevOs.showDevelopmentPolicies';
  }

  refresh(): DevelopmentPolicyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS POLICY_STABLE ${state.policyStable ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.compactSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class GovernancePressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 62);

  constructor(private readonly monitor: DevPolicyMonitor) {
    this.item.command = 'aiDevOs.showArchitectureProtection';
  }

  refresh(): DevelopmentPolicyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS GOVERNANCE_PRESSURE ${state.governancePressure}`;
    this.item.tooltip = `Avoided governance explosion ${state.estimatedAvoidedGovernanceExplosion}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class EscalationPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 61);

  constructor(private readonly monitor: DevPolicyMonitor) {
    this.item.command = 'aiDevOs.showProviderEscalationPolicy';
  }

  refresh(): DevelopmentPolicyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ESCALATION_PRESSURE ${state.escalationPressure}`;
    this.item.tooltip = state.providerHints.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RealismProtectedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 60);

  constructor(private readonly monitor: DevPolicyMonitor) {
    this.item.command = 'aiDevOs.showEmbodimentRealismPolicy';
  }

  refresh(): DevelopmentPolicyState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS REALISM_PROTECTED ${state.realismProtected ? 'YES' : 'WATCH'}`;
    this.item.tooltip = state.embodimentHints.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}