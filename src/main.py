from database import init_db
init_db()

import tkinter as tk
from typing_window import TypingWindow
from settings_window import SettingsWindow
from wpm_chart import WPMChart
from settings_strip import SettingsStrip
from finish_info import FinishInfo
from typing_analyzer import DigraphTable

import logging
import os
import pygame

# --- Initialize Pygame mixer for sound effects ---
pygame.mixer.init()
CLICK_SOUND = pygame.mixer.Sound("data/sounds/osu-hit-sound.mp3")
CLICK_SOUND.set_volume(0.5)

# --- Logging setup ---
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "typing_app.log")

# Make sure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Remove old log file
if os.path.exists(LOG_FILE):
    os.remove(LOG_FILE)

# Configure logging to file + console
logging.basicConfig(
    level=logging.DEBUG,  # log everything you want
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w', encoding='utf-8'),
        logging.StreamHandler()  # also log to console
    ]
)

# Suppress noisy libraries
logging.getLogger("PIL").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)
logging.getLogger("tkinter").setLevel(logging.WARNING)

logger = logging.getLogger("typing_app")

logger.info("Logging initialized. Log file: %s", LOG_FILE)

root = tk.Tk()
root.title("Typing Trainer")
root.geometry("900x600")
root.configure(bg="#2e2e2e")

typing_frame = TypingWindow(root, CLICK_SOUND)
settings_strip = SettingsStrip(root, typing_frame)
wpm_chart = WPMChart(root, typing_frame)
finish_info = FinishInfo(root)
table_info = DigraphTable(root)

settings_strip.pack(fill="x", padx=20, pady=(10,5))
typing_frame.pack(fill="x", padx=20, pady=(0,10))
wpm_chart.pack(fill="both", padx=20, pady=(0,10))
finish_info.pack(fill="x", padx=20, pady=(0,20))

typing_frame.wpm_chart = wpm_chart
typing_frame.finish_info = finish_info
typing_frame.table_info = table_info

root.mainloop()
