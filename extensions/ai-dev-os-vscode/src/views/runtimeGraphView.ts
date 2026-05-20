import * as vscode from 'vscode';
import {RuntimeGraphMonitor} from '../runtimeGraph/runtimeGraph';

export class RuntimeGraphViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
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
    return [
      new vscode.TreeItem(`Nodes: ${state.nodeCount}`),
      new vscode.TreeItem(`Bounded edges: ${state.edgeCount}`),
      new vscode.TreeItem(`Density: ${state.dependencyDensity}`),
      new vscode.TreeItem(`Architecture pressure: ${state.architecturePressure}`),
      new vscode.TreeItem(`Cross-boundary warnings: ${state.crossBoundaryWarnings.length}`),
      new vscode.TreeItem(`Summary only: ${state.summaryOnly}`),
    ];
  }
}