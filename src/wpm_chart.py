import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import make_interp_spline
import numpy as np
import logging
import time

logger = logging.getLogger("typing_app")

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

        # --- Initialize tracking attributes ---
        if not hasattr(self, "last_index"):
            self.last_index = typing_window.index
        if not hasattr(self, "last_wrong"):
            self.last_wrong = typing_window.wrong
        if not hasattr(self, "error_marks"):
            self.error_marks = []
        if not hasattr(self, "correct_chars"):
            self.correct_chars = 0
        if not hasattr(self, "error_recorded_for_index"):
            self.error_recorded_for_index = False

        # --- Calculate changes ---
        typed_new = typing_window.index - self.last_index
        new_errors = typing_window.wrong - self.last_wrong
        elapsed_time = typing_window.get_time_live()

        # --- Only update if a new character is typed ---
        if typed_new != 0:
            # --- Update correct_chars ---
            if typed_new > 0:
                correct_new = max(0, typed_new - max(0, new_errors))
                self.correct_chars += correct_new
            elif typed_new < 0:
                # Backspace
                self.correct_chars = max(0, self.correct_chars + typed_new)

            # --- Detect new errors ---
            if typing_window.wrong > self.last_wrong and not self.error_recorded_for_index:
                self.error_marks.append(elapsed_time)
                self.error_recorded_for_index = True
                logger.debug("New error recorded at %.2f s, index=%d", elapsed_time, typing_window.index)

            if typing_window.wrong == self.last_wrong:
                self.error_recorded_for_index = False

            # --- Update last_wrong and last_index ---
            self.last_wrong = typing_window.wrong
            self.last_index = typing_window.index

            # --- WPM calculation with accuracy ---
            if typing_window.index > 5 and elapsed_time > 0 and not getattr(typing_window, "finished", False):
                wpm_raw = (self.correct_chars / 5) / (elapsed_time / 60)
                accuracy = self.correct_chars / max(1, typing_window.index)
                wpm_effective = wpm_raw * accuracy

                self.wpm_history.append(max(0, wpm_effective))
                self.x_history.append(elapsed_time)
                logger.debug(
                    "WPM updated: %.2f, accuracy: %.2f%%, typed_chars=%d, elapsed=%.2fs",
                    wpm_effective, accuracy * 100, typing_window.index, elapsed_time
                )

            # --- Redraw chart ---
            self.redraw_chart()

        # --- Schedule next check ---
        if self.winfo_exists():
            self._after_id = self.after(50, self.update_chart)

    def redraw_chart(self):
        self.ax.cla()
        self.ax.set_facecolor("#2e2e2e")
        self.fig.patch.set_facecolor("#2e2e2e")

        # --- Smooth WPM line ---
        if len(self.x_history) > 3:
            x = np.array(self.x_history)
            y = np.array(self.wpm_history)
            x_smooth = np.linspace(x.min(), x.max(), 300)
            spline = make_interp_spline(x, y, k=3)
            y_smooth = spline(x_smooth)
            self.ax.plot(x_smooth, y_smooth, color="lime", linewidth=2)
            self.ax.fill_between(x_smooth, y_smooth, 0, color="lime", alpha=0.1)
            self.ax.scatter(x, y, color="white", s=10, zorder=5, alpha=0.8, edgecolors="none")
        else:
            self.ax.plot(self.x_history, self.wpm_history, color="lime", linewidth=2)
            self.ax.fill_between(self.x_history, self.wpm_history, 0, color="lime", alpha=0.1)
            self.ax.scatter(self.x_history, self.wpm_history, color="white", s=10, zorder=5, alpha=0.8, edgecolors="none")

        # --- Draw red error lines ---
        if hasattr(self, "error_marks"):
            for mark in self.error_marks:
                self.ax.axvline(x=mark, color="red", linestyle="--", linewidth=1, alpha=0.7)

        # --- Axis limits ---
        if self.x_history:
            self.ax.set_xlim(left=self.x_history[0], right=self.x_history[-1])
        self.ax.set_ylim(bottom=0)

        # --- Axis styling ---
        self.ax.spines['bottom'].set_visible(True)
        self.ax.spines['bottom'].set_color('#555555')
        self.ax.spines['bottom'].set_linewidth(1)
        self.ax.get_xaxis().set_ticks([])
        self.ax.get_xaxis().set_ticklabels([])

        self.ax.spines['left'].set_color('white')
        self.ax.spines['left'].set_linewidth(1)
        self.ax.spines['top'].set_visible(False)
        self.ax.tick_params(axis='y', colors='white', labelsize=10)
        self.ax.set_ylabel("WPM", color="white", fontsize=10)

        self.fig.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.05)
        self.canvas.draw_idle()

    def reset_chart(self):
        if hasattr(self, "_after_id"):
            self.after_cancel(self._after_id)
            del self._after_id

        # --- Reset performance data ---
        self.x_history.clear()
        self.wpm_history.clear()
        self.start_time = time.time()

        # --- Reset mistake tracking ---
        self.error_marks = []
        self.last_wrong = 0

        # --- Clear plot and redraw an empty chart ---
        self.ax.cla()
        self.ax.set_facecolor("#2e2e2e")
        self.fig.patch.set_facecolor("#2e2e2e")

        self.ax.set_ylabel("WPM", color="white", fontsize=10)
        self.ax.spines['left'].set_color('white')
        self.ax.spines['bottom'].set_color('#555555')
        self.ax.spines['bottom'].set_visible(True)
        self.ax.tick_params(axis='y', colors='white', labelsize=10)
        self.ax.get_xaxis().set_ticks([])
        self.ax.get_xaxis().set_ticklabels([])

        self.fig.subplots_adjust(left=0.08, right=0.92, top=0.95, bottom=0.05)
        self.canvas.draw_idle()
