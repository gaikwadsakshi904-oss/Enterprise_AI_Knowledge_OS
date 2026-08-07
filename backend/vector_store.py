import faiss
import pickle
import numpy as np


class VectorStore:


    def __init__(self, dimension):

        self.dimension = dimension

        self.index = None

        self.chunks = []



    def create(self, embeddings, documents):

        # Convert embeddings into numpy array

        embeddings = np.array(
            embeddings
        ).astype("float32")


        # Create FAISS index

        self.index = faiss.IndexFlatL2(
            self.dimension
        )


        # Add vectors

        self.index.add(
            embeddings
        )


        # Store documents

        self.chunks = documents



    def save(self, index_path, chunks_path):

        # Save FAISS index

        faiss.write_index(
            self.index,
            index_path
        )


        # Save documents

        with open(
            chunks_path,
            "wb"
        ) as f:

            pickle.dump(
                self.chunks,
                f
            )


        print("Vector store saved")



    def load(self, index_path, chunks_path):

        # Load FAISS index

        self.index = faiss.read_index(
            index_path
        )


        # Load documents

        with open(
            chunks_path,
            "rb"
        ) as f:

            self.chunks = pickle.load(f)



    def search(self, query_embedding, k=3):

        query_embedding = np.array(
            [query_embedding]
        ).astype("float32")


        distances, indices = self.index.search(
            query_embedding,
            k
        )


        results = []


        for idx in indices[0]:

            results.append(
                self.chunks[idx]
            )


        return results