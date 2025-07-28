from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from extract_text import extract_resume_texts
from preprocess import clean_text

def rank_resumes(folder_path, job_description):
    # Step 1: Extract and preprocess resumes
    raw_texts = extract_resume_texts(folder_path)
    cleaned_texts = {name: clean_text(text) for name, text in raw_texts.items()}

    # Step 2: Add job description to the list
    all_docs = list(cleaned_texts.values())
    all_docs.insert(0, clean_text(job_description))  # first item is JD

    # Step 3: Vectorize with TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_docs)

    # Step 4: Calculate cosine similarity
    jd_vector = tfidf_matrix[0]  # Job description
    resume_vectors = tfidf_matrix[1:]  # Resumes

    similarities = cosine_similarity(jd_vector, resume_vectors).flatten()

    # Step 5: Rank and return
    ranked = sorted(zip(cleaned_texts.keys(), similarities), key=lambda x: x[1], reverse=True)

    df = pd.DataFrame(ranked, columns=["Resume", "Score"])
    return df

if __name__ == "__main__":
    jd = """
    We are hiring a Data Scientist with strong skills in Python, machine learning,
    data analysis, and experience with NLP or TensorFlow.
    """
    results = rank_resumes("resumes", jd)
    print("\n🏆 Ranked Resumes:")
    print(results)
    results.to_csv("ranked_resumes.csv", index=False)
