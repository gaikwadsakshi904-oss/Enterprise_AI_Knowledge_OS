from document_classifier import DocumentClassifier

classifier = DocumentClassifier()

files = [
    "policy.pdf",
    "employee.pdf",
    "customer.txt",
    "manual.pdf",
    "faq.pdf",
    "sales.csv",
    "notes.docx"
]

for file in files:
    print(file, "->", classifier.classify(file))