from collections import Counter
from pathlib import Path

import regex as re
import spacy

FILES_PATH = Path("subtitles/")
KNOWN_WORDS_PATH = Path("files/known_words.txt")


def find_popular_words():
    print("Finding popular words...")
    counts = Counter()
    words_regex = re.compile(r"\p{L}+")
    nlp = spacy.load("pl_core_news_md")
    for file in FILES_PATH.iterdir():
        for line in file.open("r"):
            words = words_regex.findall(line)
            words_lower_case = [w.lower() for w in words]
            docs = nlp.pipe(words_lower_case, batch_size=1000)
            words_lower_case = [doc[0].lemma_ for doc in docs]
            counts.update(words_lower_case)
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
