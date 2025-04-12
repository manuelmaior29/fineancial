import json
import os
import re

from transaction_classification.consts import TransactionCategory

class RulesNotFoundError(Exception):
    """Exception raised when the rules file is not found. """

class RuleBasedTransactionClassifier:
    def __init__(self, rules = None):
        if not rules:
            if "TRANSACTION_CLASSIFICATION_RULES" in os.environ:
                self.rules = json.loads(os.environ["TRANSACTION_CLASSIFICATION_RULES"])
            elif "TRANSACTION_CLASSIFICATION_RULES_PATH" in os.environ:
                with open(os.environ["TRANSACTION_CLASSIFICATION_RULES_PATH"], "r") as f:
                    self.rules = json.load(f)
            else:
                raise RulesNotFoundError("Rules not found in environment variable or file")
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