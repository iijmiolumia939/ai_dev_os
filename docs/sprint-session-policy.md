# Sprint Session Policy

A sprint session is a bounded Chat or Agent Mode work session scoped to one sprint objective. The policy prefers fresh sessions when stale context or architecture escalation would make continuation expensive or ambiguous.

## Continue Only When

- the task remains inside the same sprint objective;
- context tokens are bounded;
- stale context ratio is low;
- retrieval pressure is normal;
- architecture redesign is not active;
- cache reuse is likely and useful.

## Roll Over When

- a sprint boundary is crossed;
- estimated context tokens exceed the session threshold;
- stale context ratio is high;
- retrieval pressure is high or critical;
- architecture or governance redesign begins.

## Required Rollover Output

A rollover should produce a compact continuity bundle, not a transcript replay. The next session starts from active requirements, affected runtimes, current risks, and governance state only.
