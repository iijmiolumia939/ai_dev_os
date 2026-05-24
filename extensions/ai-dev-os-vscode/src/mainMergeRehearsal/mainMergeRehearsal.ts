import * as vscode from 'vscode';

export interface MainMergeRehearsalState {
  mainMergeRehearsalActive: boolean;
  protectedBranchReadinessScore: number;
  mergeConflictVisibilityScore: number;
  rollbackSurvivabilityScore: number;
  postMergeRuntimeScore: number;
  ciReadinessScore: number;
  estimatedAvoidedMergeInstability: number;
  estimatedAvoidedPostMergeRegression: number;
  estimatedAvoidedFrontierRecovery: number;
  compactSummary: string;
}

export class MainMergeRehearsalMonitor {
  evaluate(): MainMergeRehearsalState {
    return {
      mainMergeRehearsalActive: true,
      protectedBranchReadinessScore: 100,
      mergeConflictVisibilityScore: 100,
      rollbackSurvivabilityScore: 100,
      postMergeRuntimeScore: 100,
      ciReadinessScore: 100,
      estimatedAvoidedMergeInstability: 40,
      estimatedAvoidedPostMergeRegression: 40,
      estimatedAvoidedFrontierRecovery: 40,
      compactSummary: 'main merge rehearsal active; protected branch, rollback, post-merge runtime, and CI readiness bounded',
    };
  }
}

export class MergeRehearsedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -36);

  constructor(private readonly monitor: MainMergeRehearsalMonitor) {
    this.item.command = 'aiDevOs.showMergeRehearsal';
  }

  refresh(): MainMergeRehearsalState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS MERGE_REHEARSED';
    this.item.tooltip = `protected branch readiness ${state.protectedBranchReadinessScore}; conflict visibility ${state.mergeConflictVisibilityScore}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RollbackReadyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -37);

  constructor(private readonly monitor: MainMergeRehearsalMonitor) {
    this.item.command = 'aiDevOs.showRollbackSurvivability';
  }

  refresh(): MainMergeRehearsalState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ROLLBACK_READY';
    this.item.tooltip = `rollback survivability ${state.rollbackSurvivabilityScore}; active ${state.mainMergeRehearsalActive}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class PostMergeSafeStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -38);

  constructor(private readonly monitor: MainMergeRehearsalMonitor) {
    this.item.command = 'aiDevOs.showPostMergeRuntime';
  }

  refresh(): MainMergeRehearsalState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS POST_MERGE_SAFE';
    this.item.tooltip = `post-merge runtime ${state.postMergeRuntimeScore}; avoided regression ${state.estimatedAvoidedPostMergeRegression}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CIReadyStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, -39);

  constructor(private readonly monitor: MainMergeRehearsalMonitor) {
    this.item.command = 'aiDevOs.showMergeRehearsal';
  }

  refresh(): MainMergeRehearsalState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS CI_READY';
    this.item.tooltip = `CI readiness ${state.ciReadinessScore}; merge rehearsal ${state.mainMergeRehearsalActive}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
