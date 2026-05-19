from __future__ import annotations

from dataclasses import dataclass, field

ALLOWED_MEMORY_KINDS = {
    "sprint_summary",
    "adr_summary",
    "checkpoint_summary",
    "architecture_summary",
    "stale_branch_summary",
}


@dataclass(frozen=True)
class MemoryTreeNode:
    kind: str
    title: str
    summary: str
    priority: int = 0
    continuity_weight: float = 0.0
    children: tuple[MemoryTreeNode, ...] = field(default_factory=tuple)
    stale: bool = False


def _validate_node(node: MemoryTreeNode, depth: int, max_depth: int) -> None:
    if node.kind not in ALLOWED_MEMORY_KINDS:
        raise ValueError(f"unsupported memory kind: {node.kind}")
    if not node.summary:
        raise ValueError("raw memory replay is forbidden; summary is required")
    if depth > max_depth:
        raise ValueError("memory tree depth exceeds bounded limit")
    for child in node.children:
        _validate_node(child, depth + 1, max_depth)


def build_memory_tree(
    nodes: tuple[MemoryTreeNode, ...], *, max_depth: int = 3
) -> tuple[MemoryTreeNode, ...]:
    if max_depth < 1:
        raise ValueError("memory tree max depth must be at least 1")
    for node in nodes:
        _validate_node(node, 1, max_depth)
    return tuple(
        sorted(nodes, key=lambda node: (-node.continuity_weight, -node.priority, node.title))
    )


def retrieve_memory_path(
    nodes: tuple[MemoryTreeNode, ...], *, limit: int = 6, include_stale: bool = False
) -> tuple[MemoryTreeNode, ...]:
    if limit <= 0:
        return ()
    flattened: list[MemoryTreeNode] = []

    def visit(node: MemoryTreeNode) -> None:
        if include_stale or not node.stale:
            flattened.append(node)
        for child in node.children:
            visit(child)

    for root in nodes:
        visit(root)
    ranked = sorted(
        flattened, key=lambda node: (-node.continuity_weight, -node.priority, node.title)
    )
    return tuple(ranked[:limit])
