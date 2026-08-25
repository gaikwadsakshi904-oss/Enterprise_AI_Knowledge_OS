import os


class DocumentClassifier:

    def classify(self, filename):

        filename = filename.lower()

        if "policy" in filename:
            return "Policy"

        elif "employee" in filename:
            return "Employee"

        elif "customer" in filename:
            return "Customer"

        elif "manual" in filename:
            return "Manual"

        elif "faq" in filename:
            return "FAQ"

        elif filename.endswith(".csv"):
            return "Dataset"

        else:
            return "Other"