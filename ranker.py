from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

nltk.download('punkt_tab')

def calculate_similarity(resume_text, jd_text):
    documents = [resume_text, jd_text]
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return round(similarity[0][0] * 100, 2)

def extract_keywords(text):
    words = nltk.word_tokenize(text.lower())
    return list(set([word for word in words if word.isalpha() and len(word) > 3]))

def match_skills(resume_keywords, jd_keywords):
    matched_skills = set(resume_keywords) & set(jd_keywords)
    return matched_skills, len(matched_skills)

def calculate_job_title_relevance(resume_title, jd_title):
    # Use cosine similarity or another method to match job titles
    return calculate_similarity(resume_title, jd_title)

def generate_resume_suggestions(resume_text, jd_text):
    resume_keywords = set(extract_keywords(resume_text))
    jd_keywords = set(extract_keywords(jd_text))
    missing = jd_keywords - resume_keywords

    suggestions = []
    if missing:
        suggestions.append("Add relevant keywords found in the job description such as: " + ", ".join(list(missing)[:10]))
    if "project" not in resume_text.lower():
        suggestions.append("Mention at least one project to show practical experience.")
    if "intern" not in resume_text.lower():
        suggestions.append("Add any internship experiences to improve relevance.")

    return " ".join(suggestions) if suggestions else "Your resume aligns well with the job description!"
