from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TraceNode:
    name: str
    tokens: int = 0
    cost: float = 0.0
    latency_ms: int = 0
    retries: int = 0
    council_fanout: int = 0
    context_size: int = 0
    expensive_model_usage: int = 0
    autonomous_depth: int = 0
    children: tuple[TraceNode, ...] = ()


@dataclass(frozen=True)
class LangfuseTrace:
    sprint: str
    council: TraceNode = field(default_factory=lambda: TraceNode("council"))

    def with_council_children(self, *children: TraceNode) -> LangfuseTrace:
        return LangfuseTrace(sprint=self.sprint, council=TraceNode("council", children=children))


def flatten_trace(node: TraceNode) -> list[TraceNode]:
    nodes = [node]
    for child in node.children:
        nodes.extend(flatten_trace(child))
    return nodes


def aggregate_daily_cost(traces: list[LangfuseTrace]) -> dict[str, int | float]:
    nodes = [node for trace in traces for node in flatten_trace(trace.council)]
    return {
        "tokens": sum(node.tokens for node in nodes),
        "cost": sum(node.cost for node in nodes),
        "retries": sum(node.retries for node in nodes),
        "council_fanout": sum(node.council_fanout for node in nodes),
        "max_context_size": max((node.context_size for node in nodes), default=0),
        "expensive_model_usage": sum(node.expensive_model_usage for node in nodes),
        "max_autonomous_depth": max((node.autonomous_depth for node in nodes), default=0),
        "latency_ms": sum(node.latency_ms for node in nodes),
    }
