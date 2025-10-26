import tkinter as tk
from settings_window import SettingsWindow
from typing_window import TypingWindow
from user_window import UserWindow


class SettingsStrip(tk.Frame):
    def __init__(self, master, typing_frame, **kwargs):
        super().__init__(master, bg="#3a3a3a", **kwargs)
        self.typing_frame = typing_frame

        # ---------------- Left: Words amount ----------------
        self.words_to_type = tk.IntVar(value=50)  # default
        self.active_button = None  # currently selected preset button

        options_frame = tk.Frame(self, bg="#3a3a3a")
        options_frame.pack(side="left", padx=10, pady=5)

        # Preset buttons
        self.buttons = []
        for val in [10, 25, 50, 100]:
            btn = tk.Button(
                options_frame, text=str(val), width=4, bg="#4e4e4e", fg="white",
                font=("Arial", 10), bd=0, command=lambda v=val, b=val: self.update_words(v, b)
            )
            btn.pack(side="left", padx=2)
            self.buttons.append(btn)

        # Custom entry
        self.custom_entry = tk.Entry(
            options_frame, width=5, textvariable=self.words_to_type,
            font=("Arial", 10)
        )
        self.custom_entry.pack(side="left", padx=(5,0))
        self.custom_entry.bind("<Return>", lambda e: self.update_words(self.words_to_type.get(), None))

        # Highlight default button (50)
        self.highlight_button(50)

        # ---------------- Right: Settings and User Button ----------------
        right_frame = tk.Frame(self, bg="#3a3a3a")
        right_frame.pack(side="right", padx=10)

        user_btn = tk.Button(
            right_frame, text="👤", font=("Arial", 12, "bold"),
            bg="#4e4e4e", fg="white", bd=0, relief="raised",
            command=self.open_user_window   # 👈 new method
        )
        user_btn.pack(side="left", padx=(0, 5))

        settings_btn = tk.Button(
            right_frame, text="⚙", font=("Arial", 12, "bold"),
            bg="#4e4e4e", fg="white", bd=0, relief="raised",
            command=self.open_settings
        )
        settings_btn.pack(side="left")


    # ---------------- Update word count ----------------
    def update_words(self, value, button_value):
        self.words_to_type.set(value)
        self.typing_frame.words_goal = value
        self.typing_frame.generate_text(num_words=value)

        # Highlight active preset button, deselect custom
        self.highlight_button(button_value)
        self.typing_frame.end_test()

    # ---------------- Highlight preset button ----------------
    def highlight_button(self, value):
        for btn in self.buttons:
            if int(btn["text"]) == value:
                btn.config(bg="#66cc66")  # highlight color
            else:
                btn.config(bg="#4e4e4e")  # default color

        # If custom entry is used, clear button highlight
        if value is None:
            for btn in self.buttons:
                btn.config(bg="#4e4e4e")

    # ---------------- Open Settings ----------------
    def open_settings(self):
        SettingsWindow(self.master, self.typing_frame)

    def open_user_window(self):
        UserWindow(self.master)