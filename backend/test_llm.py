from llm import LLM


llm = LLM()


answer = llm.generate(
    "What is Deep Learning?",
    """
    Deep Learning is a subset of Machine Learning
    that uses artificial neural networks with multiple layers.
    It is used in image recognition, speech recognition,
    natural language processing and autonomous vehicles.
    """
)


print(answer)