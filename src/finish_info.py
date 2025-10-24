import tkinter as tk
from tkinter import ttk

class FinishInfo(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#2e2e2e")
        self.visible = False
        self.on_restart = None

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

        # --- Stat labels ---
        self.wpm_label = tk.Label(
            self, text="", font=("Consolas", 24, "bold"), fg="white", bg="#2e2e2e"
        )
        self.accuracy_label = tk.Label(
            self, text="", font=("Consolas", 18), fg="#cccccc", bg="#2e2e2e"
        )
        self.errors_label = tk.Label(
            self, text="", font=("Consolas", 16), fg="#999999", bg="#2e2e2e"
        )

        self.wpm_label.pack(pady=(10, 2))
        self.accuracy_label.pack(pady=2)
        self.errors_label.pack(pady=2)

        # --- Progress bars ---
        self.progress_frame = tk.Frame(self, bg="#2e2e2e")
        self.progress_frame.pack(pady=(10, 0))

        tk.Label(
            self.progress_frame, text="WPM", fg="#aaaaaa", bg="#2e2e2e", font=("Consolas", 12)
        ).pack(pady=(5, 0))
        self.wpm_bar = ttk.Progressbar(
            self.progress_frame,
            length=300,
            mode="determinate",
            maximum=200,
            style="Modern.Horizontal.TProgressbar",
        )
        self.wpm_bar.pack(pady=(0, 5))

        tk.Label(
            self.progress_frame, text="Accuracy", fg="#aaaaaa", bg="#2e2e2e", font=("Consolas", 12)
        ).pack(pady=(5, 0))
        self.accuracy_bar = ttk.Progressbar(
            self.progress_frame,
            length=300,
            mode="determinate",
            maximum=30,  # represents 70–100%
            style="Modern.Horizontal.TProgressbar",
        )
        self.accuracy_bar.pack(pady=(0, 10))

        # --- Buttons ---
        self.button_frame = tk.Frame(self, bg="#2e2e2e")
        self.button_frame.pack(pady=10)

        self.restart_button = ttk.Button(
            self.button_frame, text="Restart Test", command=self._handle_restart
        )
        self.restart_button.pack(side="left", padx=10)

        # Bind Enter key
        master.bind("<Return>", self._handle_enter)

        # self.hide()

    def _handle_restart(self):
        """Restart when button pressed."""
        if self.on_restart:
            # self.hide()
            self._clear_display()
            self.on_restart()

    def _handle_enter(self, event):
        """Restart test when Enter is pressed."""
        if self.visible and self.on_restart:
            # self.hide()
            self._clear_display()
            self.on_restart()

    def _clear_display(self):
        """Reset all labels and bars."""
        self.wpm_label.config(text="")
        self.accuracy_label.config(text="")
        self.errors_label.config(text="")
        self.wpm_bar["value"] = 0
        self.accuracy_bar["value"] = 0

    def show(self, wpm, accuracy, errors, on_restart):
        """Display results and show the frame."""
        self.on_restart = on_restart

        self.wpm_label.config(text=f"{wpm:.1f} WPM")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.1f}%")
        self.errors_label.config(text=f"Errors: {errors}")

        # Update progress bars
        self.wpm_bar["value"] = min(wpm, 200)

        # Accuracy bar represents 70–100% range
        scaled_accuracy = max(0, min(accuracy - 70, 30))
        self.accuracy_bar["value"] = scaled_accuracy

        self.visible = True
        self.pack(fill="x", padx=20, pady=(0, 20))

    def hide(self):
        """Hide the finish info frame."""
        if self.visible:
            self.pack_forget()
            self.visible = False
