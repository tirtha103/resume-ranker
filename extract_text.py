from pdfminer.high_level import extract_text
import os

def extract_resume_texts(folder_path):
    texts = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            path = os.path.join(folder_path, filename)
            text = extract_text(path)
            texts[filename] = text
    return texts

if __name__ == "__main__":
    folder = "resumes"  # Folder that contains all PDF resumes
    extracted = extract_resume_texts(folder)
    for name, text in extracted.items():
        print(f"\n{name}\n{'-'*40}")
        print(text[:500])  # Only show first 500 characters of each resume
