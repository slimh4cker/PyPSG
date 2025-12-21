from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from core.models import Node


@dataclass(slots=True)
class PlanAction:
    """
    Represents a filesystem action to be executed.

    Attributes:
        path: Absolute path of the target.
        is_dir: True if directory, False if file.
    """
    path: Path
    is_dir: bool


class Planner:
    """
    Builds an execution plan from a node tree.
    """

    def build(self, root: Node, base_path: Path) -> list[PlanAction]:
        """
        Build a list of filesystem actions.

        Args:
            root: Root node of the parsed structure.
            base_path: Destination directory.

        Returns:
            List of PlanAction objects.
        """
        actions: list[PlanAction] = []

        def walk(node: Node, current: Path) -> None:
            path = current / node.name
            actions.append(PlanAction(path=path, is_dir=node.is_dir()))

            for child in node.children:
                walk(child, path)

        walk(root, base_path)
        return actions
