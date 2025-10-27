import database
import json
import random

# ---------------- Analysis ----------------
def analyze_slowest_letters(limit=2):
    """
    Returns a dict of letter -> average time (ms) based on the last `limit` tests.
    """
    tests = database.get_all_test_results()[:limit]
    letter_times = {}
    letter_counts = {}

    for test in tests:
        test_data = database.get_test_by_id(test[0])
        if not test_data:
            continue
        user_input = test_data["user_input"]
        key_times = [t*1000 for t in test_data["key_times"]]  # convert to ms
        for i, char in enumerate(user_input):
            t = key_times[i]
            letter_times[char] = letter_times.get(char, 0) + t
            letter_counts[char] = letter_counts.get(char, 0) + 1

    avg_times = {char: letter_times[char]/letter_counts[char] for char in letter_times}
    return avg_times


def analyze_slowest_combos(limit=2):
    """
    Returns a dict of 2-letter combo -> average time (ms) based on the last `limit` tests.
    """
    tests = database.get_all_test_results()[:limit]
    combo_times = {}
    combo_counts = {}

    for test in tests:
        test_data = database.get_test_by_id(test[0])
        if not test_data:
            continue
        user_input = test_data["user_input"]
        key_times = [t*1000 for t in test_data["key_times"]]
        for i in range(len(user_input)-1):
            combo = user_input[i] + user_input[i+1]
            t = key_times[i] + key_times[i+1]
            combo_times[combo] = combo_times.get(combo, 0) + t
            combo_counts[combo] = combo_counts.get(combo, 0) + 1

    avg_times = {combo: combo_times[combo]/combo_counts[combo] for combo in combo_times}
    return avg_times


# ---------------- Generate custom text ----------------
def generate_custom_text(length=50, mode="slowest_combos", limit=2):
    """
    Generate custom text using slowest letters or combos from recent tests.
    """
    if mode == "slowest_letters":
        avg_times = analyze_slowest_letters(limit=limit)
        slow_letters = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)
        letters = [l for l,_ in slow_letters]
        if not letters:
            return ""
        return "".join(random.choices(letters, k=length))

    elif mode == "slowest_combos":
        avg_times = analyze_slowest_combos(limit=limit)
        slow_combos = sorted(avg_times.items(), key=lambda x: x[1], reverse=True)
        combos = [c for c,_ in slow_combos]
        if not combos:
            return ""
        text = ""
        while len(text) < length:
            text += random.choice(combos)
        return text[:length]

    else:
        raise ValueError("Unknown mode: use 'slowest_letters' or 'slowest_combos'")
