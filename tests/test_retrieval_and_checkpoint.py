from __future__ import annotations

from checkpoints import Checkpoint, write_checkpoint
from retrieval import build_manifest, prune, select_context


def test_retrieval_and_checkpoint_workflow(tmp_path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "architecture.md").write_text("retrieval governance", encoding="utf-8")
    manifest = build_manifest(tmp_path, ("docs",))
    bundle = select_context(manifest, "governance")

    checkpoint_path = write_checkpoint(
        Checkpoint(active_requirements=("NFR-COST-01",)), tmp_path / "checkpoints" / "latest.json"
    )

    assert bundle["entries"]
    assert prune(bundle)["policy"]
    assert checkpoint_path.exists()
