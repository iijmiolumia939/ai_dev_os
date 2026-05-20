import * as vscode from 'vscode';
import {GovernanceHealthMonitor} from '../governance/health';

export class GovernanceDashboardViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.changed.event;

  constructor(private readonly monitor: GovernanceHealthMonitor) {}

  refresh(): void {
    this.changed.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  async getChildren(): Promise<vscode.TreeItem[]> {
    const state = await this.monitor.evaluate();
    return [
      new vscode.TreeItem(`Health: ${state.level} (${state.healthScore})`),
      new vscode.TreeItem(`Pressure: ${state.pressure}`),
      new vscode.TreeItem(`Dominant pressure: ${state.dominantPressure}`),
      new vscode.TreeItem(`Highest risk: ${state.highestRisk}`),
      new vscode.TreeItem(`Stale session: ${state.staleSessionActive ? 'active' : 'clear'}`),
      new vscode.TreeItem(`Checkpoint pressure: ${state.checkpointPressure}`),
      new vscode.TreeItem(`Architecture isolation: ${state.architectureIsolationState}`),
      new vscode.TreeItem(`Workspace: ${state.workspaceCleanliness}`),
      new vscode.TreeItem(`Rollout: ${state.rolloutStability}`),
      new vscode.TreeItem(`Summary only: ${state.summaryOnly}`),
    ];
  }
}
