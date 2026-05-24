import * as vscode from 'vscode';

export interface RegistrationConflict {
  readonly kind: 'command' | 'status';
  readonly key: string;
  readonly firstOwner: string;
  readonly secondOwner: string;
}

export interface RegistrationProjection {
  readonly accepted: number;
  readonly skipped: number;
  readonly conflicts: readonly RegistrationConflict[];
  readonly namespaceViolations: readonly string[];
  readonly budgetExceeded: boolean;
  readonly terminationTriggered: boolean;
  readonly deterministicOrdering: boolean;
}

export interface CommandRegistrationEntry {
  readonly order: number;
  readonly namespace: string;
  readonly commandIds: readonly string[];
  readonly register: () => readonly vscode.Disposable[];
}

export interface StatusBarRegistrationEntry {
  readonly order: number;
  readonly namespace: string;
  readonly statusId: string;
  readonly disposable: vscode.Disposable;
}

export class RegistrationConflictGuard {
  private readonly owners = new Map<string, string>();
  private readonly conflicts: RegistrationConflict[] = [];

  accept(kind: 'command' | 'status', key: string, owner: string): boolean {
    const scopedKey = `${kind}:${key}`;
    const firstOwner = this.owners.get(scopedKey);
    if (firstOwner !== undefined) {
      this.conflicts.push({kind, key, firstOwner, secondOwner: owner});
      return false;
    }
    this.owners.set(scopedKey, owner);
    return true;
  }

  snapshot(): readonly RegistrationConflict[] {
    return [...this.conflicts];
  }
}

export class RegistrationNamespaceGuard {
  private readonly violations: string[] = [];

  acceptCommand(commandId: string, owner: string): boolean {
    if (commandId.startsWith('aiDevOs.')) {
      return true;
    }
    this.violations.push(`${owner}:${commandId}`);
    return false;
  }

  acceptStatus(statusId: string, owner: string): boolean {
    if (statusId.startsWith('AI_DEV_OS ')) {
      return true;
    }
    this.violations.push(`${owner}:${statusId}`);
    return false;
  }

  snapshot(): readonly string[] {
    return [...this.violations];
  }
}

export class RegistrationBudgetGuard {
  constructor(
    private readonly maxCommands = 360,
    private readonly maxStatusBars = 240,
    private readonly maxGroups = 96,
  ) {}

  withinCommandBudget(commandCount: number, groupCount: number): boolean {
    return commandCount <= this.maxCommands && groupCount <= this.maxGroups;
  }

  withinStatusBudget(statusCount: number): boolean {
    return statusCount <= this.maxStatusBars;
  }
}

export class RegistrationTerminationGuard {
  constructor(private readonly maxSkipped = 16) {}

  shouldTerminate(skipped: number, budgetExceeded: boolean): boolean {
    return budgetExceeded || skipped > this.maxSkipped;
  }
}

export class CommandRegistrationRegistry {
  private projection: RegistrationProjection = emptyProjection();

  constructor(
    private readonly conflictGuard = new RegistrationConflictGuard(),
    private readonly namespaceGuard = new RegistrationNamespaceGuard(),
    private readonly budgetGuard = new RegistrationBudgetGuard(),
    private readonly terminationGuard = new RegistrationTerminationGuard(),
  ) {}

  register(entries: readonly CommandRegistrationEntry[]): readonly vscode.Disposable[] {
    const ordered = deterministicOrder(entries);
    const commandCount = ordered.reduce((total, entry) => total + entry.commandIds.length, 0);
    const budgetExceeded = !this.budgetGuard.withinCommandBudget(commandCount, ordered.length);
    const disposables: vscode.Disposable[] = [];
    let accepted = 0;
    let skipped = 0;

    for (const entry of ordered) {
      const namespaceSafe = entry.commandIds.every((commandId) =>
        this.namespaceGuard.acceptCommand(commandId, entry.namespace),
      );
      const conflictSafe = entry.commandIds.every((commandId) =>
        this.conflictGuard.accept('command', commandId, entry.namespace),
      );
      if (!namespaceSafe || !conflictSafe || budgetExceeded) {
        skipped += 1;
        if (this.terminationGuard.shouldTerminate(skipped, budgetExceeded)) {
          break;
        }
        continue;
      }
      disposables.push(...entry.register());
      accepted += entry.commandIds.length;
    }

    this.projection = {
      accepted,
      skipped,
      conflicts: this.conflictGuard.snapshot(),
      namespaceViolations: this.namespaceGuard.snapshot(),
      budgetExceeded,
      terminationTriggered: this.terminationGuard.shouldTerminate(skipped, budgetExceeded),
      deterministicOrdering: hasDeterministicOrder(ordered),
    };
    return disposables;
  }

  snapshot(): RegistrationProjection {
    return this.projection;
  }
}

export class StatusBarRegistrationRegistry {
  private projection: RegistrationProjection = emptyProjection();

  constructor(
    private readonly conflictGuard = new RegistrationConflictGuard(),
    private readonly namespaceGuard = new RegistrationNamespaceGuard(),
    private readonly budgetGuard = new RegistrationBudgetGuard(),
    private readonly terminationGuard = new RegistrationTerminationGuard(),
  ) {}

  register(entries: readonly StatusBarRegistrationEntry[]): readonly vscode.Disposable[] {
    const ordered = deterministicOrder(entries);
    const budgetExceeded = !this.budgetGuard.withinStatusBudget(ordered.length);
    const disposables: vscode.Disposable[] = [];
    let accepted = 0;
    let skipped = 0;

    for (const entry of ordered) {
      const namespaceSafe = this.namespaceGuard.acceptStatus(entry.statusId, entry.namespace);
      const conflictSafe = this.conflictGuard.accept('status', entry.statusId, entry.namespace);
      if (!namespaceSafe || !conflictSafe || budgetExceeded) {
        skipped += 1;
        if (this.terminationGuard.shouldTerminate(skipped, budgetExceeded)) {
          break;
        }
        continue;
      }
      disposables.push(entry.disposable);
      accepted += 1;
    }

    this.projection = {
      accepted,
      skipped,
      conflicts: this.conflictGuard.snapshot(),
      namespaceViolations: this.namespaceGuard.snapshot(),
      budgetExceeded,
      terminationTriggered: this.terminationGuard.shouldTerminate(skipped, budgetExceeded),
      deterministicOrdering: hasDeterministicOrder(ordered),
    };
    return disposables;
  }

  snapshot(): RegistrationProjection {
    return this.projection;
  }
}

function deterministicOrder<T extends {readonly order: number; readonly namespace: string}>(
  entries: readonly T[],
): T[] {
  return [...entries].sort((left, right) => left.order - right.order || left.namespace.localeCompare(right.namespace));
}

function hasDeterministicOrder<T extends {readonly order: number}>(entries: readonly T[]): boolean {
  return entries.every((entry, index) => index === 0 || entries[index - 1].order <= entry.order);
}

function emptyProjection(): RegistrationProjection {
  return {
    accepted: 0,
    skipped: 0,
    conflicts: [],
    namespaceViolations: [],
    budgetExceeded: false,
    terminationTriggered: false,
    deterministicOrdering: true,
  };
}