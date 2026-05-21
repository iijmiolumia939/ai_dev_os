import * as vscode from 'vscode';
import {RateLimitedNotifications} from '../notifications/rateLimitedNotifications';
import {
  DevPolicyMonitor,
  EscalationPressureStatusBar,
  GovernancePressureStatusBar,
  PolicyStableStatusBar,
  RealismProtectedStatusBar,
} from '../devPolicy/devPolicy';

export function registerDevPolicyCommands(
  monitor: DevPolicyMonitor,
  policyStatus: PolicyStableStatusBar,
  governanceStatus: GovernancePressureStatusBar,
  escalationStatus: EscalationPressureStatusBar,
  realismStatus: RealismProtectedStatusBar,
  notifications: RateLimitedNotifications,
): vscode.Disposable[] {
  const refreshAll = () => {
    policyStatus.refresh();
    governanceStatus.refresh();
    escalationStatus.refresh();
    realismStatus.refresh();
  };

  const showDevelopmentPolicies = vscode.commands.registerCommand(
    'aiDevOs.showDevelopmentPolicies',
    async () => {
      const state = policyStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS policies: ${state.compactSummary}; human-confirmed ${state.humanConfirmedGovernanceOnly}.`,
      );
    },
  );

  const showArchitectureProtection = vscode.commands.registerCommand(
    'aiDevOs.showArchitectureProtection',
    async () => {
      const state = governanceStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS architecture policy: ${state.architectureHints.join('; ')}.`,
      );
    },
  );

  const showEmbodimentRealismPolicy = vscode.commands.registerCommand(
    'aiDevOs.showEmbodimentRealismPolicy',
    async () => {
      const state = realismStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS realism policy: ${state.embodimentHints.join('; ')}.`,
      );
    },
  );

  const showProviderEscalationPolicy = vscode.commands.registerCommand(
    'aiDevOs.showProviderEscalationPolicy',
    async () => {
      const state = escalationStatus.refresh();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS escalation policy: ${state.providerHints.join('; ')}.`,
      );
    },
  );

  const showAntiExplosionPolicy = vscode.commands.registerCommand(
    'aiDevOs.showAntiExplosionPolicy',
    async () => {
      const state = monitor.evaluate();
      await vscode.window.showInformationMessage(
        `AI_DEV_OS anti-explosion policy: ${state.antiExplosionHints.join('; ')}.`,
      );
    },
  );

  const compactPolicySummary = vscode.commands.registerCommand(
    'aiDevOs.compactPolicySummary',
    async () => {
      const state = monitor.compactSummary();
      refreshAll();
      await notifications.info(
        'development-policy-compacted',
        `AI_DEV_OS policy summary compacted; governance pressure ${state.governancePressure}.`,
      );
    },
  );

  return [
    showDevelopmentPolicies,
    showArchitectureProtection,
    showEmbodimentRealismPolicy,
    showProviderEscalationPolicy,
    showAntiExplosionPolicy,
    compactPolicySummary,
  ];
}