import * as vscode from 'vscode';
import {
  EscalationGuardedStatusBar,
  GovernanceStablePolicyStatusBar,
  LocalFirstPolicyStatusBar,
  PolicyBoundedStatusBar,
  RuntimePolicyMonitor,
} from '../runtimePolicy/runtimePolicy';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';

export function registerRuntimePolicyCommands(
  monitor: RuntimePolicyMonitor,
  policyBoundedStatus: PolicyBoundedStatusBar,
  governanceStableStatus: GovernanceStablePolicyStatusBar,
  localFirstPolicyStatus: LocalFirstPolicyStatusBar,
  escalationGuardedStatus: EscalationGuardedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    policyBoundedStatus.refresh();
    governanceStableStatus.refresh();
    localFirstPolicyStatus.refresh();
    escalationGuardedStatus.refresh();
  };

  const showRuntimePolicy = vscode.commands.registerCommand(
    'aiDevOs.showRuntimePolicy',
    async () => {
      const state = policyBoundedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS runtime policy: execution ${state.executionPolicyScore}; reflective ${state.reflectivePolicyScore}.`,
      );
    },
  );

  const showRetryPolicy = vscode.commands.registerCommand(
    'aiDevOs.showRetryPolicy',
    async () => {
      const state = escalationGuardedStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS retry policy: ${state.retryPolicyScore}.`,
      );
    },
  );

  const showProviderPolicy = vscode.commands.registerCommand(
    'aiDevOs.showProviderPolicy',
    async () => {
      const state = localFirstPolicyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS provider policy: ${state.providerPolicyScore}.`,
      );
    },
  );

  const showContinuationPolicy = vscode.commands.registerCommand(
    'aiDevOs.showContinuationPolicy',
    async () => {
      const state = governanceStableStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS continuation policy: ${state.continuationPolicyScore}.`,
      );
    },
  );

  const compactRuntimePolicySummary = vscode.commands.registerCommand(
    'aiDevOs.compactRuntimePolicySummary',
    async () => {
      const state = monitor.evaluate();
      refreshAll();
      await notifications.info(
        'runtime-policy-compact-summary',
        `AI_DEV_OS compact runtime policy: ${state.compactSummary}.`,
      );
    },
  );

  return [
    showRuntimePolicy,
    showRetryPolicy,
    showProviderPolicy,
    showContinuationPolicy,
    compactRuntimePolicySummary,
  ];
}
