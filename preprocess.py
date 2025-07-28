import spacy
import re

# Load SpaCy English model
nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    # Lowercase + remove special chars
    text = text.lower()
    text = re.sub(r'\d+', '', text)                  # remove numbers
    text = re.sub(r'[^\w\s]', '', text)              # remove punctuation
    text = re.sub(r'\s+', ' ', text).strip()         # remove extra spaces

    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

    return " ".join(tokens)
from extract_text import extract_resume_texts
from preprocess import clean_text

if __name__ == "__main__":
    resumes = extract_resume_texts("resumes")
    for filename, text in resumes.items():
        print(f"\nOriginal ({filename[:20]}):\n{text[:300]}")
        cleaned = clean_text(text)
        print(f"\nCleaned ({filename[:20]}):\n{cleaned[:300]}")
        print("-" * 60)