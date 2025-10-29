# stats_window.py
import tkinter as tk

class StatsWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="#1e1e1e")
        self.pack(expand=True, fill="both")

        # Example stats content
        title = tk.Label(self, text="📊 Typing Statistics", font=("Arial", 14, "bold"), bg="#1e1e1e", fg="white")
        title.pack(pady=10)

        # You can later replace this area with actual graphs or stats
        tk.Label(self, text="This will display advanced typing stats soon!", 
                 bg="#1e1e1e", fg="#cccccc", font=("Arial", 10)).pack(pady=20)
