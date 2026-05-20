import * as vscode from 'vscode';

export type ReasoningTier = 'HIGH' | 'MEDIUM' | 'LOW';
export type BudgetPressure = 'NORMAL' | 'WARNING' | 'HIGH' | 'OVER_BUDGET';

export interface SprintReasoningEntry {
  task: string;
  tier: ReasoningTier;
  escalationPath: string;
  downgradePossible: boolean;
  compactionRecommended: boolean;
}

export interface ReasoningRoutingState {
  activeTier: ReasoningTier;
  budgetPressure: BudgetPressure;
  escalationWarning: boolean;
  downgradeRecommendation: boolean;
  compactionRecommendation: boolean;
  humanVisibleRouting: true;
  deterministicPolicy: true;
  providerNeutralContracts: true;
  rollbackSafeRouting: true;
  sprintReasoningMap: SprintReasoningEntry[];
  estimatedAvoidedPremiumBurn: number;
  estimatedAvoidedUnneededEscalation: number;
}

const burnByTier: Record<ReasoningTier, number> = {HIGH: 8, MEDIUM: 3, LOW: 1};

const defaultSprintMap: SprintReasoningEntry[] = [
  {
    task: 'architecture',
    tier: 'HIGH',
    escalationPath: 'human-visible policy escalation',
    downgradePossible: false,
    compactionRecommended: true,
  },
  {
    task: 'runtime tests',
    tier: 'LOW',
    escalationPath: 'none',
    downgradePossible: false,
    compactionRecommended: false,
  },
  {
    task: 'docs',
    tier: 'LOW',
    escalationPath: 'none',
    downgradePossible: false,
    compactionRecommended: false,
  },
  {
    task: 'adapter wiring',
    tier: 'MEDIUM',
    escalationPath: 'none',
    downgradePossible: true,
    compactionRecommended: false,
  },
];

export class ReasoningRoutingMonitor {
  private compacted = false;

  evaluate(): ReasoningRoutingState {
    const sprintReasoningMap = this.compacted
      ? defaultSprintMap.filter((entry) => entry.tier !== 'LOW')
      : defaultSprintMap;
    const dailyBurn = sprintReasoningMap.reduce((total, entry) => total + burnByTier[entry.tier], 0);
    const allPremiumBurn = sprintReasoningMap.length * burnByTier.HIGH;
    const budgetPressure = dailyBurn >= 20 ? 'OVER_BUDGET' : dailyBurn >= 17 ? 'HIGH' : dailyBurn >= 13 ? 'WARNING' : 'NORMAL';
    return {
      activeTier: sprintReasoningMap.some((entry) => entry.tier === 'HIGH') ? 'HIGH' : 'MEDIUM',
      budgetPressure,
      escalationWarning: sprintReasoningMap.some((entry) => entry.tier === 'HIGH'),
      downgradeRecommendation: budgetPressure === 'WARNING' || budgetPressure === 'HIGH' || budgetPressure === 'OVER_BUDGET',
      compactionRecommendation: sprintReasoningMap.some((entry) => entry.compactionRecommended),
      humanVisibleRouting: true,
      deterministicPolicy: true,
      providerNeutralContracts: true,
      rollbackSafeRouting: true,
      sprintReasoningMap,
      estimatedAvoidedPremiumBurn: Math.max(0, allPremiumBurn - dailyBurn),
      estimatedAvoidedUnneededEscalation: sprintReasoningMap.filter((entry) => entry.tier !== 'HIGH').length,
    };
  }

  compactScope(): ReasoningRoutingState {
    this.compacted = true;
    return this.evaluate();
  }
}

export class ReasoningTierStatusBar {
  private readonly item = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 84);

  constructor(private readonly monitor: ReasoningRoutingMonitor) {
    this.item.command = 'aiDevOs.showReasoningTier';
  }

  refresh(): ReasoningRoutingState {
    const state = this.monitor.evaluate();
    const pressureSuffix = state.budgetPressure === 'NORMAL' ? '' : ' BUDGET_PRESSURE';
    this.item.text = `AI_DEV_OS ${state.activeTier}_REASONING${pressureSuffix}`;
    this.item.tooltip = `Routing ${state.activeTier}; budget ${state.budgetPressure}; avoided premium burn ${state.estimatedAvoidedPremiumBurn}`;
    this.item.show();
    return state;
  }

  dispose(): void {
    this.item.dispose();
  }
}