from rag_pipeline import RAGPipeline


rag = RAGPipeline()

question = "What is Deep Learning?"

 

response = rag.ask(question)


print("\nQUESTION:")
print(response["question"])


print("\nRETRIEVED DOCUMENTS:")

for doc in response["retrieved_documents"]:
    print(doc)
    print("----------------")


print("\nFINAL AI ANSWER:")
print(response["answer"])