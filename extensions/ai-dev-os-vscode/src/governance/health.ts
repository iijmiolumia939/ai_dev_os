import * as vscode from 'vscode';
import {PersistenceGovernance} from '../persistence/governance';
import {LocalPersistenceStore} from '../persistence/localPersistence';

export type GovernanceLevel = 'HEALTHY' | 'WARNING' | 'HIGH_PRESSURE' | 'CRITICAL';

export interface GovernanceHealthState {
  level: GovernanceLevel;
  healthScore: number;
  pressure: 'low' | 'medium' | 'high' | 'critical';
  dominantPressure: string;
  highestRisk: string;
  activeWarnings: string[];
  staleSessionActive: boolean;
  checkpointPressure: 'low' | 'medium' | 'high';
  retrievalExplosionWarning: boolean;
  architectureIsolationState: 'recommended' | 'not_required';
  workspaceCleanliness: 'clean' | 'review';
  rolloutStability: 'stable' | 'watch';
  summaryOnly: boolean;
  automaticActionAllowed: false;
}

export class GovernanceHealthMonitor {
  constructor(
    private readonly persistence: LocalPersistenceStore,
    private readonly persistenceGovernance: PersistenceGovernance,
  ) {}

  async evaluate(): Promise<GovernanceHealthState> {
    const state = await this.persistence.read();
    const governance = await this.persistenceGovernance.validate();
    const pressure = this.pressureFor(governance.retentionPressure);
    const stale = Boolean(state.stale_warning_state.stale_session_detected);
    const checkpointPressure = governance.checkpointRotationRequired ? 'high' : 'low';
    const activeWarnings: string[] = [];
    if (pressure !== 'low') {
      activeWarnings.push(`persistence pressure ${pressure}`);
    }
    if (stale) {
      activeWarnings.push('stale session state');
    }
    if (governance.checkpointRotationRequired) {
      activeWarnings.push('checkpoint pressure high');
    }
    if (governance.migrationRequired || governance.quarantineDetected) {
      activeWarnings.push('schema review needed');
    }
    const riskPenalty = activeWarnings.length * 12 + (pressure === 'critical' ? 22 : 0);
    const score = Math.max(0, Math.min(100, 100 - riskPenalty));
    return {
      level: this.levelFor(score, activeWarnings.length),
      healthScore: score,
      pressure,
      dominantPressure: governance.checkpointRotationRequired ? 'checkpoint' : 'persistence',
      highestRisk: stale ? 'stale_continuity' : governance.migrationRequired ? 'schema_migration' : 'none',
      activeWarnings,
      staleSessionActive: stale,
      checkpointPressure,
      retrievalExplosionWarning: false,
      architectureIsolationState: stale ? 'recommended' : 'not_required',
      workspaceCleanliness: 'clean',
      rolloutStability: 'stable',
      summaryOnly: true,
      automaticActionAllowed: false,
    };
  }

  async compactRecommendation(): Promise<GovernanceHealthState> {
    return this.evaluate();
  }

  private pressureFor(value: 'low' | 'medium' | 'high'): 'low' | 'medium' | 'high' | 'critical' {
    return value;
  }

  private levelFor(score: number, warningCount: number): GovernanceLevel {
    if (score <= 35 || warningCount >= 5) {
      return 'CRITICAL';
    }
    if (score <= 55 || warningCount >= 3) {
      return 'HIGH_PRESSURE';
    }
    if (score <= 80 || warningCount > 0) {
      return 'WARNING';
    }
    return 'HEALTHY';
  }
}

export class GovernanceStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 90);

  constructor(private readonly monitor: GovernanceHealthMonitor) {
    this.item.command = 'aiDevOs.showGovernanceDashboard';
  }

  async refresh(): Promise<GovernanceHealthState> {
    const state = await this.monitor.evaluate();
    this.item.text = `AI_DEV_OS ${state.level}`;
    this.item.tooltip = `Governance health ${state.healthScore}; pressure ${state.pressure}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}
