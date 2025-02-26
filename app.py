import json
import streamlit as st
import pandas as pd
import io
from src.preprocessing.parser import *
from src.models.rulebased import *


if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame()
if "transactions_classification_rules" not in st.session_state:
    st.session_state.transactions_classification_rules = None
if "transactions_classifier_model" not in st.session_state:
    st.session_state.transactions_classifier_model = RuleBasedClassifier(rules=None)

def parse_classification_rules(file):
    try:
        classification_rules = {}
        classification_rules = json.load(file)
        return classification_rules
    except Exception as e:
        st.error(f"Error parsing the classification rules: {e}")
        return {}

def parse_xlsx(file):
    try:
        # TODO: Replace hardcoded parser
        parser = BTParser()
        transaction_data = parser.parse(document_path=file)
        return pd.DataFrame([transaction.__dict__ for transaction in transaction_data])
    except Exception as e:
        st.error(f"Error processing file: {e}")
        return pd.DataFrame()

st.set_page_config(layout='wide')
st.title("💰 Bank Transactions Parser")

uploaded_rules_file = st.file_uploader("Upload rules for transaction classification", type=["json"])
if uploaded_rules_file is not None:
    classification_rules = parse_classification_rules(uploaded_rules_file)
    st.session_state.transactions_classification_rules = classification_rules
    st.session_state.transactions_classifier_model = RuleBasedClassifier(rules=classification_rules)
    st.success("✅ Classification rules parsed successfully!")

uploaded_file = st.file_uploader("Upload a bank statement (CSV)", type=["csv"])
if uploaded_file is not None:
    parsed_transactions = parse_xlsx(uploaded_file)

    if not parsed_transactions.empty and st.session_state.transactions_classification_rules:
        st.success("✅ Transactions parsed successfully!")
        parsed_transactions["category"] = parsed_transactions["cleaned_desc"].map(lambda x: st.session_state.transactions_classifier_model.classify(x))
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
