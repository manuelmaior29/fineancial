from sklearn.feature_extraction.text import TfidfVectorizer

class CustomTfidfVectorizer(TfidfVectorizer):
    def __init__(self, min_word_freq=5, max_features=None, ngram_range=(1, 1), stop_words='english'):
        """
        Custom TF-IDF Vectorizer that filters words below a specified frequency.
        
        Args:
            min_word_freq (int): Minimum frequency for words to be considered in the vocabulary.
            max_features (int): Maximum number of features to keep (optional).
            ngram_range (tuple): The lower and upper boundary of the range of n-values for word or char n-grams.
            stop_words (str or list): Stop words to be removed. Defaults to 'english'.
        """
        super().__init__(max_features=max_features, ngram_range=ngram_range, stop_words=stop_words)
        self.min_word_freq = min_word_freq
        self.word_freq = {}
        self.vocab_ = None

    def fit(self, raw_documents):
        for doc in raw_documents:
            for word in doc.split():
                self.word_freq[word] = self.word_freq.get(word, 0) + 1
        self.vocab_ = {word: i for i, (word, freq) in enumerate(self.word_freq.items()) if freq >= self.min_word_freq}
        processed_docs = [
            " ".join([word if word in self.vocab_ else "UNK" for word in doc.split()])
            for doc in raw_documents
        ]
        super().fit(processed_docs)
        return self

    def transform(self, raw_documents):
        processed_docs = [
            " ".join([word if word in self.vocab_ else "UNK" for word in doc.split()])
            for doc in raw_documents
        ]
        return super().transform(processed_docs)
