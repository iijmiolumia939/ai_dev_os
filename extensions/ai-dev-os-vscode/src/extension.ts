import * as vscode from 'vscode';
import {registerPersistenceCommands} from './commands/persistenceCommands';
import {registerSessionCommands} from './commands/sessionCommands';
import {RateLimitedNotifications} from './notifications/rateLimitedNotifications';
import {LocalPersistenceStore} from './persistence/localPersistence';
import {BoundaryStateStore} from './state/boundaryState';
import {SessionBoundaryViewProvider} from './views/sessionBoundaryView';

export async function activate(context: vscode.ExtensionContext): Promise<void> {
  const store = new BoundaryStateStore(context);
  const notifications = new RateLimitedNotifications(vscode.window);
  const view = new SessionBoundaryViewProvider(store);
  const persistence = new LocalPersistenceStore();
  await persistence.ensure();
  const restored = await persistence.read();
  await store.update(persistence.toBoundaryState(restored));
  if (restored.rollover_state.rollover_pending || restored.stale_warning_state.stale_session_detected) {
    await notifications.warn(
      'startup-persistence-warning',
      'AI_DEV_OS restored a pending rollover or stale session warning from local persistence.',
    );
  } else if (Object.keys(restored.last_continuity_bundle).length > 0) {
    await notifications.info(
      'startup-continuity-restored',
      'AI_DEV_OS compact continuity is available from local persistence.',
    );
  }
  context.subscriptions.push(...registerSessionCommands(context, store, notifications, view));
  context.subscriptions.push(
    ...registerPersistenceCommands(store, persistence, notifications, view),
  );
}

export function deactivate(): void {
  return;
}
