import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


stop_words = set(ENGLISH_STOP_WORDS)


def preprocess_text(text):
    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9 ]", "", text)

    words = text.split()

    words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(words)
