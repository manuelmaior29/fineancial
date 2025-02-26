import json
import streamlit as st
import pandas as pd
import io
from src.preprocessing.parser import *
from src.models.rulebased import *


if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame()
if "transactions_classification_rules" not in st.session_state:
    st.session_state.transactions_classification_rules = {}
if "transactions_classifier_model" not in st.session_state:
    st.session_state.transactions_classifier_model = RuleBasedClassifier()

def parse_classification_rules(file):
    try:
        classification_rules = {}
        with open(file, "r") as f:
            classification_rules = json.load(f)
        return classification_rules
    except Exception as e:
        st.error(f"Error parsing the classification rules: {e}")
        return {}

def parse_xlsx(file):
    try:
        # TODO: Replace hardcoded parser
        parser = BTParser()
        transaction_data = parser.parse(document_path=r"C:\Users\mam2clj\Documents\Personal\Documents\RO35BTRLRONCRT0285357701-01.01.2025-01.02.2025.csv")
        return pd.DataFrame([transaction.__dict__ for transaction in transaction_data])
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return pd.DataFrame()

st.set_page_config(layout='wide')
st.title("💰 Bank Transactions Parser")
uploaded_file = st.file_uploader("Upload a bank statement (CSV)", type=["csv"])
if uploaded_file is not None:
    parsed_transactions = parse_xlsx(uploaded_file)

    if not parsed_transactions.empty:
        st.success("✅ Transactions parsed successfully!")
        st.session_state.transactions = pd.concat(
            [st.session_state.transactions, parsed_transactions], ignore_index=True
        )

st.subheader("📊 All Transactions")
st.data_editor(st.session_state.transactions)
st.subheader("⬇️ Download Transactions")
buffer = io.BytesIO()
st.session_state.transactions.to_excel(buffer, index=False)
st.download_button(
    label="Download as Excel",
    data=buffer.getvalue(),
    file_name="aggregated_transactions.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
