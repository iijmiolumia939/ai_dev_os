import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  ContinuationStreamingStatusBar,
  InterruptionSafeStatusBar,
  ProviderStreamingStatusBar,
  StreamingActiveStatusBar,
  StreamingCognitionMonitor,
} from '../streamingCognition/streamingCognition';

export function registerStreamingCognitionCommands(
  monitor: StreamingCognitionMonitor,
  streamingStatus: StreamingActiveStatusBar,
  interruptionStatus: InterruptionSafeStatusBar,
  providerStatus: ProviderStreamingStatusBar,
  continuationStatus: ContinuationStreamingStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    streamingStatus.refresh();
    interruptionStatus.refresh();
    providerStatus.refresh();
    continuationStatus.refresh();
  };

  const showStreamingCognition = vscode.commands.registerCommand(
    'aiDevOs.showStreamingCognition',
    async () => {
      const state = streamingStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS streaming cognition: ${state.cognitionSummary.join('; ')}.`,
      );
    },
  );

  const showStreamingContinuation = vscode.commands.registerCommand(
    'aiDevOs.showStreamingContinuation',
    async () => {
      const state = continuationStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS streaming continuation: ${state.continuationSummary.join('; ')}.`,
      );
    },
  );

  const showInterruptionRecovery = vscode.commands.registerCommand(
    'aiDevOs.showInterruptionRecovery',
    async () => {
      const state = interruptionStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS interruption recovery: ${state.interruptionRecovery.join('; ')}.`,
      );
    },
  );

  const showProviderStreaming = vscode.commands.registerCommand(
    'aiDevOs.showProviderStreaming',
    async () => {
      const state = providerStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider streaming: ${state.providerStreamingSummary.join('; ')}.`,
      );
    },
  );

  const compactStreamingSummary = vscode.commands.registerCommand(
    'aiDevOs.compactStreamingSummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await notifications.info(
        'streaming-cognition-compacted',
        `AI_DEV_OS streaming summary compacted; pressure ${state.streamingPressure}.`,
      );
    },
  );

  return [
    showStreamingCognition,
    showStreamingContinuation,
    showInterruptionRecovery,
    showProviderStreaming,
    compactStreamingSummary,
  ];
}
