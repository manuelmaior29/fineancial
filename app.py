import sys

import streamlit as st
import pandas as pd

sys.path.append("src")
from transaction_classification.adapter import TransactionClassificationAdapter
from transaction_classification.models.rulebased.rulebased import RuleBasedTransactionClassifier
import processing.filters as filters
import ui.charts
import ui.state
import ui.callbacks
import ui.inputs
import ui.static_content

def main():
    ui.state.init()
    st.set_page_config(page_title="fineancial", 
                       page_icon=":moneybag:",
                       layout="wide")
    st.title("fineancial")

    # AI-driven modules
    classification_rules = ui.inputs.upload_file(label=ui.static_content.LABEL_UPLOAD_FILE_CLASSIFICATION_RULES, 
                                                 file_types=["json"], 
                                                 parser_fn=ui.inputs.parse_json, 
                                                 key="file_classification_rules")

    # Upload CSV file(s) with raw transactions data
    transactions = ui.inputs.upload_file(label=ui.static_content.LABEL_UPLOAD_FILE_TRANSACTIONS, 
                                         file_types=["csv", "xlsx"],
                                         parser_fn=ui.inputs.parse_transactions,
                                         key="file_transactions_data",
                                         allow_multiple=True)
    
    if transactions and classification_rules:
        # TODO: Prepare code for hotswapping
        transaction_classification_model_rule_based = RuleBasedTransactionClassifier(rules=classification_rules)
        transaction_classification_adapter = TransactionClassificationAdapter(model=transaction_classification_model_rule_based, preprocess_fn=lambda x: x.cleaned_desc, postprocess_fn=lambda x: x)

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
                with col_expenses:
                    df_transactions_expenses = df_transactions_filtered[df_transactions_filtered["transaction_type"] == "Expense"]
                    df_transactions_expenses = df_transactions_expenses.groupby(["category"]).agg({"amount": "sum"}).reset_index()
                    ui.charts.show_bar_chart(df_transactions_expenses, "category", "amount", "Transaction Amount Sums by Category (Expenses)", "Category", "Amount")

                with col_incomes:
                    df_transactions_incomes = df_transactions_filtered[df_transactions_filtered["transaction_type"] == "Income"]
                    df_transactions_incomes = df_transactions_incomes.groupby(["category"]).agg({"amount": "sum"}).reset_index()
                    ui.charts.show_bar_chart(df_transactions_incomes, "category", "amount", "Transaction Amount Sums by Category (Incomes)", "Category", "Amount")

            with tab_trends:
                df_transactions_filtered["signed_amount"] = df_transactions_filtered.apply(
                    lambda row: row["amount"] if row["transaction_type"] == "Income" else -row["amount"],
                    axis=1
                )
                df_transactions_filtered = df_transactions_filtered.groupby(df_transactions_filtered["date"].dt.date).agg({"signed_amount": "sum"}).reset_index()
                df_transactions_filtered["running_balance"] = df_transactions_filtered["signed_amount"].cumsum()

                # FIXME: Adapt for multiple currencies
                try:
                    cashflow = df_transactions_filtered['running_balance'].iloc[-1] - df_transactions_filtered['running_balance'].iloc[0]
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
            
if __name__ == "__main__":
    main()
