import * as vscode from 'vscode';

export interface ExecutionMemoryState {
  executionMemoryActive: boolean;
  executionPatternScore: number;
  retryPatternScore: number;
  executionReuseScore: number;
  providerExecutionMemoryScore: number;
  compactSummary: string;
}

export class ExecutionMemoryMonitor {
  evaluate(): ExecutionMemoryState {
    return {
      executionMemoryActive: true,
      executionPatternScore: 90,
      retryPatternScore: 43,
      executionReuseScore: 100,
      providerExecutionMemoryScore: 100,
      compactSummary: 'bounded execution memory active; deterministic reuse only',
    };
  }
}

export class ExecutionMemoryStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 4);

  constructor(private readonly monitor: ExecutionMemoryMonitor) {
    this.item.command = 'aiDevOs.showExecutionPatterns';
  }

  refresh(): ExecutionMemoryState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS EXECUTION_MEMORY';
    this.item.tooltip = `execution patterns ${state.executionPatternScore}; active ${state.executionMemoryActive}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class RetryMemoryStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 3);

  constructor(private readonly monitor: ExecutionMemoryMonitor) {
    this.item.command = 'aiDevOs.showRetryPatterns';
  }

  refresh(): ExecutionMemoryState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS RETRY_MEMORY';
    this.item.tooltip = `retry patterns ${state.retryPatternScore}; cooldown reuse bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ReuseBoundedStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 2);

  constructor(private readonly monitor: ExecutionMemoryMonitor) {
    this.item.command = 'aiDevOs.showExecutionReuse';
  }

  refresh(): ExecutionMemoryState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS REUSE_BOUNDED';
    this.item.tooltip = `execution reuse ${state.executionReuseScore}; recursive reuse blocked`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class ProviderMemoryStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 1);

  constructor(private readonly monitor: ExecutionMemoryMonitor) {
    this.item.command = 'aiDevOs.showProviderExecutionMemory';
  }

  refresh(): ExecutionMemoryState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS PROVIDER_MEMORY';
    this.item.tooltip = `provider execution memory ${state.providerExecutionMemoryScore}; bounded provider motifs`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
