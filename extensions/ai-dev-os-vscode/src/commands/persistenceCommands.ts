import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {LocalPersistenceStore} from '../persistence/localPersistence';
import {BoundaryStateStore} from '../state/boundaryState';
import {SessionBoundaryViewProvider} from '../views/sessionBoundaryView';

export function registerPersistenceCommands(
  store: BoundaryStateStore,
  persistence: LocalPersistenceStore,
  notifications: RateLimitedNotifications,
  view: SessionBoundaryViewProvider,
): vscode.Disposable[] {
  const restoreSessionState = vscode.commands.registerCommand(
    'aiDevOs.restoreSessionState',
    async () => {
      const restored = await persistence.read();
      await store.update(persistence.toBoundaryState(restored));
      await notifications.info('persistence-restored', 'AI_DEV_OS local session state restored.');
      view.refresh();
    },
  );

  const showPersistenceState = vscode.commands.registerCommand(
    'aiDevOs.showPersistenceState',
    async () => {
      const state = await persistence.read();
      await vscode.window.showInformationMessage(JSON.stringify(state, undefined, 2));
    },
  );

  const cleanupStalePersistence = vscode.commands.registerCommand(
    'aiDevOs.cleanupStalePersistence',
    async () => {
      const state = await persistence.read();
      const cleaned = {...state, stale_warning_state: {stale_session_detected: false, warning_count: 0}};
      await persistence.write(cleaned);
      await store.update({staleWarningCount: 0});
      await notifications.info('persistence-cleaned', 'AI_DEV_OS stale persistence cleaned.');
      view.refresh();
    },
  );

  const exportLocalContinuityIndex = vscode.commands.registerCommand(
    'aiDevOs.exportLocalContinuityIndex',
    async () => {
      const state = await persistence.read();
      const document = await vscode.workspace.openTextDocument({
        language: 'json',
        content: JSON.stringify(
          {
            continuity_bundle_ids: Object.keys(state.last_continuity_bundle),
            generation: state.current_session_generation,
            prompt_mode: state.current_prompt_mode,
            summary_only: true,
          },
          undefined,
          2,
        ),
      });
      await vscode.window.showTextDocument(document, {preview: false});
    },
  );

  const resetLocalSessionState = vscode.commands.registerCommand(
    'aiDevOs.resetLocalSessionState',
    async () => {
      await persistence.reset();
      await store.update({
        currentSessionGeneration: 1,
        currentEnforcementState: 'ACTIVE',
        lastExportedContinuityBundle: '',
        pendingRolloverState: false,
        staleWarningCount: 0,
      });
      await notifications.info('persistence-reset', 'AI_DEV_OS local session state reset.');
      view.refresh();
    },
  );

  return [
    restoreSessionState,
    showPersistenceState,
    cleanupStalePersistence,
    exportLocalContinuityIndex,
    resetLocalSessionState,
  ];
}
