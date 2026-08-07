from fastapi import FastAPI, UploadFile, File

from document_loader import *
from embedding import *
from vector_store import *

from rag_pipeline import answer_query

from summarizer import summarize
from keyword_extractor import extract_keywords
from entity_extractor import extract_entities



app=FastAPI(
    title="Enterprise AI Knowledge OS"
)



index=None

chunks=[]



@app.get("/")
def home():

    return {
        "message":
        "Enterprise AI Knowledge OS Running"
    }



@app.post("/upload")
async def upload(file:UploadFile=File(...)):


    path="../documents/"+file.filename


    with open(path,"wb") as f:

        f.write(
            await file.read()
        )


    docs=load_documents(
        "../documents"
    )


    global chunks,index


    chunks=split_documents(
        docs
    )


    embeddings=create_embeddings(
        chunks
    )


    index=create_index(
        embeddings
    )


    save_index(
        index,
        "models/faiss_index.bin"
    )


    return {
        "status":"Document indexed"
    }




@app.get("/ask")
def ask(question:str):


    response=answer_query(
        question,
        index,
        chunks
    )


    return {
        "answer":response
    }





@app.post("/summarize")
def summary(text:str):


    return {
        "summary":
        summarize(text)
    }





@app.post("/keywords")
def keywords(text:str):


    return {
        "keywords":
        extract_keywords(text)
    }





@app.post("/entities")
def entities(text:str):


    return {
        "entities":
        extract_entities(text)
    }