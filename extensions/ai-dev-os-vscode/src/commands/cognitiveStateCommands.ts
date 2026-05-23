import * as vscode from 'vscode';
import {
  AttentionFocusStatusBar,
  CognitiveLoadStatusBar,
  CognitiveStateMemoryPressureStatusBar,
  CognitiveStateMonitor,
} from '../cognitiveState/cognitiveState';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerCognitiveStateCommands(
  monitor: CognitiveStateMonitor,
  cognitiveLoadStatus: CognitiveLoadStatusBar,
  attentionFocusStatus: AttentionFocusStatusBar,
  cognitiveMemoryPressureStatus: CognitiveStateMemoryPressureStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    cognitiveLoadStatus.refresh();
    attentionFocusStatus.refresh();
    cognitiveMemoryPressureStatus.refresh();
  };

  const showCognitiveState = vscode.commands.registerCommand(
    'aiDevOs.showCognitiveState',
    async () => {
      const state = cognitiveLoadStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS cognitive state: ${state.compactSummary}.`,
      );
    },
  );

  const showAttentionFocus = vscode.commands.registerCommand(
    'aiDevOs.showAttentionFocus',
    async () => {
      const state = attentionFocusStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS attention focus: ${state.attentionFocus}; ${state.attentionDistribution.join(', ')}.`,
      );
    },
  );

  const showCognitiveMemoryPressure = vscode.commands.registerCommand(
    'aiDevOs.showCognitiveMemoryPressure',
    async () => {
      const state = cognitiveMemoryPressureStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS cognitive memory pressure: ${state.memoryPressure}.`,
      );
    },
  );

  const compactCognitiveState = vscode.commands.registerCommand(
    'aiDevOs.compactCognitiveState',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'cognitive-state-compact-summary',
        `AI_DEV_OS compact cognitive state: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showCognitiveState,
    showAttentionFocus,
    showCognitiveMemoryPressure,
    compactCognitiveState,
  ];
}