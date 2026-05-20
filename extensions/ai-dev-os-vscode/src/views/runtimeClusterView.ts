import * as vscode from 'vscode';
import {RuntimeGraphMonitor} from '../runtimeGraph/runtimeGraph';

export class RuntimeClusterViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.changed.event;

  constructor(private readonly monitor: RuntimeGraphMonitor) {}

  refresh(): void {
    this.changed.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(): vscode.TreeItem[] {
    const state = this.monitor.evaluate();
    const clusters = Object.entries(state.clusterSizes).map(
      ([category, count]) => new vscode.TreeItem(`${category}: ${count}`),
    );
    return [
      ...clusters,
      new vscode.TreeItem(`Oversized: ${state.oversizedRuntimes.join(', ') || 'none'}`),
      new vscode.TreeItem(`Isolated: ${state.isolatedClusters.join(', ') || 'none'}`),
      new vscode.TreeItem(`Simplification: ${state.simplificationRecommended}`),
    ];
  }
}