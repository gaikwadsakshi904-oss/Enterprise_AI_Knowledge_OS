from google import genai

from config import GEMINI_API_KEY, GEMINI_MODEL


def main():

    print("=" * 60)
    print("GEMINI CONNECTION TEST")
    print("=" * 60)

    print(
        f"Model: {GEMINI_MODEL}"
    )

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents="Explain artificial intelligence in one sentence.",
    )

    print("\nResponse:")
    print(response.text)

    print("\nGemini connection successful.")


if __name__ == "__main__":
    main()