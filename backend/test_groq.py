import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")

print("GROQ KEY:", "FOUND" if key else "MISSING")

if not key:
    raise SystemExit("ERROR: GROQ_API_KEY missing")

client = Groq(api_key=key)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: GROQ WORKING"
        }
    ],
    temperature=0,
    max_tokens=20
)

print("MODEL:", response.model)
print("RESPONSE:", response.choices[0].message.content)


