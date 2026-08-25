import numpy as np


class Reranker:

    def __init__(self, embedding_service):

        self.embedding_service = embedding_service

    def _get_text(self, chunk):

        if isinstance(chunk, dict):
            return chunk.get("text", "")

        return getattr(
            chunk,
            "text",
            ""
        )

    def rerank(
        self,
        query,
        results,
        top_k=5
    ):

        if not results:
            return []

        documents = [
            self._get_text(result["chunk"])
            for result in results
        ]

        query_embedding = (
            self.embedding_service.encode(
                [query]
            )
        )[0]

        document_embeddings = (
            self.embedding_service.encode(
                documents
            )
        )

        # Because embeddings are normalized,
        # dot product = cosine similarity.
        scores = np.dot(
            document_embeddings,
            query_embedding
        )

        reranked = []

        for result, score in zip(
            results,
            scores
        ):

            updated = dict(result)

            updated["reranker_score"] = float(
                score
            )

            reranked.append(updated)

        reranked.sort(
            key=lambda x:
                x["reranker_score"],
            reverse=True
        )

        return reranked[:top_k]
