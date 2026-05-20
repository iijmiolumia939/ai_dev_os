import * as vscode from 'vscode';
import {GovernanceCoreMonitor} from '../governanceCore/governanceCore';

export class PrimitiveReuseViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.changed.event;

  constructor(private readonly monitor: GovernanceCoreMonitor) {}

  refresh(): void {
    this.changed.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(): vscode.TreeItem[] {
    const state = this.monitor.evaluate();
    return [
      new vscode.TreeItem(`Reuse targets: ${state.reuseTargets.length}`),
      new vscode.TreeItem(`Warnings reduced: ${state.duplicatedGovernanceWarningsReduced}`),
      ...state.reuseTargets.map((target) => new vscode.TreeItem(target)),
    ];
  }
}