from core.models import DirNode, FileNode
from utils.tree_format import clean_line, is_file, indent_level


class TreeParser:
    def parse(self, text: str) -> DirNode:
        root: DirNode | None = None
        stack: list[DirNode] = []

        for raw_line in text.splitlines():
            name = clean_line(raw_line)
            if not name:
                continue

            level = indent_level(raw_line)
            node = FileNode(name) if is_file(name) else DirNode(name)

            if root is None:
                if not isinstance(node, DirNode):
                    raise ValueError("Root element must be a directory")
                root = node
                stack = [root]
                continue

            level = max(1, level)

            if level > len(stack):
                level = len(stack)

            stack = stack[:level]
            parent = stack[-1]
            parent.children.append(node)

            if isinstance(node, DirNode):
                stack.append(node)

        if root is None:
            raise ValueError("No valid root directory found")

        return root
