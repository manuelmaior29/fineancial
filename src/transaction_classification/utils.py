from sklearn.preprocessing import LabelEncoder
from transaction_classification.consts import TransactionCategory

class TransactionCategoryEncoder(LabelEncoder):
    def __init__(self, categories=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categories = [cat.value for cat in list(TransactionCategory)] if not categories else categories
        self.fit(self.categories)

    def transform(self, y):
        return super().transform(y)