import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline
import numpy as np
import time

class WPMChart(tk.Frame):
    def __init__(self, master, typing_window, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#2e2e2e")  # Tkinter frame background
        self.typing_window = typing_window

        self.x_history = []
        self.wpm_history = []
        self.start_time = time.time()

        # ---------------- Matplotlib Figure ----------------
        self.fig, self.ax = plt.subplots(figsize=(8, 2))
        self.fig.patch.set_facecolor("#2e2e2e")  # figure background
        self.ax.set_facecolor("#2e2e2e")         # plot background

        # Hide everything: spines, ticks, labels
        self.ax.axis('off')

        # Canvas for Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Start live updates
        self.update_chart()

    def setup_chart(self):
        """Call this once when initializing the chart."""
        self.ax.set_facecolor("#2e2e2e")
        self.fig.patch.set_facecolor("#2e2e2e")

        # Persistent right axis
        self.ax_right = self.ax.twinx()
        self.ax_right.spines['right'].set_color('white')
        self.ax_right.spines['right'].set_linewidth(1)
        self.ax_right.spines['top'].set_visible(False)
        self.ax_right.spines['left'].set_visible(False)
        self.ax_right.tick_params(axis='y', colors='white', labelsize=10)
        self.ax_right.set_ylabel("")

        # Initial figure size (only once)
        self.fig.set_size_inches(10, 5)  # adjust to taste

        # Layout
        self.fig.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.05)

    def update_chart(self):
        typing_window = self.typing_window

        # --- Only start after first character typed ---
        if typing_window.index < 1:
            self.after(500, self.update_chart)
            return

        # --- WPM calculation ---
        elapsed_time = typing_window.get_time_live()
        num_chars = typing_window.index
        wpm = 0 if num_chars < 5 else (num_chars / 5) / (elapsed_time / 60)

        # --- Add new data ---
        self.wpm_history.append(max(0, wpm))
        self.x_history.append(elapsed_time)

        # --- Clear and redraw chart ---
        self.ax.cla()
        self.ax.set_facecolor("#2e2e2e")
        self.fig.patch.set_facecolor("#2e2e2e")

        # --- Smooth WPM line using cubic spline ---
        if len(self.x_history) > 3:
            x = np.array(self.x_history)
            y = np.array(self.wpm_history)

            x_smooth = np.linspace(x.min(), x.max(), 300)
            spline = make_interp_spline(x, y, k=3)
            y_smooth = spline(x_smooth)

            self.ax.plot(x_smooth, y_smooth, color="lime", linewidth=2, label="WPM")
            self.ax.fill_between(x_smooth, y_smooth, 0, color="lime", alpha=0.1)
            self.ax.scatter(x, y, color="white", s=10, zorder=5, alpha=0.8, edgecolors="none")
        else:
            self.ax.plot(self.x_history, self.wpm_history, color="lime", linewidth=2)
            self.ax.fill_between(self.x_history, self.wpm_history, 0, color="lime", alpha=0.1)
            self.ax.scatter(self.x_history, self.wpm_history, color="white", s=10, zorder=5, alpha=0.8, edgecolors="none")

        # --- Axis limits ---
        self.ax.set_xlim(left=0, right=self.x_history[-1])
        self.ax.set_ylim(bottom=0)

        # --- X-axis style ---
        self.ax.spines['bottom'].set_visible(True)
        self.ax.spines['bottom'].set_color('#555555')
        self.ax.spines['bottom'].set_linewidth(1)
        self.ax.get_xaxis().set_ticks([])
        self.ax.get_xaxis().set_ticklabels([])

        # --- Left Y-axis ---
        self.ax.spines['left'].set_color('white')
        self.ax.spines['left'].set_linewidth(1)
        self.ax.spines['top'].set_visible(False)
        self.ax.tick_params(axis='y', colors='white', labelsize=10)
        self.ax.set_ylabel("WPM", color="white", fontsize=10)

        # --- Layout ---
        self.fig.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.05)

        self.canvas.draw_idle()
        self.after(500, self.update_chart)
