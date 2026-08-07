from config import FAISS_INDEX, CHUNKS_FILE
from embedding import EmbeddingModel
from vector_store import VectorStore
from llm import LLM


class RAGPipeline:

    def __init__(self):

        print("Initializing RAG Pipeline...")


        # Load embedding model
        self.embedding_model = EmbeddingModel()


        # Load FAISS vector store
        self.vector_store = VectorStore(384)

        self.vector_store.load(
            FAISS_INDEX,
            CHUNKS_FILE
        )


        # Load LLM model
        self.llm = LLM()


        print("RAG Pipeline Ready")



    def retrieve(self, question, k=3):

        # Convert question into embedding
        query_embedding = self.embedding_model.encode(
            [question]
        )[0]


        # Search similar documents
        results = self.vector_store.search(
            query_embedding,
            k
        )


        return results



    def build_context(self, documents):

        context = ""


        for i, doc in enumerate(documents, start=1):

            context += f"Document {i}\n"

            context += doc

            context += "\n\n"


        return context



    def ask(self, question):

        # Step 1: Retrieve documents
        documents = self.retrieve(
            question
        )


        # Step 2: Create context
        context = self.build_context(
            documents
        )


        # Step 3: Generate answer using LLM
        answer = self.llm.generate(
            question,
            context
        )


        return {

            "question": question,

            "retrieved_documents": documents,

            "context": context,

            "answer": answer

        }