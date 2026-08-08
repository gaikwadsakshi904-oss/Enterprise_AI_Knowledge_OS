
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from document_loader import load_documents, split_documents
from embedding import create_embeddings
from vector_store import create_index, save_index

from rag_pipeline import RAGPipeline

from keyword_extractor import extract_keywords
from entity_extractor import extract_entities

import os


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Enterprise AI Knowledge OS",
    description="Enterprise AI Knowledge Management System",
    version="1.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ============================================================
# GLOBAL RAG PIPELINE
# ============================================================

rag = None


# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "status": "success",
        "message": "Enterprise AI Knowledge OS Running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "rag_loaded": rag is not None
    }


# ============================================================
# INITIALIZE RAG
# ============================================================

@app.post("/initialize")
def initialize_rag():

    global rag

    try:

        rag = RAGPipeline()

        return {
            "status": "success",
            "message": "RAG Pipeline initialized successfully"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# ASK AI
# ============================================================

@app.get("/ask")
def ask(question: str):

    if rag is None:

        return {
            "status": "error",
            "message": "RAG Pipeline is not initialized. Open /initialize first."
        }

    try:

        result = rag.ask(question)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

@app.post("/upload")
async def upload(file: UploadFile = File(...)):

    try:

        documents_folder = "../documents"

        os.makedirs(
            documents_folder,
            exist_ok=True
        )

        file_path = os.path.join(
            documents_folder,
            file.filename
        )

        file_content = await file.read()

        with open(
            file_path,
            "wb"
        ) as f:

            f.write(file_content)


        # Load documents
        docs = load_documents(
            documents_folder
        )


        # Split documents
        chunks = split_documents(
            docs
        )


        # Create embeddings
        embeddings = create_embeddings(
            chunks
        )


        # Create FAISS index
        index = create_index(
            embeddings
        )


        # Make sure models folder exists
        os.makedirs(
            "models",
            exist_ok=True
        )


        # Save index
        save_index(
            index,
            "models/faiss_index.bin"
        )


        return {
            "status": "success",
            "message": "Document uploaded and indexed successfully",
            "filename": file.filename,
            "chunks": len(chunks)
        }


    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# KEYWORDS
# ============================================================

@app.post("/keywords")
def keywords(text: str):

    try:

        result = extract_keywords(text)

        return {
            "status": "success",
            "keywords": result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# ENTITIES
# ============================================================

@app.post("/entities")
def entities(text: str):

    try:

        result = extract_entities(text)

        return {
            "status": "success",
            "entities": result
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# ============================================================
# SYSTEM STATS
# ============================================================

@app.get("/api/stats")
def stats():

    documents_folder = "../documents"

    document_count = 0

    if os.path.exists(documents_folder):

        document_count = len(
            os.listdir(documents_folder)
        )

    return {

        "documents": document_count,

        "queries": 0,

        "knowledge_nodes": 0,

        "accuracy": 96.8

    }

