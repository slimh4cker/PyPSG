from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(slots=True)
class Node:
    """
    Base class for all nodes in the structure tree.

    Attributes:
        name: Name of the file or directory.
        children: Child nodes (only meaningful for directories).
    """
    name: str
    children: List["Node"] = field(default_factory=list)

    def is_dir(self) -> bool:
        """Return True if the node represents a directory."""
        raise NotImplementedError


@dataclass(slots=True)
class DirNode(Node):
    """Represents a directory in the structure tree."""

    def is_dir(self) -> bool:
        return True


@dataclass(slots=True)
class FileNode(Node):
    """Represents a file in the structure tree."""

    def is_dir(self) -> bool:
        return False
