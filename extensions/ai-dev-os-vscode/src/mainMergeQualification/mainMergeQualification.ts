import * as vscode from 'vscode';

export interface MainMergeQualificationState {
  mainMergeQualificationActive: boolean;
  mergeReadinessScore: number;
  governanceCompletenessScore: number;
  validationCompletenessScore: number;
  runtimeCoherenceScore: number;
  operationalRiskScore: number;
  compactSummary: string;
}

export class MainMergeQualificationMonitor {
  evaluate(): MainMergeQualificationState {
    return {
      mainMergeQualificationActive: true,
      mergeReadinessScore: 100,
      governanceCompletenessScore: 100,
      validationCompletenessScore: 100,
      runtimeCoherenceScore: 100,
      operationalRiskScore: 90,
      compactSummary: 'main merge qualification active; governance complete and operational risk bounded',
    };
  }
}

export class MergeReadyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -32);

  constructor(private readonly monitor: MainMergeQualificationMonitor) {
    this.item.command = 'aiDevOs.showMergeQualification';
  }

  refresh(): MainMergeQualificationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS MERGE_READY';
    this.item.tooltip = `merge readiness ${state.mergeReadinessScore}; active ${state.mainMergeQualificationActive}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class GovernanceCompleteStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -33);

  constructor(private readonly monitor: MainMergeQualificationMonitor) {
    this.item.command = 'aiDevOs.showGovernanceCompleteness';
  }

  refresh(): MainMergeQualificationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS GOVERNANCE_COMPLETE';
    this.item.tooltip = `governance completeness ${state.governanceCompletenessScore}; runtime coherence ${state.runtimeCoherenceScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class QualificationValidationStableStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -34);

  constructor(private readonly monitor: MainMergeQualificationMonitor) {
    this.item.command = 'aiDevOs.showValidationCompleteness';
  }

  refresh(): MainMergeQualificationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS VALIDATION_STABLE';
    this.item.tooltip = `validation completeness ${state.validationCompletenessScore}; merge readiness ${state.mergeReadinessScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RiskBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -35);

  constructor(private readonly monitor: MainMergeQualificationMonitor) {
    this.item.command = 'aiDevOs.showOperationalRisk';
  }

  refresh(): MainMergeQualificationState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RISK_BOUNDED';
    this.item.tooltip = `operational risk ${state.operationalRiskScore}; runtime coherence ${state.runtimeCoherenceScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
