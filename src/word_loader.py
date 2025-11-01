import os
import random
import logging

logger = logging.getLogger(__name__)
def detect_word_files(folder="data/words"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    logger.info("Detected word files: %s", folder)
    return [f for f in os.listdir(folder) if f.endswith(".txt")]

def load_words(file_path):
    if not os.path.exists(file_path):
        return ["error", "file", "not", "found"]
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    logger.info("Loaded %d words from %s", len(text.split()), file_path)
    return text.split()

def generate_random_text(words, num_words=50):
    logger.info("Generated random text with %d words", num_words)
    return " ".join(random.choices(words, k=num_words))
