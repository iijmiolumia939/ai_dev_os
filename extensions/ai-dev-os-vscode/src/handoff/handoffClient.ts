import {execFile} from 'child_process';
import {promisify} from 'util';
import * as vscode from 'vscode';

const execFileAsync = promisify(execFile);

export interface HandoffResult {
  copyReadyPrompt: string;
  raw: string;
}

export class HandoffClient {
  async generate(workspaceFolder: string): Promise<HandoffResult> {
    const pythonCommand = vscode.workspace
      .getConfiguration('aiDevOs')
      .get<string>('pythonCommand', 'python');
    const {stdout} = await execFileAsync(
      pythonCommand,
      ['-m', 'ai_dev_os.cli', 'session-boundary-handoff', '--workspace', workspaceFolder, '--json'],
      {cwd: workspaceFolder, timeout: 15000, windowsHide: true},
    );
    const data = JSON.parse(stdout) as {copy_ready_prompt?: string};
    return {copyReadyPrompt: data.copy_ready_prompt ?? stdout, raw: stdout};
  }
}
