from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def rank_resumes(job_description, resumes):

    documents = [
        job_description
    ] + [
        resume["text"] for resume in resumes
    ]

    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform(documents)

    scores = cosine_similarity(
        matrix[0:1],
        matrix[1:]
    )[0]

    results = []

    for resume, score in zip(resumes, scores):
        results.append({
            "filename": resume["filename"],
            "score": round(score * 100, 2)
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results
