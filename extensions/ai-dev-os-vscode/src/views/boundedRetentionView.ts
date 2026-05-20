import * as vscode from 'vscode';
import {GovernanceCoreMonitor} from '../governanceCore/governanceCore';

export class BoundedRetentionViewProvider implements vscode.TreeDataProvider<vscode.TreeItem> {
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
      new vscode.TreeItem(`Retention limit: ${state.retentionLimit}`),
      new vscode.TreeItem(`Evicted items: ${state.evictedItems}`),
      new vscode.TreeItem(`Compact export: ${state.compactExportActive}`),
      new vscode.TreeItem(`Automatic rewrite: ${state.automaticRewriteUsed}`),
    ];
  }
}