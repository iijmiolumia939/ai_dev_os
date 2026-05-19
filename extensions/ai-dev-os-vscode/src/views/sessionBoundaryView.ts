import * as vscode from 'vscode';
import {BoundaryStateStore} from '../state/boundaryState';

export class SessionBoundaryViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
  private readonly changed = new vscode.EventEmitter<void>();
  readonly onDidChangeTreeData = this.changed.event;

  constructor(private readonly store: BoundaryStateStore) {}

  refresh(): void {
    this.changed.fire();
  }

  getTreeItem(element: vscode.TreeItem): vscode.TreeItem {
    return element;
  }

  getChildren(): vscode.TreeItem[] {
    const state = this.store.read();
    return [
      new vscode.TreeItem(`State: ${state.currentEnforcementState}`),
      new vscode.TreeItem(`Generation: ${state.currentSessionGeneration}`),
      new vscode.TreeItem(`Pending rollover: ${state.pendingRolloverState}`),
      new vscode.TreeItem(`Warnings: ${state.staleWarningCount}`),
    ];
  }
}
