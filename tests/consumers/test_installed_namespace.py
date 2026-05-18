from __future__ import annotations

import ai_dev_os
import ai_dev_os.bootstrap
import ai_dev_os.governance
import ai_dev_os.integrations
import ai_dev_os.retrieval
import ai_dev_os.telemetry


def test_ai_dev_os_namespace_imports() -> None:
    assert ai_dev_os.__version__ == "0.1.0a2"
    assert ai_dev_os.bootstrap.main is not None
    assert ai_dev_os.governance.BudgetState is not None
    assert ai_dev_os.retrieval.select_context is not None
    assert ai_dev_os.telemetry.UsageRecord is not None
    assert ai_dev_os.integrations.__doc__ is not None
