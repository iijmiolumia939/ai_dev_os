from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GitCollectorFrame:
    repo_path: str
    current_branch: str
    local_head: str
    remote_head: str
    ahead: int
    behind: int
    modified_file_count: int
    staged_file_count: int
    untracked_file_count: int
    changed_runtime_paths: tuple[str, ...]
    changed_test_paths: tuple[str, ...]
    changed_governance_paths: tuple[str, ...]
    read_only: bool


class GitCollector:
    def collect(self, repo_path: str | Path = ".") -> GitCollectorFrame:
        root = Path(repo_path).resolve()
        status_lines = self._git(root, "status", "--porcelain=v1", "--branch").splitlines()
        branch, ahead, behind = self._parse_branch(status_lines[0] if status_lines else "")
        entries = status_lines[1:]
        paths = tuple(self._path_from_status(line) for line in entries if line.strip())
        return GitCollectorFrame(
            repo_path=str(root),
            current_branch=branch,
            local_head=self._git(root, "rev-parse", "HEAD"),
            remote_head=self._remote_head(root, branch),
            ahead=ahead,
            behind=behind,
            modified_file_count=sum(
                1 for line in entries if line[:2].strip() and not line.startswith("??")
            ),
            staged_file_count=sum(1 for line in entries if line[0] not in {" ", "?"}),
            untracked_file_count=sum(1 for line in entries if line.startswith("??")),
            changed_runtime_paths=tuple(path for path in paths if self._is_runtime(path)),
            changed_test_paths=tuple(path for path in paths if path.startswith("tests/")),
            changed_governance_paths=tuple(path for path in paths if self._is_governance(path)),
            read_only=True,
        )

    def _git(self, root: Path, *args: str) -> str:
        completed = subprocess.run(
            ("git", *args),
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
        )
        return completed.stdout.strip()

    def _remote_head(self, root: Path, branch: str) -> str:
        upstream = self._git(root, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
        target = upstream or f"origin/{branch}"
        return self._git(root, "rev-parse", target)

    def _parse_branch(self, line: str) -> tuple[str, int, int]:
        branch = line.replace("##", "").strip().split("...")[0].split()[0] if line else ""
        ahead = self._parse_count(line, "ahead")
        behind = self._parse_count(line, "behind")
        return branch, ahead, behind

    def _parse_count(self, line: str, marker: str) -> int:
        if marker not in line:
            return 0
        tail = line.split(marker, 1)[1].strip(" ]")
        number = tail.split(",", 1)[0].strip()
        return int(number) if number.isdigit() else 0

    def _path_from_status(self, line: str) -> str:
        path = line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        return path.replace("\\", "/")

    def _is_runtime(self, path: str) -> bool:
        return path.startswith("ai_dev_os/") and not path.startswith("ai_dev_os.egg-info/")

    def _is_governance(self, path: str) -> bool:
        return path.startswith(("governance/", "tests/gates/", ".github/", "docs/"))
