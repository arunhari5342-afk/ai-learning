import re

import spacy


# Load the English spaCy model once.
nlp = spacy.load("en_core_web_sm")


def preprocess_text(text: str) -> list[str]:
    """
    Clean and preprocess text.

    Steps:
    1. Convert text to lowercase
    2. Tokenize
    3. Remove stop words
    4. Remove punctuation
    5. Remove numbers
    6. Lemmatize
    """

    # Convert input to lowercase
    text = text.lower()

    # Process the text using spaCy
    doc = nlp(text)

    tokens = []

    for token in doc:

        # Skip stop words
        if token.is_stop:
            continue

        # Skip punctuation
        if token.is_punct:
            continue

        # Skip spaces
        if token.is_space:
            continue

        # Skip numbers
        if token.like_num:
            continue

        # Get the base/dictionary form
        lemma = token.lemma_.strip()

        # Ignore empty values
        if not lemma:
            continue

        tokens.append(lemma)

    return tokens


def preprocess_to_string(text: str) -> str:
    """
    Preprocess text and return the result as a single string.
    """

    tokens = preprocess_text(text)

    return " ".join(tokens)