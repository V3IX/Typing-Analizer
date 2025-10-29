import tkinter as tk
from word_loader import detect_word_files

class SettingsWindow:
    def __init__(self, master, typing_window):
        self.master = master
        self.typing_window = typing_window
        self.word_files = detect_word_files()
        self.word_var = tk.StringVar(value=self.typing_window.word_list_choice)
        self.open_settings()

    def open_settings(self):
        settings_win = tk.Toplevel(self.master)
        settings_win.title("Settings")
        settings_win.geometry("350x250")
        settings_win.configure(bg="#3e3e3e")
        settings_win.resizable(False, False)

        # Center window
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()
        x = main_x + (main_width // 2) - (350 // 2)
        y = main_y + (main_height // 2) - (250 // 2)
        settings_win.geometry(f"350x250+{x}+{y}")

        # Word list dropdown
        tk.Label(settings_win, text="Word list:", bg="#3e3e3e", fg="white").pack(pady=5)
        dropdown = tk.OptionMenu(
            settings_win,
            self.word_var,
            *self.word_files,
            command=lambda _: self.typing_window.set_word_list(self.word_var.get())
        )
        dropdown.config(bg="#4e4e4e", fg="white", highlightthickness=0)
        dropdown["menu"].config(bg="#4e4e4e", fg="white")
        dropdown.pack(pady=5)
