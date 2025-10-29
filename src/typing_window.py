from word_loader import load_words, generate_random_text, detect_word_files
from settings_window import SettingsWindow
from finish_info import FinishInfo
from user_window import UserWindow

import tkinter as tk
import database
import logging
import time
import os

logger = logging.getLogger(__name__)
# typing_window.py
class TypingWindow(tk.Frame):
    def __init__(self, master, click_sound, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="#2e2e2e")
        self.finish_info = FinishInfo(master=self)
        
        self.click_sound = click_sound

        self.word_list_choice = ""
        self.index = 0
        self.start_time = None
        self.finished = False

        self.wrong = 0
        self.wrong_streak = 0
        self.last_wrong = False

        self.user_input = []
        self.key_times = []
        self.last_key_time = None

        self.replay_mode = False

        # --- Text widget ---
        self.text_widget = tk.Text(
            self, font=("Consolas", 24), bg="#2e2e2e",
            height=5, width=50, bd=0, highlightthickness=0,
            wrap="word"
        )
        self.text_widget.pack(pady=20, fill="x")

        self.text_widget.tag_config("gray", foreground="gray")
        self.text_widget.tag_config("white", foreground="white")
        self.text_widget.tag_config("red", foreground="red")
        self.text_widget.tag_configure("center", justify="center")

        self.text_widget.focus_set()
        self.text_widget.bind("<Key>", self.on_keypress)

        # --- Detect word files ---
        self.word_files = detect_word_files()
        if self.word_files:
            self.word_list_choice = self.word_files[0]

        # --- Load initial text ---
        self.generate_text()

    def set_word_list(self, choice):
        self.word_list_choice = choice
        self.generate_text()

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

    def on_keypress(self, event):
        if len(event.char) == 1 or event.keysym == "BackSpace":
            letter = "\b" if event.keysym == "BackSpace" else event.char

            current_time = time.perf_counter()
            if not hasattr(self, "last_key_time") or self.last_key_time is None:
                key_delta = 0
            else:
                key_delta = current_time - self.last_key_time
            self.last_key_time = current_time

            # --- Record key and time delta ---
            if not hasattr(self, "user_input"):
                self.user_input = []
            if not hasattr(self, "key_times"):
                self.key_times = []

            typed_char = "\b" if event.keysym == "BackSpace" else event.char
            self.user_input.append(typed_char)
            self.key_times.append(key_delta)

            logger.debug(
                "Key pressed: '%s', delta=%.4f, index=%d",
                typed_char,
                key_delta,
                getattr(self, "index", 0)
            )

            self.type(letter)
            
    def type(self, letter):
        if self.finished:
            return

        current_time = time.time()
        self.text_widget.config(state=tk.NORMAL)

        # Handle backspace
        if letter == "\b":
            if self.index > 0:
                self.index -= 1
                self.text_widget.delete(f"1.{self.index}")
                self.text_widget.insert(f"1.{self.index}", self.text[self.index])
                self.text_widget.tag_add("gray", f"1.{self.index}", f"1.{self.index+1}")
                logger.debug("Backspace pressed, index=%d", self.index)
        else:
            if self.index < len(self.text):
                expected_char = self.text[self.index]
                self.text_widget.delete(f"1.{self.index}")

                self.click_sound.play()
                if letter == expected_char:
                    self.text_widget.insert(f"1.{self.index}", letter)
                    self.text_widget.tag_add("white", f"1.{self.index}", f"1.{self.index+1}")
                    self.last_wrong = False
                    logger.debug("Typed correct letter '%s' at index=%d", letter, self.index)
                else:
                    self.text_widget.insert(f"1.{self.index}", letter)
                    self.text_widget.tag_add("red", f"1.{self.index}", f"1.{self.index+1}")
                    self.wrong += 1
                    if not self.last_wrong:
                        self.wrong_streak += 1
                    self.last_wrong = True
                    logger.debug("Typed WRONG letter '%s' at index=%d, wrong=%d", letter, self.index, self.wrong)

                self.index += 1

        if self.start_time is None:
            self.start_time = current_time
            self.time = current_time
            logger.debug("Test started at %f", self.start_time)

        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tk.DISABLED)

        # Update WPM chart if exists
        if hasattr(self, "wpm_chart"):
            self.wpm_chart.update_chart()

        # Finish test automatically
        if self.index >= len(self.text) and self.last_wrong == False:
            self.finished = True
            logger.info("Test finished automatically")
            self.finish_test()

    def get_time_live(self):
        if self.start_time is None:
            return 0
        return time.time() - self.start_time
    
    def end_test(self):
        logger.info("Ending test")
        
        self.text_widget.config(state=tk.DISABLED)
        if hasattr(self, "wpm_chart"):
            self.wpm_chart.reset_chart()
            logger.debug("WPM chart reset")

        self.index = 0
        self.start_time = None
        self.finished = False
        self.wrong_streak = 0
        self.wrong = 0
        logger.debug("Test state reset: index=%d, wrong=%d, wrong_streak=%d",
                    self.index, self.wrong, self.wrong_streak)

        self.user_input = []
        self.key_times = []
        self.last_key_time = None
        logger.debug("User input and key times cleared")

        if not getattr(self, "replay_mode", False):
            logger.info("Generating new text for next test")
            self.generate_text(num_words=self.words_goal)

        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.focus_set()
        self.finish_info._clear_display()
        logger.info("Test ready for user input")

    def finish_test(self):
        elapsed_time = self.get_time_live()
        num_chars = len(self.text)
        num_words = num_chars / 5
        base_wpm = (num_words / (elapsed_time / 60)) if elapsed_time > 0 else 0

        # --- Accuracy ---
        accuracy = max(0, 1 - self.wrong / num_chars)  # value between 0 and 1

        # --- Monkeytype-style WPM ---
        wpm = base_wpm * accuracy

        logger.info("Test finished")
        logger.debug("Elapsed time: %.2f seconds", elapsed_time)
        logger.debug("Num chars: %d, Num words: %.2f", num_chars, num_words)
        logger.debug("Base WPM: %.2f, Accuracy: %.2f%%", base_wpm, accuracy*100)
        logger.debug("Final WPM (monkeytype style): %.2f", wpm)
        logger.debug("Errors: %d, Wrong streak: %d", self.wrong, self.wrong_streak)
        logger.debug("User input length: %d, Key times length: %d", len(self.user_input), len(self.key_times))

        # --- Show finish info panel ---
        if hasattr(self, "finish_info"):
            self.finish_info.show(
                wpm=wpm,
                accuracy=accuracy * 100,  # convert to percentage
                errors=self.wrong_streak,
                on_restart=self.end_test,
                on_replay=self.replay
            )

        if not getattr(self, "replay_mode", False):
            # --- Save results to database ---
            database.save_test_result(
                wpm=wpm,
                accuracy=accuracy,
                num_words=len(self.text.split()),
                expected_text=self.text,
                user_input=self.user_input,
                key_times=self.key_times
            )

        logger.info("Test results saved to database")
        print(database.get_all_test_results())

    def replay(self, data=None):
        """Replay a specific test (or the most recent one if none given)."""

        logger = logging.getLogger(__name__)
        logger.info("Starting replay of test")

        # Load test data
        if data is None:
            data = database.get_latest_test_result()
            if not data:
                logger.warning("No saved test found in database. Replay aborted.")
                return

        self.replay_mode = True
        logger.debug("Ending current test (if any) before replay")
        self.end_test()

        # Restore text and replay data
        self.text = data["text"]
        self.user_input = data["user_input"]
        self.key_times = data["key_times"]
        logger.info("Loaded test from database: %d characters, %d key presses",
                    len(self.text), len(self.user_input))

        # Reset text display
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert("1.0", self.text)
        self.text_widget.tag_add("gray", "1.0", "end")
        self.text_widget.tag_add("center", "1.0", "end")
        self.text_widget.config(state=tk.DISABLED)
        logger.debug("Text widget reset for replay")

        self.index = 0
        self.finished = False
        self.wrong = 0

        time.sleep(0.5)  # small pause before starting

        # Replay animation
        def replay_step(i):
            if i < len(self.user_input):
                char = self.user_input[i]
                delay = self.key_times[i] if i < len(self.key_times) else 0
                logger.debug("Replaying char %d: '%s' (delay: %.3f s)", i, char, delay)
                self.type(char)
                self.after(int(delay * 1000), lambda: replay_step(i + 1))
            else:
                # Replay done
                self.finished = True
                logger.info("Replay finished. Total characters replayed: %d", len(self.user_input))
                self.finish_test()
                self.replay_mode = False

        replay_step(0)
