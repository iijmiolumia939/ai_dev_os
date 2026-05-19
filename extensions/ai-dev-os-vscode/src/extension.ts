import * as vscode from 'vscode';
import {registerSessionCommands} from './commands/sessionCommands';
import {RateLimitedNotifications} from './notifications/rateLimitedNotifications';
import {BoundaryStateStore} from './state/boundaryState';
import {SessionBoundaryViewProvider} from './views/sessionBoundaryView';

export function activate(context: vscode.ExtensionContext): void {
  const store = new BoundaryStateStore(context);
  const notifications = new RateLimitedNotifications(vscode.window);
  const view = new SessionBoundaryViewProvider(store);
  context.subscriptions.push(...registerSessionCommands(context, store, notifications, view));
}

export function deactivate(): void {
  return;
}
