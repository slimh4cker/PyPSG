from pathlib import Path
from typing import Iterable

from core.planner import PlanAction


class Executor:
    """
    Executes filesystem actions produced by the Planner.

    Supports dry-run mode.
    """

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.log: list[str] = []

    def execute(self, actions: Iterable[PlanAction]) -> None:
        """
        Execute a sequence of plan actions.

        Args:
            actions: Iterable of PlanAction objects.
        """
        for action in actions:
            if action.is_dir:
                self._mkdir(action.path)
            else:
                self._touch(action.path)

    def _mkdir(self, path: Path) -> None:
        self.log.append(f"[DIR ] {path}")
        if not self.dry_run:
            path.mkdir(parents=True, exist_ok=True)

    def _touch(self, path: Path) -> None:
        self.log.append(f"[FILE] {path}")
        if not self.dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.touch(exist_ok=True)
