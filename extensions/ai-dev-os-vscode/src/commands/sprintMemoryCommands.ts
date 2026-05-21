import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  MemoryEvictionStatusBar,
  MemoryPressureStatusBar,
  PatternStableStatusBar,
  SprintMemoryMonitor,
  SprintMemoryStatusBar,
} from '../sprintMemory/sprintMemory';

export function registerSprintMemoryCommands(
  monitor: SprintMemoryMonitor,
  memoryStatus: SprintMemoryStatusBar,
  pressureStatus: MemoryPressureStatusBar,
  patternStatus: PatternStableStatusBar,
  evictionStatus: MemoryEvictionStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    memoryStatus.refresh();
    pressureStatus.refresh();
    patternStatus.refresh();
    evictionStatus.refresh();
  };

  const showSprintMemory = vscode.commands.registerCommand('aiDevOs.showSprintMemory', async () => {
    const state = memoryStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS sprint memory: ${state.compactMemory}; bounded ${state.boundedMemoryOnly}.`,
    );
  });

  const showSprintPatterns = vscode.commands.registerCommand('aiDevOs.showSprintPatterns', async () => {
    const state = patternStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS sprint patterns: ${state.compactPatterns.join('; ')}.`,
    );
  });

  const showSprintFailures = vscode.commands.registerCommand('aiDevOs.showSprintFailures', async () => {
    const state = pressureStatus.refresh();
    await vscode.window.showInformationMessage(
      `AI_DEV_OS sprint failures: ${state.compactFailures.join('; ')}; pressure ${state.memoryPressure}.`,
    );
  });

  const showSprintEfficiency = vscode.commands.registerCommand(
    'aiDevOs.showSprintEfficiency',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS sprint efficiency: ${state.compactEfficiency}.`,
      );
    },
  );

  const compactSprintMemory = vscode.commands.registerCommand('aiDevOs.compactSprintMemory', async () => {
    const state = monitor.compactMemory();
    refreshAll();
    await notifications.info(
      'sprint-memory-compacted',
      `AI_DEV_OS compact sprint memory retained ${state.compactPatterns.length} heuristics.`,
    );
  });

  const cleanupSprintMemory = vscode.commands.registerCommand('aiDevOs.cleanupSprintMemory', async () => {
    const state = monitor.cleanupMemory();
    refreshAll();
    await notifications.info(
      'sprint-memory-cleaned',
      `AI_DEV_OS sprint memory cleanup complete; pressure ${state.memoryPressure}.`,
    );
  });

  return [
    showSprintMemory,
    showSprintPatterns,
    showSprintFailures,
    showSprintEfficiency,
    compactSprintMemory,
    cleanupSprintMemory,
  ];
}
