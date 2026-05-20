import * as vscode from 'vscode';
import {RuntimeSimplificationMonitor} from '../runtimeSimplification/runtimeSimplification';

export class RuntimeOverlapViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.changed.event;

  constructor(private readonly monitor: RuntimeSimplificationMonitor) {}

  refresh(): void {
    this.changed.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(): vscode.TreeItem[] {
    const state = this.monitor.evaluate();
    return [
      new vscode.TreeItem(`Detected: ${state.overlapDetected}`),
      new vscode.TreeItem(`Density: ${state.overlapDensity}`),
      new vscode.TreeItem(`Pressure: ${state.simplificationPressure}`),
      ...state.overlapCategories.map((category) => new vscode.TreeItem(category)),
    ];
  }
}