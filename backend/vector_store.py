import json
from typing import List, Dict

import faiss
import numpy as np

from config import (
    FAISS_INDEX_PATH,
    CHUNKS_PATH,
    METADATA_PATH,
    EMBEDDING_DIMENSION,
)


class VectorStore:

    def __init__(self):

        self.index = None
        self.chunks = []
        self.metadata = []

        self.load()


    # =====================================================
    # BUILD INDEX
    # =====================================================

    def build(
        self,
        embeddings: np.ndarray,
        chunks: List[Dict],
    ):

        if len(chunks) == 0:

            raise ValueError(
                "Cannot build FAISS index without chunks."
            )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        if embeddings.ndim != 2:

            raise ValueError(
                "Embeddings must be a 2-dimensional array."
            )

        if embeddings.shape[0] != len(chunks):

            raise ValueError(
                "Number of embeddings does not match "
                "number of chunks."
            )

        if embeddings.shape[1] != EMBEDDING_DIMENSION:

            raise ValueError(
                f"Expected embedding dimension "
                f"{EMBEDDING_DIMENSION}, "
                f"got {embeddings.shape[1]}"
            )

        faiss.normalize_L2(
            embeddings
        )

        self.index = faiss.IndexFlatIP(
            EMBEDDING_DIMENSION
        )

        self.index.add(
            embeddings
        )

        self.chunks = chunks

        self.metadata = []

        for chunk in chunks:

            self.metadata.append({

                "chunk_id": chunk["chunk_id"],

                "document": chunk["document"],

                "page": chunk.get("page"),

                "source": chunk.get("source"),

            })

        self.save()


    # =====================================================
    # ADD DOCUMENT CHUNKS
    # =====================================================

    def add(
        self,
        embeddings: np.ndarray,
        chunks: List[Dict],
    ):

        if len(chunks) == 0:

            raise ValueError(
                "Cannot add empty chunks."
            )

        embeddings = np.asarray(
            embeddings,
            dtype="float32",
        )

        if embeddings.ndim != 2:

            raise ValueError(
                "Embeddings must be a 2-dimensional array."
            )

        if embeddings.shape[0] != len(chunks):

            raise ValueError(
                "Number of embeddings does not match "
                "number of chunks."
            )

        if embeddings.shape[1] != EMBEDDING_DIMENSION:

            raise ValueError(
                f"Expected embedding dimension "
                f"{EMBEDDING_DIMENSION}, "
                f"got {embeddings.shape[1]}"
            )

        faiss.normalize_L2(
            embeddings
        )

        if self.index is None:

            self.index = faiss.IndexFlatIP(
                EMBEDDING_DIMENSION
            )

        self.index.add(
            embeddings
        )

        self.chunks.extend(
            chunks
        )

        for chunk in chunks:

            self.metadata.append({

                "chunk_id": chunk["chunk_id"],

                "document": chunk["document"],

                "page": chunk.get("page"),

                "source": chunk.get("source"),

            })

        self.save()

        print(
            f"Added {len(chunks)} chunks."
        )

        print(
            f"Total vectors: {self.index.ntotal}"
        )


    # =====================================================
    # SEARCH
    # =====================================================

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
    ) -> List[Dict]:

        if self.index is None:

            return []

        if self.index.ntotal == 0:

            return []

        query_embedding = np.asarray(
            query_embedding,
            dtype="float32",
        )

        if query_embedding.ndim == 1:

            query_embedding = query_embedding.reshape(
                1,
                -1
            )

        if query_embedding.shape[1] != EMBEDDING_DIMENSION:

            raise ValueError(
                f"Expected query embedding dimension "
                f"{EMBEDDING_DIMENSION}, "
                f"got {query_embedding.shape[1]}"
            )

        faiss.normalize_L2(
            query_embedding
        )

        actual_k = min(
            top_k,
            self.index.ntotal,
        )

        scores, indices = self.index.search(
            query_embedding,
            actual_k,
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index < 0:

                continue

            chunk = self.chunks[index]

            metadata = self.metadata[index]

            results.append({

                "chunk_id": metadata["chunk_id"],

                "text": chunk["text"],

                "document": metadata["document"],

                "page": metadata["page"],

                "source": metadata["source"],

                "score": round(
                    float(score),
                    4,
                ),

            })

        return results


    # =====================================================
    # SAVE
    # =====================================================

    def save(self):

        if self.index is None:

            return

        faiss.write_index(
            self.index,
            str(FAISS_INDEX_PATH),
        )

        with open(
            CHUNKS_PATH,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.chunks,
                file,
                indent=2,
                ensure_ascii=False,
            )

        with open(
            METADATA_PATH,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.metadata,
                file,
                indent=2,
                ensure_ascii=False,
            )


    # =====================================================
    # LOAD
    # =====================================================

    def load(self):

        if not (
            FAISS_INDEX_PATH.exists()
            and CHUNKS_PATH.exists()
            and METADATA_PATH.exists()
        ):

            print(
                "No existing FAISS index found."
            )

            return

        try:

            self.index = faiss.read_index(
                str(FAISS_INDEX_PATH)
            )

            with open(
                CHUNKS_PATH,
                "r",
                encoding="utf-8",
            ) as file:

                self.chunks = json.load(
                    file
                )

            with open(
                METADATA_PATH,
                "r",
                encoding="utf-8",
            ) as file:

                self.metadata = json.load(
                    file
                )

            print(
                f"FAISS index loaded: "
                f"{self.index.ntotal} vectors"
            )

        except Exception as error:

            print(
                f"Failed to load vector store: {error}"
            )

            self.index = None

            self.chunks = []

            self.metadata = []


    # =====================================================
    # COUNT
    # =====================================================

    def count(self) -> int:

        if self.index is None:

            return 0

        return self.index.ntotal


    # =====================================================
    # CLEAR
    # =====================================================

    def clear(self):

        self.index = None

        self.chunks = []

        self.metadata = []

        for path in [
            FAISS_INDEX_PATH,
            CHUNKS_PATH,
            METADATA_PATH,
        ]:

            if path.exists():

                path.unlink()
