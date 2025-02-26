from abc import ABC, abstractmethod
from src.standard import StandardTransaction
import pandas as pd
import re

class BaseParser(ABC):
    """Abstract base class for bank statement parsers."""

    @abstractmethod
    def parse(self, document_path: str):
        """Parse the document and return a list of StandardTransaction objects."""
        pass

class BTParser(BaseParser):
    def parse(self, file):
        df_metadata = pd.read_csv(file, skiprows=9, nrows=4)
        df_metadata.columns = [0, 1]
        df = pd.read_csv(file, skiprows=14)
        transactions = []
        currency = self.get_currency(df_metadata)
        for _, row in df.iterrows():
            if not "Round Up" in row["Description"]:
                transaction = StandardTransaction(
                    transaction_type=self.get_transaction_type(row),
                    category=self.get_category(row),
                    label="",
                    date=self.get_date(row),
                    cleaned_desc=self.clean_description(row["Description"]),
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
        return ""

    def get_amount(self, row):
        return row["Debit"] if pd.notna(row["Debit"]) else row["Credit"]

    def clean_description(self, desc):
        clean_desc = desc.split(";")[1]
        clean_desc = re.sub(r"TID:\w+", "", clean_desc)
        clean_desc = re.sub(r"comision tranzactie \d+\.\d+ RON", "", clean_desc)
        clean_desc = re.sub(r"valoare tranzactie: \d+\.\d+ RON", "", clean_desc)
        clean_desc = re.sub(r"RRN:\w+", "", clean_desc)
        clean_desc = re.sub(r"\d{2}/\d{2}/\d{4} \w+", "", clean_desc)
        clean_desc = re.sub(r"\s+", " ", clean_desc)
        clean_desc = clean_desc.strip()
        clean_desc = re.sub(r"RRN: \w+", "", clean_desc)
        return clean_desc
