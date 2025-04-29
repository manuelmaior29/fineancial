from abc import ABC, abstractmethod

from transaction_classification.consts import TransactionCategory
from processing.standard import StandardTransaction

class TransactionPredictable(ABC):
    @abstractmethod
    def predict(self, transaction: StandardTransaction) -> TransactionCategory:
        raise NotImplementedError()

class TransactionClassificationAdapter:
    def __init__(self, model: TransactionPredictable, preprocess_fn, postprocess_fn):
        self.model = model
        self.preprocess_fn = preprocess_fn
        self.postprocess_fn = postprocess_fn

    def predict(self, transaction: StandardTransaction) -> TransactionCategory:
        print(str(transaction))
        model_input = self.preprocess_fn(transaction)
        prediction = self.model.predict(model_input)
        return self.postprocess_fn(prediction)