import tkinter as tk
from tkinter import ttk
from datetime import datetime
from database import get_all_test_results

class UserWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("User Account")
        self.geometry("600x450")
        self.configure(bg="#1e1e1e")

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
        self.tree.pack(expand=True, fill="both", padx=10, pady=(10,0))

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=120)

        # Replay button below Treeview
        self.replay_btn = tk.Button(self.history_frame, text="Replay Selected Test", command=self.replay_selected)
        self.replay_btn.pack(pady=8)

        # Load data
        self.load_profile()
        self.load_history()

    def load_profile(self):
        for widget in self.profile_frame.winfo_children():
            widget.destroy()

        rows = get_all_test_results()
        total_tests = len(rows)
        best_wpm = max((r[1] for r in rows), default=0)
        avg_acc = sum((r[2] for r in rows), 0) / total_tests * 100 if total_tests > 0 else 0  # ✅ multiply by 100

        stats = [
            ("Total Tests", total_tests),
            ("Best WPM", best_wpm),
            ("Average Accuracy", f"{avg_acc:.1f}%")
        ]

        for stat, value in stats:
            card = tk.Frame(self.profile_frame, bg="#2c2c2c", padx=15, pady=10)
            card.pack(fill="x", padx=20, pady=10)
            tk.Label(card, text=stat, bg="#2c2c2c", fg="#cccccc", font=("Arial", 10, "bold")).pack(anchor="w")
            tk.Label(card, text=value, bg="#2c2c2c", fg="white", font=("Arial", 14, "bold")).pack(anchor="w", pady=(5,0))

    def load_history(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        rows = get_all_test_results()
        for ts, wpm, acc, words in rows:
            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
            acc_percent = acc * 100  # ✅ convert to percentage
            self.tree.insert("", "end", values=(date_str, round(wpm,1), f"{acc_percent:.1f}%", words))

    def replay_selected(self):
        selected = self.tree.selection()
        if not selected:
            return
        # For now, empty function
        item = self.tree.item(selected[0])
        print("Replay clicked for:", item["values"])
