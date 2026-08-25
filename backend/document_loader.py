from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader
from docx import Document

from config import (
    DOCUMENTS_DIR,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".docx",
}


# =========================================================
# PDF
# =========================================================

def read_pdf(file_path: Path) -> List[Dict]:

    reader = PdfReader(str(file_path))

    pages = []

    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text() or ""

        text = text.strip()

        if not text:
            continue

        pages.append({
            "text": text,
            "page": page_number,
        })

    return pages


# =========================================================
# TXT
# =========================================================

def read_txt(file_path: Path) -> List[Dict]:

    text = file_path.read_text(
        encoding="utf-8",
        errors="ignore",
    )

    text = text.strip()

    if not text:
        return []

    return [{
        "text": text,
        "page": None,
    }]


# =========================================================
# DOCX
# =========================================================

def read_docx(file_path: Path) -> List[Dict]:

    document = Document(
        str(file_path)
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    text = "\n".join(paragraphs)

    if not text:
        return []

    return [{
        "text": text,
        "page": None,
    }]


# =========================================================
# LOAD ONE FILE
# =========================================================

def load_file(
    file_path: Path
) -> List[Dict]:

    extension = (
        file_path.suffix.lower()
    )

    if extension == ".pdf":

        return read_pdf(file_path)

    if extension == ".txt":

        return read_txt(file_path)

    if extension == ".docx":

        return read_docx(file_path)

    raise ValueError(
        f"Unsupported file type: "
        f"{extension}"
    )


# =========================================================
# CHUNK TEXT
# =========================================================

def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    overlap: int = CHUNK_OVERLAP,
) -> List[str]:

    # Remove unnecessary whitespace
    text = " ".join(
        text.split()
    )

    if not text:
        return []

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[
            start:end
        ].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


# =========================================================
# LOAD ALL DOCUMENTS
# =========================================================

def load_documents(
    folder_path=None
) -> List[Dict]:

    # Allow old code to pass a folder
    # while defaulting to our configured
    # documents directory.

    if folder_path is None:

        folder = DOCUMENTS_DIR

    else:

        folder = Path(
            folder_path
        )

    if not folder.exists():

        print(
            f"Document folder does not exist: "
            f"{folder}"
        )

        return []

    all_chunks = []

    for file_path in sorted(
        folder.iterdir()
    ):

        if not file_path.is_file():
            continue

        if (
            file_path.suffix.lower()
            not in SUPPORTED_EXTENSIONS
        ):
            continue

        print(
            f"Processing: "
            f"{file_path.name}"
        )

        try:

            pages = load_file(
                file_path
            )

        except Exception as error:

            print(
                f"Failed to read "
                f"{file_path.name}: "
                f"{error}"
            )

            continue

        chunk_counter = 0

        for page_data in pages:

            chunks = chunk_text(
                page_data["text"]
            )

            for chunk in chunks:

                chunk_counter += 1

                all_chunks.append({

                    "chunk_id": (
                        f"{file_path.stem}_"
                        f"{chunk_counter}"
                    ),

                    "text": chunk,

                    "document": (
                        file_path.name
                    ),

                    "page": (
                        page_data.get("page")
                    ),

                    "source": (
                        file_path.name
                    ),
                })

    return all_chunks