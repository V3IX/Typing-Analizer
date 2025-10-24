import tkinter as tk
from typing_window import TypingWindow
from settings_window import SettingsWindow
from wpm_chart import WPMChart
from settings_strip import SettingsStrip

root = tk.Tk()
root.title("Typing Trainer")
root.geometry("900x600")
root.configure(bg="#2e2e2e")

# ---------------- Typing Window ----------------
typing_frame = TypingWindow(root)

# ---------------- Settings Strip ----------------
settings_strip = SettingsStrip(root, typing_frame)

# Pack in the correct order so settings strip is above typing window
settings_strip.pack(fill="x", padx=20, pady=(10,5))
typing_frame.pack(fill="x", padx=20, pady=(0,10))

# ---------------- WPM Chart ----------------
wpm_chart = WPMChart(root, typing_frame)
wpm_chart.pack(fill="both", padx=20, pady=(0,20))
typing_frame.wpm_chart = wpm_chart

root.mainloop()