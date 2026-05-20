import * as fs from 'fs/promises';
import * as path from 'path';
import {LocalPersistenceStore} from './localPersistence';

export interface PersistenceGovernanceState {
  currentBudgetUsage: number;
  retentionPressure: 'low' | 'medium' | 'high';
  schemaCompatible: boolean;
  migrationRequired: boolean;
  quarantineDetected: boolean;
  checkpointRotationRequired: boolean;
  compactRecommendation: boolean;
}

export class PersistenceGovernance {
  constructor(private readonly persistence: LocalPersistenceStore) {}

  async validate(): Promise<PersistenceGovernanceState> {
    const state = await this.persistence.read();
    const schema = await this.readSchema();
    const checkpointCount = await this.countCheckpoints();
    const usage = JSON.stringify(state).length + JSON.stringify(schema).length + checkpointCount * 512;
    const pressure = usage >= 54000 ? 'high' : usage >= 41000 ? 'medium' : 'low';
    const compatible = ['1.0', '1.1'].includes(String(schema.schema_version ?? '1.1'));
    const quarantine = Boolean(schema.quarantine ?? state.stale_warning_state.stale_session_detected);
    return {
      currentBudgetUsage: usage,
      retentionPressure: pressure,
      schemaCompatible: compatible,
      migrationRequired: !compatible || Boolean(schema.migration_required),
      quarantineDetected: quarantine,
      checkpointRotationRequired: checkpointCount > 5,
      compactRecommendation: pressure !== 'low' || quarantine,
    };
  }

  async rotateCheckpoints(): Promise<number> {
    const checkpointDir = path.join(this.persistence.storageDir(), 'checkpoints');
    await fs.mkdir(checkpointDir, {recursive: true});
    const entries = (await fs.readdir(checkpointDir)).sort().reverse();
    const expired = entries.slice(5);
    await Promise.all(expired.map((entry) => fs.rm(path.join(checkpointDir, entry), {force: true})));
    return expired.length;
  }

  async migrate(): Promise<PersistenceGovernanceState> {
    const schemaDir = path.join(this.persistence.storageDir(), 'schema');
    await fs.mkdir(schemaDir, {recursive: true});
    await fs.writeFile(
      path.join(schemaDir, 'migration-state.json'),
      JSON.stringify({migration_required: false, quarantine: false, summary_only: true}, undefined, 2),
    );
    return this.validate();
  }

  private async readSchema(): Promise<Record<string, unknown>> {
    try {
      const raw = await fs.readFile(
        path.join(this.persistence.storageDir(), 'schema', 'schema-version.json'),
        'utf8',
      );
      return JSON.parse(raw) as Record<string, unknown>;
    } catch {
      return {schema_version: '1.1', summary_only: true};
    }
  }

  private async countCheckpoints(): Promise<number> {
    try {
      return (await fs.readdir(path.join(this.persistence.storageDir(), 'checkpoints'))).length;
    } catch {
      return 0;
    }
  }
}
