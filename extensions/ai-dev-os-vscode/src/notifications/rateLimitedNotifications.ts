import * as vscode from 'vscode';

export class RateLimitedNotifications {
  private readonly emitted = new Map<string, number>();

  constructor(private readonly window: typeof vscode.window, private readonly minIntervalMs = 30000) {}

  async warn(key: string, message: string): Promise<boolean> {
    const now = Date.now();
    const previous = this.emitted.get(key) ?? 0;
    if (now - previous < this.minIntervalMs) {
      return false;
    }
    this.emitted.set(key, now);
    await this.window.showWarningMessage(message);
    return true;
  }

  async info(key: string, message: string): Promise<boolean> {
    const now = Date.now();
    const previous = this.emitted.get(key) ?? 0;
    if (now - previous < this.minIntervalMs) {
      return false;
    }
    this.emitted.set(key, now);
    await this.window.showInformationMessage(message);
    return true;
  }
}
