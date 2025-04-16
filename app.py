import sys
from datetime import datetime

import streamlit as st
import pandas as pd
import json

import ui.charts

sys.path.append("src")
from processing.parser import BTParser
from ui.static_content import HELP_UPLOAD_FILE
from transaction_classification.adapter import TransactionClassificationAdapter
from transaction_classification.models.rulebased.rulebased import RuleBasedTransactionClassifier
import processing.filters as filters

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
    st.set_page_config(page_title="fineancial", 
                       page_icon=":moneybag:",
                       layout="wide")
    st.title("fineancial")

    # AI-driven modules
    # TODO: Prepare code for hotswapping
    transaction_classification_model_rule_based = RuleBasedTransactionClassifier(rules=None)
    transaction_classification_adapter = TransactionClassificationAdapter(model=transaction_classification_model_rule_based, preprocess_fn=lambda x: x.cleaned_desc, postprocess_fn=lambda x: x)

    # Upload CSV file with raw transactions data
    csv_file = st.file_uploader("Upload your bank transactions file (CSV)", 
                                type=["csv"],
                                help=HELP_UPLOAD_FILE)
    if csv_file is not None:
        transactions = []
        parser = BTParser() # TODO: Add other parsers
        transactions = parser.parse(csv_file, substrings_to_remove=[], sep=",")

        transaction_categories = [transaction_classification_adapter.predict(transaction) for transaction in transactions]
        df_transactions = pd.DataFrame([transaction.__dict__ for transaction in transactions])
        df_transactions["category"] = [category.value for category in transaction_categories] 

        column_data, column_graphs = st.columns([2, 1])

        # Data editor section
        with column_data:

            # Make aggrid table fit width based on content
            grid_response = st.data_editor(
                df_transactions,
                use_container_width=True,
                height=500,
                key="transactions_table"
            )
            df_transactions = pd.DataFrame(grid_response)
        
        # Graph section
        with column_graphs:
            select_interval = st.selectbox("Select time interval", ["Daily", "Weekly", "Monthly", "Yearly"])
            col_prev, col_next = st.columns(2)
            with col_prev:
                prev_interval = st.button("Previous", use_container_width=True)
            with col_next:
                next_interval = st.button("Next", use_container_width=True)

            tab_category_overview, tab_trends = st.tabs(["Category overview", "Trends"])

            with tab_category_overview:
                # TODO: Replace code with module that calculates transaction amount sums by category
                df_transactions_expenses = df_transactions[df_transactions["transaction_type"] == "Expense"] \
                    .groupby(["category"]) \
                    .agg({"amount": "sum"}) \
                    .reset_index()
                ui.charts.show_bar_chart(df_transactions_expenses, "category", "amount", "Transaction Amount Sums by Category (Expenses)", "Category", "Amount")

                df_transactions_incomes = df_transactions[df_transactions["transaction_type"] == "Income"] \
                    .groupby(["category"]) \
                    .agg({"amount": "sum"}) \
                    .reset_index()
                ui.charts.show_bar_chart(df_transactions_incomes, "category", "amount", "Transaction Amount Sums by Category (Incomes)", "Category", "Amount")

            with tab_trends:
                # TODO: Replace code with module that calculates running balance
                df_transactions = filters.filter_by_date_period(df_transactions, 
                                                                df_transactions["date"].max().replace(day=1).to_pydatetime(), 
                                                                datetime.now())
                
                
                df_transactions["signed_amount"] = df_transactions.apply(
                    lambda row: row["amount"] if row["transaction_type"] == "Income" else -row["amount"],
                    axis=1
                )
                df_transactions["running_balance"] = df_transactions["signed_amount"].cumsum()
                ui.charts.show_trends_chart(df_transactions, "date", "running_balance", "white", "Running Balance", "Date", "Amount")

    # st.header("Upload JSON Rules")
    # json_file = st.file_uploader("Upload your rules file (json)", type=["json"])
    # if json_file is not None:
    #     rules = load_json(json_file)
    #     if rules is not None:
    #         st.write("**Loaded Rules:**")
    #         st.json(rules)

if __name__ == "__main__":
    main()
