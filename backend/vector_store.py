import os
import pickle
import faiss
import numpy as np


def create_index(embeddings):
    """
    Create a FAISS index from embeddings.
    """

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    if len(embeddings) == 0:
        raise ValueError("No embeddings available")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    return index


def save_index(index, file_path):
    """
    Save FAISS index to disk.
    """

    folder = os.path.dirname(file_path)

    if folder:
        os.makedirs(
            folder,
            exist_ok=True
        )

    faiss.write_index(
        index,
        file_path
    )

    print(
        f"FAISS index saved: {file_path}"
    )


def load_index(file_path):
    """
    Load FAISS index from disk.
    """

    if not os.path.exists(file_path):
        return None

    index = faiss.read_index(
        file_path
    )

    return index


def search_index(index, query_embedding, k=3):
    """
    Search similar documents.
    """

    query_embedding = np.asarray(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    return distances, indices


class VectorStore:

    def __init__(self, dimension=384):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(
            dimension
        )

    def add(self, embeddings):

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        self.index.add(
            embeddings
        )

    def search(
        self,
        query_embedding,
        k=3
    ):

        query_embedding = np.asarray(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        return distances, indices

    def save(
        self,
        file_path
    ):

        folder = os.path.dirname(
            file_path
        )

        if folder:
            os.makedirs(
                folder,
                exist_ok=True
            )

        faiss.write_index(
            self.index,
            file_path
        )

    def load(
        self,
        file_path,
        chunks_file=None
    ):

        if os.path.exists(file_path):

            self.index = faiss.read_index(
                file_path
            )

            print(
                "FAISS index loaded"
            )

        else:

            print(
                "FAISS index not found"
            )