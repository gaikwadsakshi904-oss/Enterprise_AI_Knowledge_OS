import os
import pandas as pd
from pypdf import PdfReader


def load_documents(folder_path):
    documents = []

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        # PDF files
        if filename.lower().endswith(".pdf"):

            try:
                reader = PdfReader(file_path)

                text = ""

                for page in reader.pages:
                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

                if text.strip():
                    documents.append(text)

            except Exception as e:
                print(f"Error reading PDF {filename}: {e}")

        # TXT files
        elif filename.lower().endswith(".txt"):

            try:
                with open(
                    file_path,
                    "r",
                    encoding="utf-8"
                ) as f:

                    text = f.read()

                if text.strip():
                    documents.append(text)

            except Exception as e:
                print(f"Error reading TXT {filename}: {e}")

    return documents


def split_documents(documents, chunk_size=500):

    chunks = []

    for document in documents:

        words = document.split()

        for i in range(0, len(words), chunk_size):

            chunk = " ".join(
                words[i:i + chunk_size]
            )

            if chunk.strip():
                chunks.append(chunk)

    return chunks