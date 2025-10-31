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


# ---------------- Analysis ----------------
def analyze_slowest_letters(limit=2):
    """
    Returns a dict of letter -> average time (ms) based on the last `limit` tests.
    """
    tests = database.get_all_test_results()[:limit]
    letter_times = {}
    letter_counts = {}

    for test in tests:
        test_data = database.get_test_by_id(test[0])
        if not test_data:
            continue
        user_input = test_data["user_input"]
        key_times = [t*1000 for t in test_data["key_times"]]  # convert to ms
        for i, char in enumerate(user_input):
            t = key_times[i]
            letter_times[char] = letter_times.get(char, 0) + t
            letter_counts[char] = letter_counts.get(char, 0) + 1

    avg_times = {char: letter_times[char]/letter_counts[char] for char in letter_times}
    return avg_times


def analyze_slowest_combos(limit=2):
    """
    Returns a dict of 2-letter combo -> average time (ms) based on the last `limit` tests.
    """
    tests = database.get_all_test_results()[:limit]
    combo_times = {}
    combo_counts = {}

    for test in tests:
        test_data = database.get_test_by_id(test[0])
        if not test_data:
            continue
        user_input = test_data["user_input"]
        key_times = [t*1000 for t in test_data["key_times"]]
        for i in range(len(user_input)-1):
            combo = user_input[i] + user_input[i+1]
            t = key_times[i] + key_times[i+1]
            combo_times[combo] = combo_times.get(combo, 0) + t
            combo_counts[combo] = combo_counts.get(combo, 0) + 1

    avg_times = {combo: combo_times[combo]/combo_counts[combo] for combo in combo_times}
    return avg_times


# ---------------- Generate custom text ----------------
def generate_custom_text(length=50, mode="slowest_combos", limit=2):
    """
    Generate custom text using slowest letters or combos from recent tests.
    """
    if mode == "slowest_letters":
        avg_times = analyze_slowest_letters(limit=limit)
        slow_letters = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)
        letters = [l for l,_ in slow_letters]
        if not letters:
            return ""
        return "".join(random.choices(letters, k=length))

    elif mode == "slowest_combos":
        avg_times = analyze_slowest_combos(limit=limit)
        slow_combos = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)
        combos = [c for c,_ in slow_combos]
        if not combos:
            return ""
        text = ""
        while len(text) < length:
            text += random.choice(combos)
        return text[:length]

    else:
        raise ValueError("Unknown mode: use 'slowest_letters' or 'slowest_combos'")