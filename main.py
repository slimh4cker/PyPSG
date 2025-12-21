import sys

from interfaces.cli import run as run_cli
from interfaces.gui import StructureGeneratorGUI

import tkinter as tk


def main() -> int:
    """
    Entry point for structure_generator.

    If arguments are provided → CLI
    Otherwise → GUI
    """
    if len(sys.argv) > 1:
        return run_cli()

    root = tk.Tk()
    StructureGeneratorGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
