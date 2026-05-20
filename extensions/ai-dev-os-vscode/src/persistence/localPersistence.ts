import * as fs from 'fs/promises';
import * as path from 'path';
import * as vscode from 'vscode';
import {BoundaryState} from '../state/boundaryState';

export interface PersistenceState {
  current_session_generation: number;
  rollover_state: Record<string, unknown>;
  last_continuity_bundle: Record<string, unknown>;
  current_prompt_mode: string;
  session_focus: string;
  stale_warning_state: Record<string, unknown>;
  repository_subset_summary: string[];
  compact_continuity_metadata: Record<string, unknown>;
  summary_only: boolean;
  bounded: boolean;
}

const defaultState: PersistenceState = {
  current_session_generation: 1,
  rollover_state: {rollover_pending: false},
  last_continuity_bundle: {},
  current_prompt_mode: 'bounded_implementation',
  session_focus: 'bounded-implementation',
  stale_warning_state: {stale_session_detected: false, warning_count: 0},
  repository_subset_summary: [],
  compact_continuity_metadata: {},
  summary_only: true,
  bounded: true,
};

export function workspaceRoot(): string {
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
}

export class LocalPersistenceStore {
  constructor(private readonly root = workspaceRoot()) {}

  storageDir(): string {
    return path.join(this.root, '.ai-dev-os');
  }

  sessionBoundaryPath(): string {
    return path.join(this.storageDir(), 'session-boundary.json');
  }

  async ensure(): Promise<void> {
    await fs.mkdir(path.join(this.storageDir(), 'checkpoints'), {recursive: true});
  }

  async read(): Promise<PersistenceState> {
    try {
      const raw = await fs.readFile(this.sessionBoundaryPath(), 'utf8');
      return {...defaultState, ...JSON.parse(raw)} as PersistenceState;
    } catch {
      return defaultState;
    }
  }

  async write(state: PersistenceState): Promise<void> {
    await this.ensure();
    await fs.writeFile(this.sessionBoundaryPath(), JSON.stringify(this.bound(state), undefined, 2));
  }

  async reset(): Promise<void> {
    await this.ensure();
    await this.write(defaultState);
  }

  toBoundaryState(state: PersistenceState): Partial<BoundaryState> {
    return {
      currentSessionGeneration: state.current_session_generation,
      currentEnforcementState: state.rollover_state.rollover_pending
        ? 'ROLLOVER_REQUIRED'
        : 'ACTIVE',
      lastExportedContinuityBundle: JSON.stringify(state.last_continuity_bundle, undefined, 2),
      pendingRolloverState: Boolean(state.rollover_state.rollover_pending),
      staleWarningCount: Number(state.stale_warning_state.warning_count ?? 0),
    };
  }

  private bound(state: PersistenceState): PersistenceState {
    return {
      ...state,
      repository_subset_summary: state.repository_subset_summary.slice(0, 5),
      summary_only: true,
      bounded: true,
    };
  }
}
