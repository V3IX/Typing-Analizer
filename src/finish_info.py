import tkinter as tk
from tkinter import ttk
import logging

logger = logging.getLogger(__name__)
class FinishInfo(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#2e2e2e")
        self.visible = False
        self.on_restart = None
        self.on_replay = None
        self.replay = None

        self.finish_info_mode = "always"
        self.results_ready = False  # track whether there’s something to show

        # --- Style ---
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor="#1f1f1f",
            bordercolor="#1f1f1f",
            background="#00c853",
            lightcolor="#00c853",
            darkcolor="#00c853",
            thickness=10,
        )

        # --- Labels ---
        self.wpm_label = tk.Label(self, text="", font=("Consolas", 24, "bold"), fg="white", bg="#2e2e2e")
        self.accuracy_label = tk.Label(self, text="", font=("Consolas", 18), fg="#cccccc", bg="#2e2e2e")
        self.errors_label = tk.Label(self, text="", font=("Consolas", 16), fg="#999999", bg="#2e2e2e")

        self.wpm_label.pack(pady=(10, 2))
        self.accuracy_label.pack(pady=2)
        self.errors_label.pack(pady=2)

        # --- Progress bars ---
        self.progress_frame = tk.Frame(self, bg="#2e2e2e")
        self.progress_frame.pack(pady=(10, 0))

        tk.Label(self.progress_frame, text="WPM", fg="#aaaaaa", bg="#2e2e2e", font=("Consolas", 12)).pack(pady=(5, 0))
        self.wpm_bar = ttk.Progressbar(self.progress_frame, length=300, mode="determinate", maximum=200,
                                       style="Modern.Horizontal.TProgressbar")
        self.wpm_bar.pack(pady=(0, 5))

        tk.Label(self.progress_frame, text="Accuracy", fg="#aaaaaa", bg="#2e2e2e", font=("Consolas", 12)).pack(pady=(5, 0))
        self.accuracy_bar = ttk.Progressbar(self.progress_frame, length=300, mode="determinate", maximum=30,
                                            style="Modern.Horizontal.TProgressbar")
        self.accuracy_bar.pack(pady=(0, 10))

        # --- Buttons ---
        self.button_frame = tk.Frame(self, bg="#2e2e2e")
        self.button_frame.pack(pady=10)

        self.restart_button = ttk.Button(self.button_frame, text="Restart Test", command=self._handle_restart)
        self.restart_button.pack(side="left", padx=10)

        self.replay_button = ttk.Button(self.button_frame, text="Replay Test", command=self._handle_replay)
        self.replay_button.pack(side="left", padx=10)

        master.bind("<Return>", self._handle_enter)
        logger.info("FinishInfo initialized")

    # ------------------- Button handlers -------------------
    def _handle_restart(self):
        if self.on_restart:
            self._clear_display()
            self.on_restart()
        logger.info("Restart button pressed")

    def _handle_replay(self):
        if self.replay:
            return
        if self.on_replay:
            self.replay = True
            self.on_replay()
        logger.info("Replay button pressed")

    def _handle_enter(self, event):
        if self.on_restart:
            self._clear_display()
            self.on_restart()
        logger.info("Enter key pressed for restart")

    # ------------------- Core logic -------------------
    def _clear_display(self):
        self.wpm_label.config(text="")
        self.accuracy_label.config(text="")
        self.errors_label.config(text="")
        self.wpm_bar["value"] = 0
        self.accuracy_bar["value"] = 0
        self.results_ready = False
        self._update_visibility()
        logger.info("FinishInfo display cleared")

    def show(self, wpm=None, accuracy=None, errors=None, on_restart=None, on_replay=None):
        """Update and optionally show results depending on mode."""
        if wpm is not None:
            self.on_restart = on_restart
            self.on_replay = on_replay
            self.replay = False
            self.results_ready = True

            # Update stats
            self.wpm_label.config(text=f"{wpm:.1f} WPM")
            self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
            self.errors_label.config(text=f"Errors: {errors}")

            # Update bars
            self.wpm_bar["value"] = min(wpm, 200)
            scaled_accuracy = max(0, min(accuracy - 70, 30))
            self.accuracy_bar["value"] = scaled_accuracy

        self._update_visibility()
        logger.info("FinishInfo shown with WPM: %.1f, Accuracy: %.1f%%, Errors: %d", wpm, accuracy, errors)

    def hide(self):
        """Force hide, regardless of mode."""
        self.pack_forget()
        self.visible = False

    def set_mode(self, mode):
        """Change visibility behavior."""
        self.finish_info_mode = mode
        self._update_visibility()

    def _update_visibility(self):
        """Smart logic to decide whether to show or hide."""
        if self.finish_info_mode == "hidden":
            self.hide()
        elif self.finish_info_mode == "always":
            if not self.visible:
                self.pack(fill="x", padx=20, pady=(0, 20))
                self.visible = True
        elif self.finish_info_mode == "after":
            if self.results_ready:
                if not self.visible:
                    self.pack(fill="x", padx=20, pady=(0, 20))
                    self.visible = True
            else:
                self.hide()
        logger.info("FinishInfo visibility updated: mode=%s, visible=%s", self.finish_info_mode, self.visible)