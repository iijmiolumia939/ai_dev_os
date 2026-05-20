import * as vscode from 'vscode';

export interface RuntimeSimplificationState {
  overlapDetected: boolean;
  overlapCategories: string[];
  overlapDensity: number;
  contractGroups: string[];
  mergeCandidates: string[];
  governanceGroups: string[];
  simplificationPressure: 'low' | 'medium' | 'high';
  recommendationCount: number;
  humanReviewRequired: boolean;
  summaryOnly: true;
  automaticMutationUsed: false;
}

const overlapCategories = [
  'duplicated governance signals',
  'duplicated persistence logic',
  'duplicated session lifecycle logic',
  'duplicated compact export logic',
];

export class RuntimeSimplificationMonitor {
  private compacted = false;

  evaluate(): RuntimeSimplificationState {
    const categories = this.compacted ? overlapCategories.slice(0, 2) : overlapCategories;
    const contractGroups = this.compacted
      ? ['policies:broad_surface']
      : ['frames:broad_surface', 'policies:broad_surface', 'contracts:broad_surface'];
    const mergeCandidates = categories.slice(0, 3).map((category) => `review ${category}`);
    const governanceGroups = categories.filter((category) => category.includes('governance') || category.includes('persistence'));
    const density = Number((categories.length / 6).toFixed(4));
    const pressure = density >= 0.67 ? 'high' : density >= 0.34 ? 'medium' : 'low';
    return {
      overlapDetected: categories.length > 0,
      overlapCategories: categories,
      overlapDensity: density,
      contractGroups,
      mergeCandidates,
      governanceGroups,
      simplificationPressure: pressure,
      recommendationCount: mergeCandidates.length + contractGroups.length + governanceGroups.length,
      humanReviewRequired: mergeCandidates.length > 0,
      summaryOnly: true,
      automaticMutationUsed: false,
    };
  }

  compact(): RuntimeSimplificationState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class SimplificationStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 87);

  constructor(private readonly monitor: RuntimeSimplificationMonitor) {
    this.item.command = 'aiDevOs.showSimplificationRecommendations';
  }

  refresh(): RuntimeSimplificationState {
    const state = this.monitor.evaluate();
    this.item.text = `AI_DEV_OS Simplify ${state.simplificationPressure.toUpperCase()}`;
    this.item.tooltip = `Runtime overlap ${state.overlapCategories.length}; merge candidates ${state.mergeCandidates.length}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}