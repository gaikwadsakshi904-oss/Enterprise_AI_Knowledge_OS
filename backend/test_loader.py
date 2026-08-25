from document_loader import DocumentLoader
from config import DOCUMENT_FOLDER

loader = DocumentLoader()

docs = loader.load_documents(DOCUMENT_FOLDER)

print("Documents Loaded:", len(docs))

for doc in docs:
    print(doc["filename"])