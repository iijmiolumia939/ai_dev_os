import * as vscode from 'vscode';
import {RuntimeSimplificationMonitor} from '../runtimeSimplification/runtimeSimplification';

export class MergeCandidateViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
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
      new vscode.TreeItem(`Human review: ${state.humanReviewRequired}`),
      new vscode.TreeItem(`Automatic mutation: ${state.automaticMutationUsed}`),
      ...state.mergeCandidates.map((candidate) => new vscode.TreeItem(candidate)),
    ];
  }
}