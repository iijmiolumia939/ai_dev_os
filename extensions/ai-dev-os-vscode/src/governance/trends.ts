import * as vscode from 'vscode';
import {GovernanceHealthMonitor, GovernanceHealthState} from './health';

export type GovernanceTrendLevel = 'IMPROVING' | 'STABLE' | 'DEGRADING' | 'OSCILLATING';

export interface GovernanceTrendState {
  trendLevel: GovernanceTrendLevel;
  activeWindowSize: number;
  evictedSnapshots: number;
  driftDetected: boolean;
  regressionDetected: boolean;
  oscillationDetected: boolean;
  dashboardDelta: string[];
  boundedWindowMaintained: boolean;
  summaryOnly: boolean;
  automaticActionAllowed: false;
}

export class GovernanceTrendMonitor {
  private snapshots: GovernanceHealthState[] = [];

  constructor(private readonly health: GovernanceHealthMonitor, private readonly maxWindowSize = 5) {}

  async evaluate(): Promise<GovernanceTrendState> {
    const current = await this.health.evaluate();
    this.snapshots.push(current);
    const evicted = Math.max(0, this.snapshots.length - this.maxWindowSize);
    this.snapshots = this.snapshots.slice(-this.maxWindowSize);
    const previous = this.snapshots.length > 1 ? this.snapshots[this.snapshots.length - 2] : current;
    const scoreDelta = current.healthScore - previous.healthScore;
    const oscillation = this.oscillating();
    const trendLevel = oscillation ? 'OSCILLATING' : scoreDelta < -5 ? 'DEGRADING' : scoreDelta > 5 ? 'IMPROVING' : 'STABLE';
    return {
      trendLevel,
      activeWindowSize: this.snapshots.length,
      evictedSnapshots: evicted,
      driftDetected: trendLevel === 'DEGRADING',
      regressionDetected: current.level === 'HIGH_PRESSURE' || current.level === 'CRITICAL',
      oscillationDetected: oscillation,
      dashboardDelta: [
        `health:${scoreDelta}`,
        `pressure:${previous.pressure}->${current.pressure}`,
        `checkpoint:${previous.checkpointPressure}->${current.checkpointPressure}`,
        `architecture:${previous.architectureIsolationState}->${current.architectureIsolationState}`,
      ],
      boundedWindowMaintained: this.snapshots.length <= this.maxWindowSize,
      summaryOnly: true,
      automaticActionAllowed: false,
    };
  }

  compactWindow(): void {
    this.snapshots = this.snapshots.slice(-2);
  }

  resetWindow(): void {
    this.snapshots = [];
  }

  private oscillating(): boolean {
    if (this.snapshots.length < 4) {
      return false;
    }
    const levels = this.snapshots.map((item) => item.healthScore);
    const directions = levels.slice(1).map((score, index) => Math.sign(score - levels[index])).filter(Boolean);
    return directions.length >= 3 && directions.every((direction, index) => index === 0 || direction !== directions[index - 1]);
  }
}

export class GovernanceTrendStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 89);

  constructor(private readonly monitor: GovernanceTrendMonitor) {
    this.item.command = 'aiDevOs.showGovernanceTrends';
  }

  async refresh(): Promise<GovernanceTrendState> {
    const state = await this.monitor.evaluate();
    this.item.text = `AI_DEV_OS Trend ${state.trendLevel}`;
    this.item.tooltip = `Window ${state.activeWindowSize}; drift ${state.driftDetected}; regression ${state.regressionDetected}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
