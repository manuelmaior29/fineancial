import re

class RuleBasedClassifier:
    def __init__(self, rules):
        self.rules = rules

    def classify(self, description):
        """Assigns a category based on keyword matching."""
        cleaned_desc = description.lower().strip()
        for category, keywords in self.rules.items():
            if any(re.search(rf"\b{kw}\b", cleaned_desc) for kw in keywords):
                return category
        return "Other"