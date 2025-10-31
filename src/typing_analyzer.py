import database
import json
import random
import tkinter as tk

import tkinter as tk

import string
import tkinter as tk

class DigraphTable(tk.Frame):
    def __init__(self, master, letters=string.ascii_lowercase, cell_width=6, **kwargs):
        super().__init__(master, **kwargs)
        self.visible = False
        self.letters = letters
        self.rows = len(letters) + 1
        self.cols = len(letters) + 1
        self.cells = []
        self.digraph_times = {}  # store all digraph times

        for r in range(self.rows):
            row_cells = []
            for c in range(self.cols):
                lbl = tk.Label(self, text="", font=("Consolas", 10),
                               width=cell_width, height=1,
                               bg="#3e3e3e", fg="white",
                               borderwidth=1, relief="solid")
                lbl.grid(row=r, column=c, sticky="nsew", padx=1, pady=1)
                row_cells.append(lbl)
            self.cells.append(row_cells)

        # Fill header row/column
        for i, l in enumerate(self.letters):
            self.cells[0][i+1].config(text=l)
            self.cells[i+1][0].config(text=l)

        # Make grid expand evenly
        for r in range(self.rows):
            self.grid_rowconfigure(r, weight=1)
        for c in range(self.cols):
            self.grid_columnconfigure(c, weight=1)

        self.hide()

    def update_digraph_time(self, pair, time_ms):
        """
        Update a single digraph without clearing previous data
        """
        self.digraph_times[pair] = time_ms
        l1, l2 = pair
        try:
            r = self.letters.index(l1) + 1
            c = self.letters.index(l2) + 1
            self.cells[r][c].config(text=f"{time_ms:.0f}")
        except ValueError:
            pass  # ignore if letters not in list

    def set_mode(self, visible):
        if visible:
            self.show()
        else:
            self.hide()

    def show(self):
        """Display the chart and start updating."""
        self.pack(fill="x", padx=10, pady=5)

        if not hasattr(self, "_after_id"):
            self.update_chart()

    def hide(self):
        """Hide the chart and stop updating."""
        self.pack_forget()
        if hasattr(self, "_after_id"):
            self.after_cancel(self._after_id)
            del self._after_id
