from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from groq import Groq
import os
import tempfile

router = APIRouter(prefix="/documents", tags=["Documents"])

def extract_text(path, filename):
    if filename.lower().endswith(".pdf"):
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

@router.post("/upload-summary")
async def upload_summary(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".pdf", ".txt")):
        raise HTTPException(400, "Only PDF and TXT files are supported")

    suffix = os.path.splitext(file.filename)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        path = tmp.name

    try:
        text = extract_text(path, file.filename)

        if not text.strip():
            raise HTTPException(400, "No readable text found")

        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        prompt = f"""
Summarize the following document.

Return exactly:
SUMMARY:
A clear concise summary.

KEY POINTS:
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

DOCUMENT:
{text[:30000]}
"""

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        result = response.choices[0].message.content

        return {
            "filename": file.filename,
            "characters": len(text),
            "summary": result,
            "status": "success"
        }

    finally:
        try:
            os.remove(path)
        except:
            pass

