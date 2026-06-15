from flask import Flask, request, jsonify, render_template
import pdfplumber
import docx
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import nltk
from nltk.corpus import stopwords
# Download the stopwords dataset (only needed once)
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# {
#     "a", "an", "the", "and", "or", "but", "if", "while",
#     "is", "am", "are", "was", "were", "be", "been",
#     "to", "from", "in", "on", "at", "for", "with",
#     "about", "as", "by", "of", "this", "that",
#     "it", "its", "their", "them", "they"
# }

app = Flask(__name__)


# ---------------- HOME PAGE ----------------

@app.route("/")
def home_page():
    return render_template("index.html")


# ---------------- PREPROCESS FUNCTION ----------------

def preprocess_text(text):

    text = text.lower()

    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)

    words = text.split()

    words = [word for word in words if word not in stop_words]

    cleaned_text = " ".join(words)

    return cleaned_text


# ---------------- MAIN ROUTE ----------------

@app.route("/Results", methods=["POST"])
def preprocess():

    files = request.files.getlist("file")

    # Job Description from form
    job_description = request.form.get("job_description")

    processed_jd = preprocess_text(job_description)

    results = []

    for file in files:

        print("Filename:", file.filename)

        text = ""

        # -------- PDF --------

        if file.filename.endswith(".pdf"):

            with pdfplumber.open(file) as pdf:

                text = "\n".join(
                    page.extract_text() or ""
                    for page in pdf.pages
                )

        # -------- DOCX --------

        elif file.filename.endswith(".docx"):

            doc = docx.Document(file)

            text = "\n".join(
                paragraph.text
                for paragraph in doc.paragraphs
            )

        else:
            return jsonify({
                "error": f"Unsupported file type: {file.filename}"
            }), 400

        # -------- PREPROCESS RESUME --------

        processed_resume = preprocess_text(text)

        # -------- TF-IDF --------

        documents = [processed_jd, processed_resume]

        tfidf = TfidfVectorizer()

        matrix = tfidf.fit_transform(documents)

        # -------- SIMILARITY SCORE --------

        score = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        results.append({
            "filename": file.filename,
            "score": round(score * 100, 2)
        })

    # -------- SORT BY SCORE --------

    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return render_template(
        "output.html",
        results=results
    )


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)