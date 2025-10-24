import tkinter as tk
from typing_window import TypingWindow
from settings_window import SettingsWindow
from wpm_chart import WPMChart
from settings_strip import SettingsStrip
from finish_info import FinishInfo

root = tk.Tk()
root.title("Typing Trainer")
root.geometry("900x600")
root.configure(bg="#2e2e2e")

typing_frame = TypingWindow(root)
settings_strip = SettingsStrip(root, typing_frame)
wpm_chart = WPMChart(root, typing_frame)
finish_info = FinishInfo(root)

settings_strip.pack(fill="x", padx=20, pady=(10,5))
typing_frame.pack(fill="x", padx=20, pady=(0,10))
wpm_chart.pack(fill="both", padx=20, pady=(0,10))
finish_info.pack(fill="x", padx=20, pady=(0,20))
finish_info.hide()

typing_frame.wpm_chart = wpm_chart
typing_frame.finish_info = finish_info

root.mainloop()
