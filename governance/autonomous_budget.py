MAX_AGENT_DEPTH = 3
MAX_REVIEW_LOOPS = 2
MAX_RETRY_LOOPS = 2
MAX_CONTEXT_REFRESH = 1
MAX_COUNCIL_ESCALATION = 1


def within_limits(values: dict[str, int]) -> bool:
    return (
        values.get("agent_depth", 0) <= MAX_AGENT_DEPTH
        and values.get("review_loops", 0) <= MAX_REVIEW_LOOPS
        and values.get("retry_loops", 0) <= MAX_RETRY_LOOPS
        and values.get("context_refresh", 0) <= MAX_CONTEXT_REFRESH
        and values.get("council_escalation", 0) <= MAX_COUNCIL_ESCALATION
    )
