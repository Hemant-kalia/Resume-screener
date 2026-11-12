import pdfplumber
import docx


def extract_text(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            text = "\n".join(
                page.extract_text() or ""
                for page in pdf.pages
            )

    elif filename.endswith(".docx"):
        document = docx.Document(file)

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

    else:
        raise ValueError(
            f"Unsupported file type: {file.filename}"
        )

    return text
