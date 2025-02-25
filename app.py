import streamlit as st
import pandas as pd
import io
from src.preprocessing.parser import *

STANDARD_FIELDS = [
    "Transaction type", "Category", "Label", "Date",
    "Cleaned Transaction Description", "Notes", "Amount", "Currency"
]

if "transactions" not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=STANDARD_FIELDS)

def parse_xlsx(file):
    try:
        # TODO: Replace hardcoded parser
        parser = BTParser()
        transaction_data = parser.parse(document_path=file)
        return pd.DataFrame([transaction.__dict__ for transaction in transaction_data])

    except Exception as e:
        st.error(f"Error processing file: {e}")
        return pd.DataFrame(columns=STANDARD_FIELDS)

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
st.dataframe(st.session_state.transactions)
st.subheader("⬇️ Download Transactions")
buffer = io.BytesIO()
st.session_state.transactions.to_excel(buffer, index=False)
st.download_button(
    label="Download as Excel",
    data=buffer.getvalue(),
    file_name="aggregated_transactions.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
