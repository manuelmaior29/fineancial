import json
import os
import re

from transaction_classification.consts import TransactionCategory

class RulesNotFoundError(Exception):
    """Exception raised when the rules file is not found. """

class RuleBasedTransactionClassifier:
    def __init__(self, rules = None):
        if not rules:
            try:
                self.rules = json.loads(os.environ["TRANSACTION_CLASSIFICATION_RULES"])
            except KeyError as e:
                raise RulesNotFoundError(f"Rules not found in environment variable: {e}")

            try:
                with open(os.environ["TRANSACTION_CLASSIFICATION_RULES_PATH"], "r") as f:
                    self.rules = json.load(f)
            except FileNotFoundError as e:
                raise RulesNotFoundError(f"Rules file not found: {e}")
        else:
            self.rules = rules

    def predict(self, description: str) -> TransactionCategory:
        """Assigns a category based on keyword matching."""
        cleaned_desc = description.lower().strip()
        for category, keywords in self.rules.items():
            if any(re.search(rf"\b{kw}\b", cleaned_desc) for kw in keywords):
                print(category)
                cat = list(filter(lambda x: x.value == category, list(TransactionCategory)))[0]
                return cat
        return TransactionCategory.OTHER