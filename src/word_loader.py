import os
import random

def detect_word_files(folder="data/words"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    return [f for f in os.listdir(folder) if f.endswith(".txt")]

def load_words(file_path):
    if not os.path.exists(file_path):
        return ["error", "file", "not", "found"]
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    return text.split()

def generate_random_text(words, num_words=50):
    return " ".join(random.choices(words, k=num_words))
