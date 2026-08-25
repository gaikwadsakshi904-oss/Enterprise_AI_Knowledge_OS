from llm import LLM

llm = LLM()

question = "What is RAG?"

context = """
RAG stands for Retrieval-Augmented Generation.
It retrieves relevant information from documents
and provides that information to an LLM to generate
a more accurate answer.
"""

response = llm.generate(question, context)

print("\nGemini RAG Response:")
print(response)