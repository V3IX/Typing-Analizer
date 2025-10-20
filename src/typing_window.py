import tkinter as tk
from word_loader import load_words, generate_random_text, detect_word_files
from settings_window import SettingsWindow
import os

class TypingWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Typing Test")
        self.master.geometry("800x300")
        self.master.configure(bg="#2e2e2e")

        self.red_mode = "typed"
        self.word_list_choice = ""
        self.index = 0

        # Text widget
        self.text_widget = tk.Text(master, font=("Consolas", 24), bg="#2e2e2e",
                                   height=2, width=50, bd=0, highlightthickness=0)
        self.text_widget.pack(pady=100)

        # Tags
        self.text_widget.tag_config("gray", foreground="gray")
        self.text_widget.tag_config("white", foreground="white")
        self.text_widget.tag_config("red", foreground="red")
        self.text_widget.tag_configure("center", justify="center")

        # Settings button
        self.settings_button = tk.Button(master, text="⚙", command=self.open_settings,
                                         font=("Arial", 12, "bold"), bg="#4e4e4e", fg="white", bd=0, relief="raised")
        self.settings_button.place(relx=0.5, rely=0.05, anchor="n")

        # Bind typing
        master.bind("<Key>", self.on_keypress)

        # Detect word files
        self.word_files = detect_word_files()
        if self.word_files:
            self.word_list_choice = self.word_files[0]

        # Load initial text
        self.load_random_text_for_typing()

    # --------------------- Settings ---------------------
    def open_settings(self):
        SettingsWindow(self.master, self)

    def set_red_mode(self, mode):
        self.red_mode = mode

    def set_word_list(self, choice):
        self.word_list_choice = choice
        self.load_random_text_for_typing()

    # --------------------- Load & generate text ---------------------
    def load_random_text_for_typing(self):
        file_path = os.path.join("data/words", self.word_list_choice)
        words = load_words(file_path)
        self.text = generate_random_text(words, num_words=50)
        self.index = 0

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
                else:
                    self.text_widget.insert(f"1.{self.index}", char_to_show)
                    self.text_widget.tag_add("red", f"1.{self.index}", f"1.{self.index+1}")
                self.index += 1

        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tk.DISABLED)
