from collections import Counter
from pathlib import Path

import regex as re

FILES_PATH = Path("subtitles/")
KNOWN_WORDS_PATH = Path("files/known_words.txt")

def find_popular_words():
    print("Finding popular words...")
    counts = Counter()
    words_regex = re.compile(r"\p{L}+")
    for file in FILES_PATH.iterdir():
        for line in file.open("r"):
            words = words_regex.findall(line)
            words = [w.lower() for w in words]
            counts.update(words)
    return counts

def remove_known(words: Counter):
    known_words = KNOWN_WORDS_PATH.read_text(encoding="utf-8").splitlines()
    for word in known_words:
        words.pop(word, None)

def save_to_file():
    print("Saving popular words...")

if __name__ == "__main__":
    words = find_popular_words()
    remove_known(words)
    print("Total words: ", len(set(words)))
    count_of_counts = Counter(words.values())
    print(count_of_counts)
    print(words)
