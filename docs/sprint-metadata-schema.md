# Sprint Metadata Schema

`sprint.yml` is an optional workspace-local file used to reduce manual sprint prompt input.

## Fields

```yaml
sprint_id: 42
active_fr_tc:
  - FR-REPOINTEL-01
  - TC-REPOINTEL-01
affected_runtimes:
  - repository_intelligence
  - session_orchestrator
roadmap_stage: workspace collector
active_risks:
  - manual summary drift
architecture_flags:
  - read-only collector
continuity_state: compact
validation_status: pending
```

The parser intentionally supports a compact deterministic subset of YAML so the runtime does not depend on PyYAML or network services.
