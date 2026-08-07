from transformers import pipeline


class LLM:

    def __init__(self):

        print("Loading LLM...")

        self.model = pipeline(
            "text2text-generation",
            model="google/flan-t5-small"
        )

        print("LLM Ready")


    def generate(self, question, context):

        prompt = f"""
Context:
{context}

Question:
{question}

Answer:
"""


        response = self.model(
            prompt,
            max_length=150,
            do_sample=False
        )


        answer = response[0]["generated_text"]


        # Remove bad short answers
        bad_answers = [
            "Machine Learning",
            "Document 1",
            "Document 2",
            "Document 3",
            "a subset of Machine Learning"
        ]


        if answer.strip() in bad_answers or len(answer.split()) < 5:

            # Take first real document text
            answer = context.replace(
                "Document 1\n",
                ""
            ).split("\n\n")[0]


        return answer