import sys

import streamlit as st
import pandas as pd
import json

sys.path.append("src")
from processing.parser import BTParser
from transaction_classification.adapter import TransactionClassificationAdapter
from transaction_classification.models.rulebased.rulebased import RuleBasedTransactionClassifier
import processing.filters as filters
import ui.charts
import ui.state
import ui.callbacks
import ui.utils
from ui.static_content import HELP_UPLOAD_FILE

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
    ui.state.init()
    st.set_page_config(page_title="fineancial", 
                       page_icon=":moneybag:",
                       layout="wide")
    st.title("fineancial")

    # AI-driven modules
    # TODO: Prepare code for hotswapping
    transaction_classification_model_rule_based = RuleBasedTransactionClassifier(rules=None)
    transaction_classification_adapter = TransactionClassificationAdapter(model=transaction_classification_model_rule_based, preprocess_fn=lambda x: x.cleaned_desc, postprocess_fn=lambda x: x)

    # Upload CSV file with raw transactions data
    csv_files = st.file_uploader("Upload your bank transactions file (CSV)", 
                                type=["csv"],
                                help=HELP_UPLOAD_FILE,
                                accept_multiple_files=True)
    
    if len(csv_files) > 0:
        parser = BTParser() # TODO: Add other parsers

        transactions = []
        for csv_file in csv_files:
            transactions += parser.parse(csv_file, substrings_to_remove=[], sep=",")

        transaction_categories = [transaction_classification_adapter.predict(transaction) for transaction in transactions]
        df_transactions = pd.DataFrame([transaction.__dict__ for transaction in transactions])
        df_transactions["category"] = [category.value for category in transaction_categories] 

        # Date interval navigation
        _ = st.selectbox("Select time interval", ["Weekly", "Monthly", "Yearly"], key="interval_type")
        col_prev, col_next = st.columns(2)
        with col_prev:
            st.button("Previous", on_click=ui.callbacks.shift_time_interval, args=("previous",), use_container_width=True)
        with col_next:
            st.button("Next", on_click=ui.callbacks.shift_time_interval, args=("next",), use_container_width=True)
            
        st.header(f"{st.session_state.current_interval_start} - {st.session_state.current_interval_end}")
        
        column_data, column_graphs = st.columns([2, 1])
        df_transactions_filtered = filters.filter_by_date_period(df_transactions, 
                                                                st.session_state.current_interval_start, 
                                                                st.session_state.current_interval_end)
        df_transactions_filtered["category_color"] = df_transactions_filtered["category"].apply(lambda x: ui.utils.string_to_emoji(x))
        
        with column_data:
            data_editor_response = st.data_editor(
                df_transactions_filtered,
                use_container_width=True,
                height=500,
                key="transactions_table"
            )
            df_transactions_filtered = pd.DataFrame(data_editor_response)
        
        # Graph section
        with column_graphs:
            
            tab_category_overview, tab_trends = st.tabs(["Category overview", "Trends"])
            with tab_category_overview:

                col_expenses, col_incomes = st.columns([1, 1])
                # TODO: Replace code with module that calculates transaction amount sums by category
                with col_expenses:
                    df_transactions_expenses = df_transactions_filtered[df_transactions_filtered["transaction_type"] == "Expense"]
                    df_transactions_expenses["category_category_color"] = df_transactions_expenses["category"] + df_transactions_expenses["category_color"]
                    df_transactions_expenses = df_transactions_expenses \
                        .groupby(["category_category_color"]) \
                        .agg({"amount": "sum"}) \
                        .reset_index()
                    ui.charts.show_bar_chart(df_transactions_expenses, "category_category_color", "amount", "Transaction Amount Sums by Category (Expenses)", "Category", "Amount")

                with col_incomes:
                    df_transactions_incomes = df_transactions_filtered[df_transactions_filtered["transaction_type"] == "Income"]
                    df_transactions_incomes["category_category_color"] = df_transactions_incomes["category"] + df_transactions_incomes["category_color"]
                    df_transactions_incomes = df_transactions_incomes \
                        .groupby(["category_category_color"]) \
                        .agg({"amount": "sum"}) \
                        .reset_index()
                    ui.charts.show_bar_chart(df_transactions_incomes, "category_category_color", "amount", "Transaction Amount Sums by Category (Incomes)", "Category", "Amount")

            with tab_trends:
                df_transactions_filtered["signed_amount"] = df_transactions_filtered.apply(
                    lambda row: row["amount"] if row["transaction_type"] == "Income" else -row["amount"],
                    axis=1
                )
                df_transactions_filtered = df_transactions_filtered.groupby(df_transactions_filtered["date"].dt.date).agg({"signed_amount": "sum"}).reset_index()
                df_transactions_filtered["running_balance"] = df_transactions_filtered["signed_amount"].cumsum()

                # FIXME: Adapt for multiple currencies
                try:
                    cashflow = df_transactions_filtered['running_balance'].iloc[-1]
                    ui.charts.show_trends_chart(df_transactions_filtered, 
                                                "date", 
                                                "running_balance", 
                                                "green" if cashflow >= 0 else "red",
                                                f"Running Balance", 
                                                "Date", 
                                                "Amount")
                    st.write(f"Cashflow (interval): {cashflow:.2f} RON")
                except IndexError as _:
                    cashflow = None
                
        # st.header("Upload JSON Rules")
        # json_file = st.file_uploader("Upload your rules file (json)", type=["json"])
        # if json_file is not None:
        #     rules = load_json(json_file)
        #     if rules is not None:
        #         st.write("**Loaded Rules:**")
        #         st.json(rules)

if __name__ == "__main__":
    main()
