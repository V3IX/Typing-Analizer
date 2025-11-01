import tkinter as tk
from word_loader import detect_word_files
import logging

logger = logging.getLogger(__name__)
class SettingsWindow:
    def __init__(self, master, typing_window):
        self.master = master
        self.typing_window = typing_window
        self.wpm_chart = typing_window.wpm_chart
        self.finish_info = typing_window.finish_info
        self.table = typing_window.table_info

        self.word_files = detect_word_files()
        self.word_var = tk.StringVar(value=self.typing_window.word_list_choice)

        self.show_chart_var = tk.StringVar(value=self.wpm_chart.wpm_chart_mode)
        self.show_finish_var = tk.StringVar(value=self.finish_info.finish_info_mode)
        self.show_table_bool = tk.BooleanVar(value=self.table.visible)

        self.open_settings()
        logger.info("SettingsWindow initialized")

    def open_settings(self):
        settings_win = tk.Toplevel(self.master)
        settings_win.title("Settings")
        settings_win.geometry("350x250")
        settings_win.configure(bg="#3e3e3e")
        settings_win.resizable(True, True)

        # Center window
        main_x = self.master.winfo_x()
        main_y = self.master.winfo_y()
        main_width = self.master.winfo_width()
        main_height = self.master.winfo_height()
        x = main_x + (main_width // 2) - (350 // 2)
        y = main_y + (main_height // 2) - (250 // 2)
        settings_win.geometry(f"350x250+{x}+{y}")

        # --- Word list dropdown ---
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

        # --- WPM Chart toggle (PUT THIS HERE) ---
        tk.Label(settings_win, text="WPM Chart Mode:", bg="#3e3e3e", fg="white").pack(pady=(20, 5))
        chart_modes = [("Always Visible", "always"), ("Visible After Test", "after"), ("Hidden", "hidden")]
        for text, mode in chart_modes:
            tk.Radiobutton(
                settings_win,
                text=text,
                variable=self.show_chart_var,
                value=mode,
                bg="#3e3e3e",
                fg="white",
                selectcolor="#2e2e2e",
                command=self.toggle_chart
            ).pack(anchor="w", padx=60)

        # --- Finish Info toggle ---
        tk.Label(settings_win, text="Finish Info Mode:", bg="#3e3e3e", fg="white").pack(pady=(20, 5))
        finish_modes = [("Always Visible", "always"), ("Visible After Test", "after"), ("Hidden", "hidden")]
        for text, mode in finish_modes:
            tk.Radiobutton(
                settings_win,
                text=text,
                variable=self.show_finish_var,
                value=mode,
                bg="#3e3e3e",
                fg="white",
                selectcolor="#2e2e2e",
                command=self.toggle_finish_info
            ).pack(anchor="w", padx=60)

        # --- Digraph Table Visibility Toggle ---
        tk.Label(settings_win, text="Digraph Table:", bg="#3e3e3e", fg="white").pack(pady=(20, 5))
        tk.Checkbutton(
            settings_win,
            text="Show Table",
            variable=self.show_table_bool,
            bg="#3e3e3e",
            fg="white",
            selectcolor="#2e2e2e",
            command=self.toggle_table
        ).pack(anchor="w", padx=60)
        logger.info("Settings window opened")

    def toggle_chart(self):
        mode = self.show_chart_var.get()
        self.typing_window.wpm_chart_mode = mode
        self.typing_window.wpm_chart.set_mode(mode)

        if mode != "hidden" and self.typing_window.table_info.visible:
            self.show_table_bool.set(False)
            self.typing_window.table_info.visible = False
            self.typing_window.table_info.set_mode(False)
        logger.info("WPM Chart mode set to %s", mode)

    def toggle_finish_info(self):
        mode = self.show_finish_var.get()
        self.typing_window.finish_info_mode = mode
        self.typing_window.finish_info.set_mode(mode)

        if mode != "hidden" and self.typing_window.table_info.visible:
            self.show_table_bool.set(False)
            self.typing_window.table_info.visible = False
            self.typing_window.table_info.set_mode(False)
        logger.info("Finish Info mode set to %s", mode)

    def toggle_table(self):
        visible = self.show_table_bool.get()
        self.typing_window.table_info.visible = visible
        self.typing_window.table_info.set_mode(visible)

        if visible:
            self.show_chart_var.set("hidden")
            self.show_finish_var.set("hidden")

            self.typing_window.wpm_chart_mode = "hidden"
            self.typing_window.finish_info_mode = "hidden"
            self.typing_window.wpm_chart.set_mode("hidden")
            self.typing_window.finish_info.set_mode("hidden")
        logger.info("Digraph Table visibility set to %s", visible)
