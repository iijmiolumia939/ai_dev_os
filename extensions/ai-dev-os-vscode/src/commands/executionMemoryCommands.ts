import * as vscode from 'vscode';
import {
  ExecutionMemoryMonitor,
  ExecutionMemoryStatusBar,
  ProviderMemoryStatusBar,
  RetryMemoryStatusBar,
  ReuseBoundedStatusBar,
} from '../executionMemory/executionMemory';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerExecutionMemoryCommands(
  monitor: ExecutionMemoryMonitor,
  executionMemoryStatus: ExecutionMemoryStatusBar,
  retryMemoryStatus: RetryMemoryStatusBar,
  reuseBoundedStatus: ReuseBoundedStatusBar,
  providerMemoryStatus: ProviderMemoryStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    executionMemoryStatus.refresh();
    retryMemoryStatus.refresh();
    reuseBoundedStatus.refresh();
    providerMemoryStatus.refresh();
  };

  const showExecutionPatterns = vscode.commands.registerCommand(
    'aiDevOs.showExecutionPatterns',
    async () => {
      const state = executionMemoryStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution patterns: ${state.executionPatternScore}.`,
      );
    },
  );

  const showRetryPatterns = vscode.commands.registerCommand(
    'aiDevOs.showRetryPatterns',
    async () => {
      const state = retryMemoryStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry patterns: ${state.retryPatternScore}.`,
      );
    },
  );

  const showExecutionReuse = vscode.commands.registerCommand(
    'aiDevOs.showExecutionReuse',
    async () => {
      const state = reuseBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS execution reuse: ${state.executionReuseScore}.`,
      );
    },
  );

  const showProviderExecutionMemory = vscode.commands.registerCommand(
    'aiDevOs.showProviderExecutionMemory',
    async () => {
      const state = providerMemoryStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider execution memory: ${state.providerExecutionMemoryScore}.`,
      );
    },
  );

  const compactExecutionMemorySummary = vscode.commands.registerCommand(
    'aiDevOs.compactExecutionMemorySummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'execution-memory-compact-summary',
        `AI_DEV_OS compact execution memory: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showExecutionPatterns,
    showRetryPatterns,
    showExecutionReuse,
    showProviderExecutionMemory,
    compactExecutionMemorySummary,
  ];
}
