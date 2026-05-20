import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {PersistenceGovernance} from '../persistence/governance';
import {LocalPersistenceStore} from '../persistence/localPersistence';
import {SessionBoundaryViewProvider} from '../views/sessionBoundaryView';

export function registerGovernanceCommands(
  persistence: LocalPersistenceStore,
  governance: PersistenceGovernance,
  notifications: RateLimitedNotifications,
  view: SessionBoundaryViewProvider,
): vscode.Disposable[] {
  const showBudget = vscode.commands.registerCommand('aiDevOs.showPersistenceBudget', async () => {
    const state = await governance.validate();
    await vscode.window.showInformationMessage(JSON.stringify(state, undefined, 2));
  });

  const rotateCheckpoints = vscode.commands.registerCommand('aiDevOs.rotateCheckpoints', async () => {
    const expired = await governance.rotateCheckpoints();
    await notifications.info('checkpoint-rotation', `AI_DEV_OS rotated ${expired} checkpoints.`);
    view.refresh();
  });

  const validateSchema = vscode.commands.registerCommand(
    'aiDevOs.validatePersistenceSchema',
    async () => {
      const state = await governance.validate();
      if (!state.schemaCompatible || state.quarantineDetected) {
        await notifications.warn(
          'schema-validation-warning',
          'AI_DEV_OS persistence schema needs migration or quarantine review.',
        );
      } else {
        await notifications.info('schema-validation-ok', 'AI_DEV_OS persistence schema is compatible.');
      }
    },
  );

  const migrateLocalPersistence = vscode.commands.registerCommand(
    'aiDevOs.migrateLocalPersistence',
    async () => {
      await governance.migrate();
      await notifications.info('schema-migrated', 'AI_DEV_OS local persistence migration completed.');
    },
  );

  const cleanupExpiredContinuity = vscode.commands.registerCommand(
    'aiDevOs.cleanupExpiredContinuity',
    async () => {
      await persistence.write({
        ...(await persistence.read()),
        stale_warning_state: {stale_session_detected: false, warning_count: 0},
      });
      await notifications.info('expired-continuity-cleaned', 'AI_DEV_OS expired continuity cleaned.');
    },
  );

  return [
    showBudget,
    rotateCheckpoints,
    validateSchema,
    migrateLocalPersistence,
    cleanupExpiredContinuity,
  ];
}
