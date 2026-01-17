from __future__ import annotations

# Tree drawing characters (Unicode + ASCII)
TREE_PREFIXES: tuple[str, ...] = (
    "├──", "└──", "│", "─",
    "+--", "|__", "\\__"
)

FILE_EXTENSIONS: tuple[str, ...] = (
    ".py", ".txt", ".md", ".toml", ".json",
    ".yaml", ".yml", ".env", ".gitignore"
)


def clean_line(line: str) -> str:
    """
    Extract the logical node name from a tree-formatted line.

    - Removes tree drawing symbols
    - Removes inline comments
    - Preserves indentation logic (handled elsewhere)
    """
    stripped = line.strip()

    for prefix in TREE_PREFIXES:
        stripped = stripped.replace(prefix, "")

    if "#" in stripped:
        stripped = stripped.split("#", 1)[0]

    return stripped.strip()


def is_file(name: str) -> bool:
    """
    Determine whether a node name represents a file.
    """
    name = name.lower()
    return (
        name.startswith(".")
        or name.endswith(FILE_EXTENSIONS)
    )


def indent_level(raw_line: str) -> int:
    import re
    """
    Heuristically compute indentation level.
    Works for irregular spacing and mixed symbols.
    """
    stripped = raw_line.lstrip()
    if not stripped:
        return 0

    match = re.search(r"[├└\+\-]", raw_line)
    if match:
        idx = match.start()
    else:
        idx = 0

    prefix = raw_line[:idx]
    level = 0
    i = 0
    while i < len(prefix):
        if prefix[i] in ("│", "|"):
            level += 1
            i += 1
        elif prefix[i] == " ":
            if i + 1 < len(prefix) and prefix[i+1] == " ":
                level += 1
                i += 2
            else:
                i += 1
        else:
            i += 1
    return level


