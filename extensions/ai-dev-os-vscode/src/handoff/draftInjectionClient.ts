import {execFile} from 'child_process';
import {promisify} from 'util';
import * as vscode from 'vscode';

const execFileAsync = promisify(execFile);

export interface BootstrapDraftPreview {
  estimated_token_size: number;
  included_continuity: string[];
  excluded_stale_context: string[];
  sprint_focus: string;
  architecture_isolation: string;
  enter_ready_state: string;
  waiting_for_send_state: string;
}

export interface BootstrapDraftResult {
  chat_opened: boolean;
  draft_prefilled: boolean;
  continuity_injected: boolean;
  awaiting_human_send: boolean;
  draft_text: string;
  preview: BootstrapDraftPreview;
  target: string;
  clipboard_fallback_active: boolean;
  auto_send: boolean;
  hidden_continuation: boolean;
  background_message_dispatch: boolean;
  silent_prompt_mutation: boolean;
  authority_escalation_used: boolean;
  status_bar_states: string[];
  warnings: string[];
  raw: string;
}

export class DraftInjectionClient {
  async generate(workspaceFolder: string): Promise<BootstrapDraftResult> {
    const pythonCommand = vscode.workspace
      .getConfiguration('aiDevOs')
      .get<string>('pythonCommand', 'python');
    const {stdout} = await execFileAsync(
      pythonCommand,
      ['-m', 'ai_dev_os.cli', 'bootstrap-draft', '--workspace', workspaceFolder, '--json'],
      {cwd: workspaceFolder, timeout: 15000, windowsHide: true},
    );
    const data = JSON.parse(stdout) as Omit<BootstrapDraftResult, 'raw'>;
    return {...data, raw: stdout};
  }
}
