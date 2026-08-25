import re
import numpy as np
from rank_bm25 import BM25Okapi


class HybridSearch:

    def __init__(
        self,
        chunks,
        embedding_service,
        vector_store
    ):

        self.chunks = chunks
        self.embedding_service = embedding_service
        self.vector_store = vector_store

        self.documents = [
            self._get_text(chunk)
            for chunk in chunks
        ]

        self.tokenized_documents = [
            self._tokenize(text)
            for text in self.documents
        ]

        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )

    def _get_text(self, chunk):

        if isinstance(chunk, dict):

            return chunk.get(
                "text",
                ""
            )

        return getattr(
            chunk,
            "text",
            ""
        )

    def _tokenize(self, text):

        return re.findall(
            r"\b[a-zA-Z0-9_-]+\b",
            text.lower()
        )

    def semantic_search(
        self,
        query,
        top_k=10
    ):

        query_embedding = (
            self.embedding_service.encode(
                [query]
            )
        )

        # Use your existing VectorStore
        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        output = []

        for result in results:

            if isinstance(result, dict):

                index = result.get(
                    "index",
                    result.get(
                        "chunk_index",
                        -1
                    )
                )

                score = result.get(
                    "score",
                    result.get(
                        "similarity",
                        0.0
                    )
                )

            else:

                index = getattr(
                    result,
                    "index",
                    -1
                )

                score = getattr(
                    result,
                    "score",
                    0.0
                )

            if (
                index is not None
                and 0 <= index < len(self.chunks)
            ):

                output.append({
                    "index": int(index),
                    "semantic_score": float(score),
                    "keyword_score": 0.0
                })

        return output

    def keyword_search(
        self,
        query,
        top_k=10
    ):

        query_tokens = self._tokenize(
            query
        )

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked_indices = np.argsort(
            scores
        )[::-1][:top_k]

        results = []

        for index in ranked_indices:

            score = float(
                scores[index]
            )

            if score <= 0:
                continue

            results.append({
                "index": int(index),
                "semantic_score": 0.0,
                "keyword_score": score
            })

        return results

    def search(
        self,
        query,
        top_k=5,
        semantic_weight=0.7,
        keyword_weight=0.3
    ):

        semantic_results = (
            self.semantic_search(
                query,
                top_k=top_k * 2
            )
        )

        keyword_results = (
            self.keyword_search(
                query,
                top_k=top_k * 2
            )
        )

        combined = {}

        for result in semantic_results:

            index = result["index"]

            combined[index] = {
                "index": index,
                "semantic_score": result[
                    "semantic_score"
                ],
                "keyword_score": 0.0
            }

        for result in keyword_results:

            index = result["index"]

            if index not in combined:

                combined[index] = {
                    "index": index,
                    "semantic_score": 0.0,
                    "keyword_score": result[
                        "keyword_score"
                    ]
                }

            else:

                combined[index][
                    "keyword_score"
                ] = result[
                    "keyword_score"
                ]

        if not combined:
            return []

        semantic_scores = [
            item["semantic_score"]
            for item in combined.values()
        ]

        keyword_scores = [
            item["keyword_score"]
            for item in combined.values()
        ]

        max_semantic = max(
            semantic_scores,
            default=1.0
        )

        max_keyword = max(
            keyword_scores,
            default=1.0
        )

        if max_semantic == 0:
            max_semantic = 1.0

        if max_keyword == 0:
            max_keyword = 1.0

        for item in combined.values():

            semantic_normalized = (
                item["semantic_score"]
                / max_semantic
            )

            keyword_normalized = (
                item["keyword_score"]
                / max_keyword
            )

            item["hybrid_score"] = (
                semantic_weight
                * semantic_normalized
                +
                keyword_weight
                * keyword_normalized
            )

        ranked = sorted(
            combined.values(),
            key=lambda item:
                item["hybrid_score"],
            reverse=True
        )

        final_results = []

        for result in ranked[:top_k]:

            index = result["index"]

            final_results.append({
                "chunk": self.chunks[index],
                "index": index,
                "semantic_score": result[
                    "semantic_score"
                ],
                "keyword_score": result[
                    "keyword_score"
                ],
                "hybrid_score": result[
                    "hybrid_score"
                ]
            })

        return final_results
