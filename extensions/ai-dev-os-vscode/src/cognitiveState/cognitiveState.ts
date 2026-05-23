import * as vscode from 'vscode';

export interface CognitiveState {
  cognitiveStateActive: boolean;
  cognitiveLoad: string;
  attentionFocus: string;
  memoryPressure: string;
  attentionDistribution: string[];
  decayStatus: string;
  compactSummary: string;
}

export class CognitiveStateMonitor {
  evaluate(): CognitiveState {
    return {
      cognitiveStateActive: true,
      cognitiveLoad: 'COGNITIVE_LOAD MEDIUM',
      attentionFocus: 'implementation',
      memoryPressure: 'MEDIUM',
      attentionDistribution: ['implementation:34', 'tests:27', 'validation:24', 'vscode:15'],
      decayStatus: 'STABLE',
      compactSummary: 'bounded cognitive state active; local-first cognition only',
    };
  }
}

export class CognitiveLoadStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 19);

  constructor(private readonly monitor: CognitiveStateMonitor) {
    this.item.command = 'aiDevOs.showCognitiveState';
  }

  refresh(): CognitiveState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS COGNITIVE_LOAD';
    this.item.tooltip = `${state.cognitiveLoad}; decay ${state.decayStatus}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class AttentionFocusStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 18);

  constructor(private readonly monitor: CognitiveStateMonitor) {
    this.item.command = 'aiDevOs.showAttentionFocus';
  }

  refresh(): CognitiveState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS ATTENTION_FOCUS';
    this.item.tooltip = `focus ${state.attentionFocus}; ${state.attentionDistribution.join(', ')}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}

export class CognitiveStateMemoryPressureStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 17);

  constructor(private readonly monitor: CognitiveStateMonitor) {
    this.item.command = 'aiDevOs.showCognitiveMemoryPressure';
  }

  refresh(): CognitiveState {
    const state = this.monitor.evaluate();
    this.item.text = 'AI_DEV_OS MEMORY_PRESSURE';
    this.item.tooltip = `working memory pressure ${state.memoryPressure}; local patch bounded`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}