import tkinter as tk
from tkinter import ttk
from datetime import datetime
from database import get_all_test_results
from collections import defaultdict
from database import generate_full_digraph_table_recent
from stats_window import StatsWindow

class UserWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("User Account")
        self.geometry("600x450")
        self.configure(bg="#1e1e1e")

        # Pagination variables
        self.current_page = 0
        self.page_size = 20
        self.all_rows = []

        # Notebook
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TNotebook.Tab", font=("Arial", 11, "bold"), padding=[12, 8])
        style.configure("Treeview", background="#2c2c2c", foreground="white",
                        fieldbackground="#2c2c2c", rowheight=28)
        style.map("Treeview", background=[("selected", "#3a6ea5")])
        style.configure("Treeview.Heading", background="#2c2c2c", foreground="white", font=("Arial", 10, "bold"))

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both", padx=12, pady=12)

        # Profile Tab
        self.profile_frame = tk.Frame(notebook, bg="#1e1e1e")
        notebook.add(self.profile_frame, text="👤 Profile")

        # History Tab
        self.history_frame = tk.Frame(notebook, bg="#1e1e1e")
        notebook.add(self.history_frame, text="📜 History")

        # Treeview for history
        columns = ("Date", "WPM", "Accuracy", "Words")
        self.tree = ttk.Treeview(self.history_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.pack(expand=True, fill="both", padx=10, pady=(10, 0))

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Table Tab
        self.analysis_frame = tk.Frame(notebook, bg="#1e1e1e")
        notebook.add(self.analysis_frame, text="⏱ Analysis")

        # Treeview for analysis
        columns = ("Letter/Combo", "Avg Time (ms)")
        self.analysis_tree = ttk.Treeview(self.analysis_frame, columns=columns, show="headings")
        self.analysis_tree.pack(expand=True, fill="both", padx=10, pady=10)

        for col in columns:
            self.analysis_tree.heading(col, text=col)
            self.analysis_tree.column(col, anchor="center", width=120)

        # Load analysis data
        self.load_analysis_table()

        self.stats_frame = tk.Frame(notebook, bg="#1e1e1e")
        notebook.add(self.stats_frame, text="📊 Stats")
        StatsWindow(self.stats_frame)

        # Load analysis data
        self.load_analysis_table()

        # Pagination controls (below Treeview)
        nav_frame = tk.Frame(self.history_frame, bg="#1e1e1e")
        nav_frame.pack(fill="x", pady=(6, 2))

        self.prev_btn = tk.Button(nav_frame, text="⬅ Previous", command=self.prev_page)
        self.prev_btn.pack(side="left", padx=10)

        self.page_label = tk.Label(nav_frame, text="", bg="#1e1e1e", fg="white", font=("Arial", 10))
        self.page_label.pack(side="left", expand=True)

        self.next_btn = tk.Button(nav_frame, text="Next ➡", command=self.next_page)
        self.next_btn.pack(side="right", padx=10)

        # Replay button (below everything)
        self.replay_btn = tk.Button(
            self.history_frame,
            text="🎬 Replay Selected Test",
            font=("Arial", 10, "bold"),
            bg="#3a6ea5",
            fg="white",
            activebackground="#4b7ecb",
            command=self.replay_selected
        )
        self.replay_btn.pack(pady=10)

        # Load data
        self.load_profile()
        self.load_history_data()
        self.show_page(0)

    def load_profile(self):
        for widget in self.profile_frame.winfo_children():
            widget.destroy()

        rows = get_all_test_results()
        total_tests = len(rows)
        best_wpm = max((r[2] for r in rows), default=0)  # WPM is index 2 now
        avg_acc = sum((r[3] for r in rows), 0) / total_tests * 100 if total_tests > 0 else 0

        stats = [
            ("Total Tests", total_tests),
            ("Best WPM", round(best_wpm, 1)),
            ("Average Accuracy", f"{avg_acc:.1f}%")
        ]

        for stat, value in stats:
            card = tk.Frame(self.profile_frame, bg="#2c2c2c", padx=15, pady=10)
            card.pack(fill="x", padx=20, pady=10)
            tk.Label(card, text=stat, bg="#2c2c2c", fg="#cccccc", font=("Arial", 10, "bold")).pack(anchor="w")
            tk.Label(card, text=value, bg="#2c2c2c", fg="white", font=("Arial", 14, "bold")).pack(anchor="w", pady=(5, 0))

    def load_history_data(self):
        """Load all data once from the database."""
        self.all_rows = get_all_test_results()

    def show_page(self, page_num):
        """Display a specific page of history."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_pages = max(1, (len(self.all_rows) - 1) // self.page_size + 1)
        page_num = max(0, min(page_num, total_pages - 1))
        self.current_page = page_num

        start = page_num * self.page_size
        end = start + self.page_size
        rows = self.all_rows[start:end]

        for test_id, ts, wpm, acc, words in rows:
            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
            acc_percent = acc * 100
            self.tree.insert("", "end", iid=str(test_id),
                            values=(date_str, round(wpm, 1), f"{acc_percent:.1f}%", words))

        # Update page label
        self.page_label.config(text=f"Page {page_num + 1} / {total_pages}")

        # Enable/disable buttons
        self.prev_btn.config(state="normal" if page_num > 0 else "disabled")
        self.next_btn.config(state="normal" if page_num < total_pages - 1 else "disabled")

    def next_page(self):
        self.show_page(self.current_page + 1)

    def prev_page(self):
        self.show_page(self.current_page - 1)

    def replay_selected(self):
        selected = self.tree.selection()
        if not selected:
            return

        test_id = int(selected[0])
        import database
        data = database.get_test_by_id(test_id)

        if not data:
            print("Test data not found for ID:", test_id)
            return

        self.destroy()  # close the user window

        # Call replay on master (should now be TypingWindow)
        if hasattr(self.master, "replay"):
            self.master.replay(data)
        else:
            print("⚠️ Master window has no replay() method.")

    def load_analysis_table(self):
        return