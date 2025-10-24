import tkinter as tk
from word_loader import load_words, generate_random_text, detect_word_files
from settings_window import SettingsWindow
from finish_info import FinishInfo
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
        self.finished = False
        self.typed_words = []

        self.wrong = 0

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
import tkinter as tk
from word_loader import load_words, generate_random_text, detect_word_files
from settings_window import SettingsWindow
from finish_info import FinishInfo
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
        self.finished = False
        self.typed_words = []

        self.wrong = 0
        self.wrong_streak = 0
        self.last_wrong = False

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

        if self.finished:
            return

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
                    self.last_wrong = False
                else:
                    self.text_widget.insert(f"1.{self.index}", char_to_show)
                    self.text_widget.tag_add("red", f"1.{self.index}", f"1.{self.index+1}")
                    self.wrong += 1

                    if not self.last_wrong:
                        self.wrong_streak += 1

                    self.last_wrong = True
                self.index += 1

        if self.start_time is None:
            self.start_time = current_time
            self.time = current_time

        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tk.DISABLED)

        # Finish test
        if self.index >= len(self.text):
            self.finished = True
            self.finish_test()

    def get_time_live(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time
    
    def end_test(self):
        self.text_widget.config(state=tk.DISABLED)
        if hasattr(self, "wpm_chart"):
            self.wpm_chart.reset_chart()

        self.index = 0
        self.start_time = None
        self.finished = False
        self.typed_words = []
        self.wrong_streak = 0
        self.wrong = 0

        self.generate_text(num_words=self.words_goal)

        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.focus_set()
        self.finish_info._clear_display()

    def finish_test(self):
        elapsed_time = self.get_time_live()
        num_chars = len(self.text)
        num_words = num_chars / 5
        base_wpm = (num_words / (elapsed_time / 60)) if elapsed_time > 0 else 0

        # --- Accuracy ---
        accuracy = max(0, 1 - self.wrong / num_chars)  # value between 0 and 1

        # --- Monkeytype-style WPM ---
        wpm = base_wpm * accuracy

        # --- Show finish info panel ---
        if hasattr(self, "finish_info"):
            self.finish_info.show(
                wpm=wpm,
                accuracy=accuracy * 100,  # convert to percentage
                errors=self.wrong_streak,
                on_restart=self.end_test
            )
