import random
import sys

sys.path.append("src")

from utils import string_to_rgb
from transaction_classification.adapter import TransactionClassificationAdapter
from transaction_classification.models.rulebased.rulebased import RuleBasedTransactionClassifier

import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder
from preprocessing.parser import BTParser
import plotly.graph_objects as go


def load_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        return None

def load_json(file):
    try:
        return json.load(file)
    except json.JSONDecodeError as e:
        st.error(f"Error reading JSON file: {e}")
        return None

def main():
    st.title("fineancial")

    # AI-driven modules
    # TODO: Prepare code for hotswapping
    transaction_classification_model_rule_based = RuleBasedTransactionClassifier(rules=None)
    transaction_classification_adapter = TransactionClassificationAdapter(model=transaction_classification_model_rule_based, preprocess_fn=lambda x: x.cleaned_desc, postprocess_fn=lambda x: x)

    # Upload CSV file with raw transactions data
    csv_file = st.file_uploader("Upload your bank transactions file (CSV)", type=["csv"])
    if csv_file is not None:
        transactions = []
        parser = BTParser() # TODO: Add other parsers
        transactions = parser.parse(csv_file, substrings_to_remove=[], sep=",")

        transaction_categories = [transaction_classification_adapter.predict(transaction) for transaction in transactions]
        df_transactions = pd.DataFrame([transaction.__dict__ for transaction in transactions])
        df_transactions["category"] = [category.value for category in transaction_categories] 

        gb = GridOptionsBuilder.from_dataframe(df_transactions)
        gb.configure_default_column(editable=True)
        grid_options = gb.build()

        grid_response = AgGrid(df_transactions, gridOptions=grid_options, editable=True, height=400)

        df_transactions = pd.DataFrame(grid_response["data"])

        df_transactions_expenses = df_transactions[df_transactions["transaction_type"] == "Expense"] \
            .groupby(["category"]) \
            .agg({"amount": "sum"})\
            .reset_index()
        fig = go.Figure(data=[go.Bar(x=df_transactions_expenses["category"], 
                                     y=df_transactions_expenses["amount"], 
                                     marker_color=[string_to_rgb(category) for category in df_transactions_expenses["category"]])])
        fig.update_layout(title="Transaction Amount Sums by Category (Expenses)", xaxis_title="Category", yaxis_title="Amount")
        st.plotly_chart(fig)

        df_transactions_incomes = df_transactions[df_transactions["transaction_type"] == "Income"].groupby(["category"]).agg({"amount": "sum"}).reset_index()
        fig = go.Figure(data=[go.Bar(x=df_transactions_incomes["category"], 
                                     y=df_transactions_incomes["amount"],
                                     marker_color=[string_to_rgb(category) for category in df_transactions_incomes["category"]])])
        fig.update_layout(title="Transaction Amount Sums by Category (Incomes)", xaxis_title="Category", yaxis_title="Amount")
        st.plotly_chart(fig)

    # st.header("Upload JSON Rules")
    # json_file = st.file_uploader("Upload your rules file (json)", type=["json"])
    # if json_file is not None:
    #     rules = load_json(json_file)
    #     if rules is not None:
    #         st.write("**Loaded Rules:**")
    #         st.json(rules)

if __name__ == "__main__":
    main()
