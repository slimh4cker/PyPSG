import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path

from core.parser import TreeParser
from core.planner import Planner
from core.executor import Executor


BG = "#F5F5F7"
PRIMARY = "#2563EB"
PRIMARY_HOVER = "#1E40AF"
TEXT = "#1F2937"
SUBTEXT = "#6B7280"
BORDER = "#E5E7EB"


class StructureGeneratorGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Structure Generator")
        self.root.geometry("980x700")
        self.root.configure(bg=BG)

        self.destination = Path.cwd()

        self._build_ui()

    # ------------------------------------------------------------------ UI

    def _build_ui(self) -> None:
        self._header()
        self._content()
        self._footer()

    def _header(self) -> None:
        header = tk.Frame(self.root, bg=BG, padx=20, pady=14)
        header.pack(fill=tk.X)

        tk.Label(
            header,
            text="Structure Generator",
            font=("Segoe UI", 16, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Generate project folder structures from tree format",
            font=("Segoe UI", 10),
            fg=SUBTEXT,
            bg=BG
        ).pack(anchor="w")

    def _content(self) -> None:
        content = tk.Frame(self.root, bg=BG, padx=20, pady=10)
        content.pack(fill=tk.BOTH, expand=True)

        tk.Label(
            content,
            text="Tree structure",
            font=("Segoe UI", 11, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w", pady=(0, 4))

        hint = (
            "Each level must use 4-character indentation (spaces or │).\n"
            "Example:\n\n"
            "project/\n"
            "├── src/\n"
            "│   └── main.py\n"
            "└── README.md"
        )

        hint_box = tk.Text(
            content,
            height=8,
            font=("Consolas", 9),
            fg=SUBTEXT,
            bg="#FAFAFA",
            relief=tk.FLAT,
            wrap=tk.WORD,
            padx=10,
            pady=8
        )
        hint_box.pack(fill=tk.X, pady=(0, 8))

        hint_box.insert("1.0", hint)
        hint_box.config(state=tk.DISABLED)

        self.text_area = scrolledtext.ScrolledText(
            content,
            font=("Consolas", 10),
            wrap=tk.NONE,
            height=22,
            relief=tk.FLAT,
            borderwidth=1
        )
        self.text_area.pack(fill=tk.BOTH, expand=True)

    def _footer(self) -> None:
        footer = tk.Frame(self.root, bg=BG, padx=20, pady=14)
        footer.pack(fill=tk.X)

        # Destination
        dest_frame = tk.Frame(footer, bg=BG)
        dest_frame.pack(side=tk.LEFT)

        tk.Label(
            dest_frame,
            text="Destination:",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT,
            bg=BG
        ).pack(anchor="w")

        self.dest_label = tk.Label(
            dest_frame,
            text=str(self.destination),
            font=("Segoe UI", 9),
            fg=SUBTEXT,
            bg=BG
        )
        self.dest_label.pack(anchor="w")

        # Buttons
        btns = tk.Frame(footer, bg=BG)
        btns.pack(side=tk.RIGHT)

        self._btn(btns, "Select folder", self.select_destination).pack(side=tk.LEFT, padx=6)
        self._btn(btns, "Preview", lambda: self.run(True)).pack(side=tk.LEFT, padx=6)
        self._btn(btns, "Generate", lambda: self.run(False), primary=True).pack(side=tk.LEFT, padx=6)
        self._btn(btns, "Clear", self.clear).pack(side=tk.LEFT, padx=(0, 12))


    # ------------------------------------------------------------------ Logic

    def select_destination(self) -> None:
        path = filedialog.askdirectory()
        if path:
            self.destination = Path(path)
            self.dest_label.config(text=str(self.destination))

    def run(self, dry_run: bool) -> None:
        content = self.text_area.get("1.0", tk.END).strip()
        if not content:
            messagebox.showwarning("Warning", "No input provided.")
            return

        try:
            tree = TreeParser().parse(content)
            actions = Planner().build(tree, self.destination)

            executor = Executor(dry_run=dry_run)
            executor.execute(actions)

            if dry_run:
                self._preview(executor.log)
            else:
                messagebox.showinfo(
                    "Success",
                    "Structure created successfully."
                )

        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def clear(self) -> None:
        self.text_area.delete("1.0", tk.END)
        
    def _preview(self, log: list[str]) -> None:
        win = tk.Toplevel(self.root)
        win.title("Preview")
        win.geometry("720x520")

        text = scrolledtext.ScrolledText(
            win,
            font=("Consolas", 10),
            relief=tk.FLAT
        )
        text.pack(fill=tk.BOTH, expand=True)

        for line in log:
            text.insert(tk.END, line + "\n")

        text.config(state=tk.DISABLED)

    # ------------------------------------------------------------------ Helpers

    def _btn(self, parent, text, command, primary=False):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10),
            padx=14,
            pady=6,
            relief=tk.FLAT,
            bg=PRIMARY if primary else "#E5E7EB",
            fg="white" if primary else TEXT,
            activebackground=PRIMARY_HOVER if primary else "#D1D5DB",
            cursor="hand2"
        )
