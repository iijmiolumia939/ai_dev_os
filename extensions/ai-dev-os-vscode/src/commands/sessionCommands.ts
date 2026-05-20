import * as vscode from 'vscode';
import {ContinuityClipboard} from '../clipboard/continuityClipboard';
import {BootstrapDraftResult, DraftInjectionClient} from '../handoff/draftInjectionClient';
import {HandoffClient} from '../handoff/handoffClient';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {BoundaryStateStore} from '../state/boundaryState';
import {SessionBoundaryViewProvider} from '../views/sessionBoundaryView';

function workspaceFolder(): string {
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
}

const chatOpenCommand = 'workbench.action.chat.open';
const newChatCommand = 'workbench.action.chat.newChat';
const enterReadyState = 'AI_DEV_OS ENTER_READY';
const waitingForSendState = 'AI_DEV_OS WAITING_FOR_SEND';

function previewText(result: BootstrapDraftResult): string {
  return [
    'AI_DEV_OS Bootstrap Draft Preview',
    `Estimated tokens: ${result.preview.estimated_token_size}`,
    `Target: ${result.target}`,
    `Awaiting human send: ${result.awaiting_human_send}`,
    '',
    'Included continuity:',
    ...result.preview.included_continuity.map(item => `- ${item}`),
    '',
    'Excluded stale context:',
    ...result.preview.excluded_stale_context.map(item => `- ${item}`),
    '',
    'Sprint focus:',
    result.preview.sprint_focus,
    '',
    'Architecture isolation:',
    result.preview.architecture_isolation,
    '',
    'Draft:',
    result.draft_text,
  ].join('\n');
}

export function registerSessionCommands(
  context: vscode.ExtensionContext,
  store: BoundaryStateStore,
  notifications: RateLimitedNotifications,
  view: SessionBoundaryViewProvider,
): vscode.Disposable[] {
  const handoff = new HandoffClient();
  const drafts = new DraftInjectionClient();
  const clipboard = new ContinuityClipboard();
  const enterOnlyStatus = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 90);
  enterOnlyStatus.text = enterReadyState;
  enterOnlyStatus.tooltip = 'Bootstrap draft ready; press Enter/Send manually in chat.';
  enterOnlyStatus.show();

  const openDraftInChat = async (result: BootstrapDraftResult): Promise<boolean> => {
    enterOnlyStatus.text = result.preview.enter_ready_state || enterReadyState;
    try {
      try {
        await vscode.commands.executeCommand(newChatCommand);
      } catch {
        // 古い VS Code でも、表示中の chat surface への prefill は継続する。
      }
      await vscode.commands.executeCommand(chatOpenCommand, {
        query: result.draft_text,
        isPartialQuery: true,
      });
      enterOnlyStatus.text = result.preview.waiting_for_send_state || waitingForSendState;
      return true;
    } catch {
      await clipboard.copy(result.draft_text);
      enterOnlyStatus.text = result.preview.waiting_for_send_state || waitingForSendState;
      return false;
    }
  };

  const generateBootstrapDraft = async (): Promise<BootstrapDraftResult> => {
    const result = await drafts.generate(workspaceFolder());
    await store.update({
      lastExportedContinuityBundle: result.draft_text,
      pendingRolloverState: true,
      currentEnforcementState: 'ROLLOVER_REQUIRED',
      lastRolloverTimestamp: Date.now(),
    });
    return result;
  };

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

  const startNewSprintSession = vscode.commands.registerCommand(
    'aiDevOs.startNewSprintSession',
    async () => {
      const result = await generateBootstrapDraft();
      const opened = await openDraftInChat(result);
      if (opened) {
        await notifications.info(
          'bootstrap-draft-opened',
          'AI_DEV_OS bootstrap draft is open. Press Enter/Send when ready.',
        );
      } else {
        await notifications.warn(
          'bootstrap-draft-clipboard-fallback',
          'AI_DEV_OS bootstrap draft copied because chat prefill was unavailable.',
        );
      }
      view.refresh();
    },
  );

  const openBootstrapChat = vscode.commands.registerCommand(
    'aiDevOs.openBootstrapChat',
    async () => {
      const result = await generateBootstrapDraft();
      await openDraftInChat(result);
      view.refresh();
    },
  );

  const previewBootstrapDraft = vscode.commands.registerCommand(
    'aiDevOs.previewBootstrapDraft',
    async () => {
      const result = await generateBootstrapDraft();
      const document = await vscode.workspace.openTextDocument({
        language: 'markdown',
        content: previewText(result),
      });
      await vscode.window.showTextDocument(document, {preview: false});
      view.refresh();
    },
  );

  const retryDraftInjection = vscode.commands.registerCommand(
    'aiDevOs.retryDraftInjection',
    async () => {
      const result = await generateBootstrapDraft();
      await openDraftInChat(result);
      await notifications.info(
        'bootstrap-draft-retry',
        'AI_DEV_OS bootstrap draft injection retried; final send remains manual.',
      );
      view.refresh();
    },
  );

  const showEnterOnlyState = vscode.commands.registerCommand(
    'aiDevOs.showEnterOnlyState',
    async () => {
      await vscode.window.showInformationMessage(enterOnlyStatus.text);
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
    startNewSprintSession,
    openBootstrapChat,
    previewBootstrapDraft,
    retryDraftInjection,
    showEnterOnlyState,
    compactCurrentSession,
    showStaleWarning,
    enterOnlyStatus,
    vscode.window.registerTreeDataProvider('aiDevOsSessionBoundary', view),
  ];
}
