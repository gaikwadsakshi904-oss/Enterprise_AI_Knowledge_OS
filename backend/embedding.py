from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL


class EmbeddingService:

    def __init__(self):

        print(
            f"Loading embedding model: "
            f"{EMBEDDING_MODEL}"
        )

        self.model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        print("Embedding model loaded.")

    def encode(
        self,
        texts: List[str],
    ) -> np.ndarray:

        if not texts:
            return np.empty(
                (0, 384),
                dtype="float32"
            )

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return embeddings.astype(
            "float32"
        )