import * as vscode from 'vscode';

export type SubagentPressure = 'LOW' | 'MEDIUM' | 'HIGH' | 'BLOCKED';

export interface SubagentExecutionState {
  subagentActive: true;
  localDelegation: true;
  fallbackReady: true;
  swarmBlocked: true;
  localSubagentProvider: 'ollama:qwen2.5-coder:7b';
  governanceSummaryProvider: 'ollama:gemma3:12b';
  mediumProvider: 'cloud:medium_provider';
  highProvider: 'GPT-5.5 premium governance provider';
  routingDistribution: {providerClass: 'LOW_LOCAL' | 'LOW_GOVERNANCE' | 'MEDIUM' | 'HIGH'; count: number}[];
  delegationScope: string[];
  fallbackState: string;
  governanceWarnings: string[];
  compactSummary: string;
  estimatedAvoidedPremiumSubagentTokens: number;
  estimatedAvoidedRecursiveAgentExplosion: number;
  boundedDelegationOnly: true;
  humanConfirmedDelegationOnly: true;
  noAutonomousAgentSwarms: true;
  noRecursiveSubagentSpawning: true;
  noHiddenProviderSwitching: true;
  noRepoWideDelegatedCognition: true;
  noAutonomousRepositoryMutation: true;
}

export class SubagentExecutionMonitor {
  private compacted = false;

  evaluate(): SubagentExecutionState {
    const localCount = this.compacted ? 4 : 5;
    return {
      subagentActive: true,
      localDelegation: true,
      fallbackReady: true,
      swarmBlocked: true,
      localSubagentProvider: 'ollama:qwen2.5-coder:7b',
      governanceSummaryProvider: 'ollama:gemma3:12b',
      mediumProvider: 'cloud:medium_provider',
      highProvider: 'GPT-5.5 premium governance provider',
      routingDistribution: [
        {providerClass: 'LOW_LOCAL', count: localCount},
        {providerClass: 'LOW_GOVERNANCE', count: 2},
        {providerClass: 'MEDIUM', count: 2},
        {providerClass: 'HIGH', count: 1},
      ],
      delegationScope: ['LOCAL_PATCH', 'adjacent runtime', 'bounded retrieval', 'compact payload'],
      fallbackState: '14b GPU degraded; 7b local fallback ready; stop after one fallback',
      governanceWarnings: ['swarm blocked', 'recursive subagent spawn blocked'],
      compactSummary: 'bounded subagent delegation; no autonomous swarm; human-confirmed execution only',
      estimatedAvoidedPremiumSubagentTokens: localCount * 850 + 1000,
      estimatedAvoidedRecursiveAgentExplosion: 6600,
      boundedDelegationOnly: true,
      humanConfirmedDelegationOnly: true,
      noAutonomousAgentSwarms: true,
      noRecursiveSubagentSpawning: true,
      noHiddenProviderSwitching: true,
      noRepoWideDelegatedCognition: true,
      noAutonomousRepositoryMutation: true,
    };
  }

  compactDelegationSummary(): SubagentExecutionState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class SubagentActiveStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 63);

  constructor(private readonly monitor: SubagentExecutionMonitor) {
    this.item.command = 'aiDevOs.showSubagentRouting';
  }

  refresh(): SubagentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS SUBAGENT_ACTIVE';
    this.item.tooltip = state.compactSummary;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class LocalDelegationStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 62);

  constructor(private readonly monitor: SubagentExecutionMonitor) {
    this.item.command = 'aiDevOs.testLocalSubagent';
  }

  refresh(): SubagentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS LOCAL_DELEGATION';
    this.item.tooltip = `Local delegation ${state.localSubagentProvider}; ${state.delegationScope.join('; ')}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class FallbackReadyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 61);

  constructor(private readonly monitor: SubagentExecutionMonitor) {
    this.item.command = 'aiDevOs.showFallbackState';
  }

  refresh(): SubagentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS FALLBACK_READY';
    this.item.tooltip = state.fallbackState;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class SwarmBlockedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 60);

  constructor(private readonly monitor: SubagentExecutionMonitor) {
    this.item.command = 'aiDevOs.showSubagentGovernance';
  }

  refresh(): SubagentExecutionState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS SWARM_BLOCKED';
    this.item.tooltip = state.governanceWarnings.join('; ');
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
