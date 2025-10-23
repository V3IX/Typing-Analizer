import tkinter as tk
from word_loader import load_words, generate_random_text, detect_word_files
from settings_window import SettingsWindow
import time
import os

# typing_window.py
class TypingWindow(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#2e2e2e")

        self.red_mode = "typed"
        self.word_list_choice = ""
        self.index = 0
        self.start_time = None

        # Text widget
        self.text_widget = tk.Text(self, font=("Consolas", 24), bg="#2e2e2e",
                                   height=5, width=50, bd=0, highlightthickness=0,
                                   wrap="word")
        self.text_widget.pack(pady=20, fill="x")

        # Tags
        self.text_widget.tag_config("gray", foreground="gray")
        self.text_widget.tag_config("white", foreground="white")
        self.text_widget.tag_config("red", foreground="red")
        self.text_widget.tag_configure("center", justify="center")

        # Bind typing
        self.text_widget.focus_set()
        self.text_widget.bind("<Key>", self.on_keypress)

        # Detect word files
        self.word_files = detect_word_files()
        if self.word_files:
            self.word_list_choice = self.word_files[0]

        # Load initial text
        self.generate_text()

    # --------------------- Settings ---------------------
    def set_red_mode(self, mode):
        self.red_mode = mode

    def set_word_list(self, choice):
        self.word_list_choice = choice
        self.generate_text()

    # --------------------- Load & generate text ---------------------
    def generate_text(self, num_words=None):
        """
        Generate the typing text based on current word list and mode.
        num_words: number of words to generate (falls back to current goal)
        """
        if num_words is None:
            num_words = getattr(self, "words_goal", 50)  # default to 50 if not set

        file_path = os.path.join("data/words", self.word_list_choice)
        words = load_words(file_path)

        # --- Generate text (currently random, can add more modes later) ---
        self.text = generate_random_text(words, num_words=num_words)
        self.index = 0

        # --- Update text widget ---
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", self.text)
        self.text_widget.tag_add("gray", "1.0", "end")
        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tk.DISABLED)

    # --------------------- Typing logic ---------------------
    def on_keypress(self, event):
        if len(event.char) != 1 and event.keysym != "BackSpace":
            return

        current_time = time.time()

        self.text_widget.config(state=tk.NORMAL)

        if event.keysym == "BackSpace":
            if self.index > 0:
                self.index -= 1
                self.text_widget.delete(f"1.{self.index}")
                self.text_widget.insert(f"1.{self.index}", self.text[self.index])
                self.text_widget.tag_add("gray", f"1.{self.index}", f"1.{self.index+1}")
        else:
            if self.index < len(self.text):
                typed_char = event.char
                expected_char = self.text[self.index]
                self.text_widget.delete(f"1.{self.index}")
                char_to_show = typed_char if typed_char == expected_char or self.red_mode == "typed" else expected_char
                if typed_char == expected_char:
                    self.text_widget.insert(f"1.{self.index}", typed_char)
                    self.text_widget.tag_add("white", f"1.{self.index}", f"1.{self.index+1}")
                    
                    self.time = current_time
                else:
                    self.text_widget.insert(f"1.{self.index}", char_to_show)
                    self.text_widget.tag_add("red", f"1.{self.index}", f"1.{self.index+1}")
                self.index += 1

        if self.start_time is None:
            self.start_time = current_time
            self.time = current_time

        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tk.DISABLED)

    def get_time_live(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time