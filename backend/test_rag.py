from rag_pipeline import RAGPipeline


def main():

    print("=" * 60)
    print("ENTERPRISE AI KNOWLEDGE OS")
    print("RAG TEST")
    print("=" * 60)

    pipeline = RAGPipeline()

    while True:

        question = input(
            "\nAsk a question "
            "(type 'exit' to quit): "
        ).strip()

        if question.lower() == "exit":

            break

        if not question:

            continue

        result = pipeline.ask(
            question
        )

        print(
            "\n" + "=" * 60
        )

        print("ANSWER")

        print("=" * 60)

        print(
            result["answer"]
        )

        print(
            "\n" + "=" * 60
        )

        print("SOURCES")

        print("=" * 60)

        for source in result[
            "sources"
        ]:

            page = source["page"]

            if page:

                location = (
                    f"{source['document']} "
                    f"(page {page})"
                )

            else:

                location = source[
                    "document"
                ]

            print(
                f"- {location} "
                f"| score={source['score']}"
            )


if __name__ == "__main__":

    main()