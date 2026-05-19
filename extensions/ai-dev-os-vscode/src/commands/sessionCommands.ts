import * as vscode from 'vscode';
import {ContinuityClipboard} from '../clipboard/continuityClipboard';
import {HandoffClient} from '../handoff/handoffClient';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {BoundaryStateStore} from '../state/boundaryState';
import {SessionBoundaryViewProvider} from '../views/sessionBoundaryView';

function workspaceFolder(): string {
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
}

export function registerSessionCommands(
  context: vscode.ExtensionContext,
  store: BoundaryStateStore,
  notifications: RateLimitedNotifications,
  view: SessionBoundaryViewProvider,
): vscode.Disposable[] {
  const handoff = new HandoffClient();
  const clipboard = new ContinuityClipboard();

  const sessionAudit = vscode.commands.registerCommand('aiDevOs.sessionAudit', async () => {
    const state = store.read();
    await notifications.info(
      'session-audit',
      `AI_DEV_OS boundary state: ${state.currentEnforcementState}`,
    );
    view.refresh();
  });

  const generateHandoff = vscode.commands.registerCommand('aiDevOs.generateHandoff', async () => {
    const result = await handoff.generate(workspaceFolder());
    await store.update({
      lastExportedContinuityBundle: result.copyReadyPrompt,
      pendingRolloverState: true,
      currentEnforcementState: 'ROLLOVER_REQUIRED',
      lastRolloverTimestamp: Date.now(),
    });
    await notifications.info('handoff-generated', 'AI_DEV_OS compact continuity generated.');
    view.refresh();
  });

  const copyContinuityBundle = vscode.commands.registerCommand(
    'aiDevOs.copyContinuityBundle',
    async () => {
      const state = store.read();
      const copied = await clipboard.copy(state.lastExportedContinuityBundle);
      if (copied) {
        await notifications.info('continuity-copied', 'AI_DEV_OS continuity bundle copied.');
      } else {
        await notifications.warn('clipboard-empty', 'AI_DEV_OS continuity bundle is not ready.');
      }
    },
  );

  const openNewSessionPrompt = vscode.commands.registerCommand(
    'aiDevOs.openNewSessionPrompt',
    async () => {
      const document = await vscode.workspace.openTextDocument({
        language: 'markdown',
        content: store.read().lastExportedContinuityBundle,
      });
      await vscode.window.showTextDocument(document, {preview: false});
    },
  );

  const confirmSessionRollover = vscode.commands.registerCommand(
    'aiDevOs.confirmSessionRollover',
    async () => {
      const state = store.read();
      await store.update({
        currentSessionGeneration: state.currentSessionGeneration + 1,
        currentEnforcementState: 'ACTIVE',
        pendingRolloverState: false,
        staleWarningCount: 0,
      });
      await notifications.info('rollover-confirmed', 'AI_DEV_OS session rollover confirmed.');
      view.refresh();
    },
  );

  const showBoundaryState = vscode.commands.registerCommand(
    'aiDevOs.showSessionBoundaryState',
    async () => {
      const state = store.read();
      await vscode.window.showInformationMessage(JSON.stringify(state, undefined, 2));
      view.refresh();
    },
  );

  const compactCurrentSession = vscode.commands.registerCommand(
    'aiDevOs.compactCurrentSession',
    async () => {
      await store.update({currentEnforcementState: 'WARNING', pendingRolloverState: true});
      await notifications.warn(
        'compact-required',
        'AI_DEV_OS compact continuity required before continuing this session.',
      );
      view.refresh();
    },
  );

  const showStaleWarning = vscode.commands.registerCommand(
    'aiDevOs.showStaleSessionWarning',
    async () => {
      const state = store.read();
      await store.update({
        staleWarningCount: state.staleWarningCount + 1,
        currentEnforcementState: 'STALE_BLOCKED',
        pendingRolloverState: true,
      });
      await notifications.warn(
        'stale-session',
        'AI_DEV_OS stale session detected. Start a human-confirmed rollover.',
      );
      view.refresh();
    },
  );

  return [
    sessionAudit,
    generateHandoff,
    copyContinuityBundle,
    openNewSessionPrompt,
    confirmSessionRollover,
    showBoundaryState,
    compactCurrentSession,
    showStaleWarning,
    vscode.window.registerTreeDataProvider('aiDevOsSessionBoundary', view),
  ];
}
