import os
import pandas as pd
from pypdf import PdfReader


class DocumentLoader:

    def load_pdf(self, path):
        text = ""

        reader = PdfReader(path)

        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text


    def load_txt(self, path):

        with open(path, "r", encoding="utf-8") as file:
            return file.read()


    def load_csv(self, path):

        df = pd.read_csv(path)

        return df.to_string(index=False)


    def load_documents(self, folder):

        documents = []

        for file in os.listdir(folder):

            path = os.path.join(folder, file)

            if file.endswith(".pdf"):
                text = self.load_pdf(path)

            elif file.endswith(".txt"):
                text = self.load_txt(path)

            elif file.endswith(".csv"):
                text = self.load_csv(path)

            else:
                continue

            documents.append(
                {
                    "filename": file,
                    "content": text
                }
            )

        return documents