import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

class LLMService:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

        if not self.api_key:
            raise RuntimeError("GROQ_API_KEY is missing from .env")

        self.client = Groq(api_key=self.api_key)
        self.model = "openai/gpt-oss-20b"

    def generate(self, question, context):

        prompt = f"""You are an enterprise AI knowledge assistant.

Answer the user's question using ONLY the provided enterprise evidence.

Rules:
- Give a clear direct answer.
- Do not invent company policies.
- If the evidence does not contain the answer, say that clearly.
- Mention relevant document names when useful.
- Keep the answer professional and concise.

USER QUESTION:
{question}

ENTERPRISE EVIDENCE:
{context}

Answer:
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a reliable enterprise knowledge assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.2,
                max_tokens=1200
            )

            return response.choices[0].message.content

        except Exception as error:
            print("GROQ ERROR:", error)

            return (
                "The AI generation service is temporarily unavailable. "
                "However, relevant evidence was successfully retrieved "
                "from the enterprise knowledge base."
            )



