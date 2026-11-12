from flask import Blueprint, request, jsonify, render_template

from app.services.extraction import extract_text
from app.services.preprocessing import preprocess_text
from app.services.matching import rank_resumes


resume_bp = Blueprint("resume", __name__)


@resume_bp.route("/")
def home_page():
    return render_template("index.html")


@resume_bp.route("/Results", methods=["POST"])
def preprocess():

    files = request.files.getlist("file")
    job_description = request.form.get("job_description", "")

    if not job_description.strip():
        return jsonify({
            "error": "Please provide a job description."
        }), 400

    if not files or not any(file.filename for file in files):
        return jsonify({
            "error": "Please upload at least one resume."
        }), 400

    processed_jd = preprocess_text(job_description)

    resumes = []

    try:
        for file in files:

            if not file.filename:
                continue

            text = extract_text(file)
            processed_resume = preprocess_text(text)

            resumes.append({
                "filename": file.filename,
                "text": processed_resume
            })

        if not resumes:
            return jsonify({
                "error": "No valid resumes were uploaded."
            }), 400

        results = rank_resumes(processed_jd, resumes)

    except ValueError as error:
        return jsonify({"error": str(error)}), 400

    except Exception:
        return jsonify({
            "error": "Unable to process the uploaded resumes."
        }), 500

    return render_template(
        "output.html",
        results=results
    )
