from abc import ABC, abstractmethod
import locale
import random
from preprocessing.standard import StandardTransaction
import pandas as pd
import re

from transaction_classification.consts import TransactionCategory

locale.setlocale(locale.LC_NUMERIC, 'en_US.UTF-8')
                 
class BaseParser(ABC):
    """Abstract base class for bank statement parsers."""

    @abstractmethod
    def parse(self, document_path: str):
        """Parse the document and return a list of StandardTransaction objects."""
        raise NotImplementedError()

class BTParser(BaseParser):
    def parse(self, file, substrings_to_remove=[], sep=','):
        # df_metadata = pd.read_csv(file, skiprows=9, nrows=4, sep=sep)
        # df_metadata.columns = [0, 1]
        file.seek(0)
        df = pd.read_csv(file, skiprows=14, sep=sep, encoding="ISO-8859-1")
        transactions = []
        currency = "RON" # self.get_currency(df_metadata)
        for _, row in df.iterrows():
            if not "Round Up" in row["Description"]:
                transaction = StandardTransaction(
                    transaction_type=self.get_transaction_type(row),
                    category=self.get_category(row),
                    label="",
                    date=self.get_date(row),
                    cleaned_desc=self.clean_description(row["Description"], substrings_to_remove),
                    notes="",
                    amount=self.get_amount(row),
                    currency=currency
                )
                transactions.append(transaction)
        return transactions

    def get_currency(self, df: pd.DataFrame):
        df.iloc[1, 1].split(" ")[-1]

    def get_date(self, row):
        date = re.search(r"(\d{2}/\d{2}/\d{4})", row["Description"])
        return date[0] if date else row["Processing date"]
    
    def get_transaction_type(self, row):
        return "Income" if pd.notna(row["Credit"]) else ("Expense" if pd.notna(row["Debit"]) else "Unknown")
    
    def get_category(self, row):
        # TODO: Return category based on cleaned description / transaction data
        return random.choice(list(TransactionCategory)).value

    def get_amount(self, row):
        amount_str = row["Debit"] if pd.notna(row["Debit"]) else row["Credit"]
        amount = pd.to_numeric(amount_str.replace(",", ""), downcast="float")
        return float(amount)

    def clean_description(self, desc: str, substrings_to_remove: str) -> str:
        clean_desc = desc.split(";")[1]
        if substrings_to_remove:
            for substring in substrings_to_remove:
                clean_desc = re.sub(substring, "", clean_desc)
        clean_desc = re.sub(r"TID:\w+", "", clean_desc)
        clean_desc = re.sub(r"comision tranzactie \d+\.\d+ RON", "", clean_desc)
        clean_desc = re.sub(r"valoare tranzactie: \d+\.\d+ RON", "", clean_desc)
        clean_desc = re.sub(r"RRN:\w+", "", clean_desc)
        clean_desc = re.sub(r"RRN: \w+", "", clean_desc)
        clean_desc = re.sub(r"\d{2}/\d{2}/\d{4} \w+", "", clean_desc)
        clean_desc = re.sub(r"\s+", " ", clean_desc)
        clean_desc = clean_desc.strip()
        clean_desc = re.sub("(\d+)", "", clean_desc)
        clean_desc = clean_desc.lower()
        clean_desc = re.sub("pos", "", clean_desc)
        clean_desc = re.sub(r'\W+', ' ', clean_desc)
        clean_desc = re.sub(r'\b\w{1,2}\b', '', clean_desc)
        clean_desc = re.sub(r'^\s+|\s+$', '', clean_desc)
        clean_desc = " ".join(list(dict.fromkeys(clean_desc.split(" ")))) if isinstance(clean_desc, str) else clean_desc
        clean_desc = re.sub(r"\s+", " ", clean_desc)
        return clean_desc
