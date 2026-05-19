import * as vscode from 'vscode';

export class ContinuityClipboard {
  async copy(text: string): Promise<boolean> {
    if (!text) {
      return false;
    }
    await vscode.env.clipboard.writeText(text);
    return true;
  }
}
