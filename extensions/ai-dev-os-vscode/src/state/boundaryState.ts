import * as vscode from 'vscode';

export type EnforcementState = 'ACTIVE' | 'WARNING' | 'ROLLOVER_REQUIRED' | 'STALE_BLOCKED';

export interface BoundaryState {
  currentSessionGeneration: number;
  lastRolloverTimestamp: number;
  currentEnforcementState: EnforcementState;
  lastExportedContinuityBundle: string;
  staleWarningCount: number;
  pendingRolloverState: boolean;
}

const stateKey = 'aiDevOs.sessionBoundaryState';

export class BoundaryStateStore {
  constructor(private readonly context: vscode.ExtensionContext) {}

  read(): BoundaryState {
    return this.context.globalState.get<BoundaryState>(stateKey, {
      currentSessionGeneration: 1,
      lastRolloverTimestamp: 0,
      currentEnforcementState: 'ACTIVE',
      lastExportedContinuityBundle: '',
      staleWarningCount: 0,
      pendingRolloverState: false,
    });
  }

  async update(next: Partial<BoundaryState>): Promise<BoundaryState> {
    const merged = {...this.read(), ...next};
    await this.context.globalState.update(stateKey, merged);
    return merged;
  }
}
