import requests
import re
from bs4 import BeautifulSoup

DUOME_URL = "https://www.duome.eu"
DUOME_VOCABULARY_PATH = "/vocabulary/en/pl"


def get_user_id(user):
    url = f"{DUOME_URL}/{user}/en/pl"
    html = get_html(url)
    match = re.search(r"/vocabulary/en/pl/(\d+)", html)
    if match:
        return match.group(1)
    else:
        raise Exception("No user found")


def get_html(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    html = response.text
    return html


def extract_vocabulary(user):
    user_id = get_user_id(user)
    url = f"{DUOME_URL}/{DUOME_VOCABULARY_PATH}/{user_id}"
    html = get_html(url)
    soup = BeautifulSoup(html, "html.parser")
    words_li_list = soup.select("#words li")

    vocabulary = []
    for word_li in words_li_list:
        word_polish_span = word_li.select_one("._blue.wA")
        if not word_polish_span:
            continue
        word_polish = word_polish_span.text
        word_english_translation = word_li.select_one(".cCCC.wT").text.replace(" - ", "")
        vocabulary.append((word_polish, word_english_translation))
    return vocabulary


def save_vocabulary_to_file(vocabulary, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for (word, translation) in vocabulary:
            file.write(f"{word};{translation}\n")


if __name__ == '__main__':
    user = input("Username: ")
    vocabulary = extract_vocabulary(user)
    save_vocabulary_to_file(vocabulary, f"files/{user}.txt")
    print("Saved vocabulary to", f"files/{user}.txt")
