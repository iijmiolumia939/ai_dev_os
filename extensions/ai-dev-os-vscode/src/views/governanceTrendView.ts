import * as vscode from 'vscode';
import {GovernanceTrendMonitor} from '../governance/trends';

export class GovernanceTrendViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.changed.event;

  constructor(private readonly monitor: GovernanceTrendMonitor) {}

  refresh(): void {
    this.changed.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  async getChildren(): Promise<vscode.TreeItem[]> {
    const state = await this.monitor.evaluate();
    return [
      new vscode.TreeItem(`Trend: ${state.trendLevel}`),
      new vscode.TreeItem(`Window: ${state.activeWindowSize}`),
      new vscode.TreeItem(`Evicted: ${state.evictedSnapshots}`),
      new vscode.TreeItem(`Drift: ${state.driftDetected}`),
      new vscode.TreeItem(`Regression: ${state.regressionDetected}`),
      new vscode.TreeItem(`Oscillation: ${state.oscillationDetected}`),
      new vscode.TreeItem(`Bounded: ${state.boundedWindowMaintained}`),
      new vscode.TreeItem(`Delta: ${state.dashboardDelta.join('; ')}`),
    ];
  }
}
