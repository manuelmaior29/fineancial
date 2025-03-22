import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import sys
sys.path.append("..")
from argparse import ArgumentParser
from feature_extraction import CustomTfidfVectorizer

def train_model(X, y, max_iter=1000, min_word_freq=2):
    feature_extractor = CustomTfidfVectorizer(min_word_freq=min_word_freq)
    feature_extractor.fit(X)
    X = feature_extractor.transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    model = LogisticRegression(max_iter=max_iter)
    model.fit(X_train, y_train)
    return feature_extractor, model

def main():
    parser = ArgumentParser()
    parser.add_argument("--train_data", type=str, required=True)
    parser.add_argument("--min_word_freq", type=int, required=False, default=2)
    parser.add_argument("--max_iter", type=int, required=False, default=1000)
    parser.add_argument("--output_model_path", type=str, required=True)
    args = parser.parse_args()
    data = pd.read_csv(args.train_data, sep=';')

    # To move in the parser that brings data to "standard format"
    data["cleaned_desc"] = data["cleaned_desc"].str.replace(".", " ")
    data["cleaned_desc"] = data["cleaned_desc"].str.replace(",", " ")
    data["cleaned_desc"] = data["cleaned_desc"].str.replace(":", " ")
    data["cleaned_desc"] = data["cleaned_desc"].str.replace(";", " ")
    data["cleaned_desc"] = data["cleaned_desc"].str.replace("/", " ")
    data["cleaned_desc"] = data["cleaned_desc"].str.replace("*", " ")
    data["cleaned_desc"] = data["cleaned_desc"].str.replace("-", " ")
    data["cleaned_desc"] = data["cleaned_desc"].str.replace(r"\s+", " ", regex=True)
    data["cleaned_desc"] = data["cleaned_desc"].str.replace(r"(\d+)", "", regex=True)
    data["cleaned_desc"] = data["cleaned_desc"].str.lower()
    data["cleaned_desc"] = data["cleaned_desc"].str.replace("pos", "")
    data["cleaned_desc"] = data["cleaned_desc"].fillna("")

    X = data["cleaned_desc"]
    y = data["category"]
    feature_extractor, model = train_model(X, y, max_iter=args.max_iter, min_word_freq=args.min_word_freq)

    with open(args.output_model_path + ".model", "wb") as f:
        pickle.dump(model, f)

    with open(args.output_model_path + ".vectorizer", "wb") as f:
        pickle.dump(feature_extractor, f)

if __name__ == "__main__":
    main()