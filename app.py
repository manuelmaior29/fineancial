import sys
sys.path.append("src")

import streamlit as st
import pandas as pd
import json
from st_aggrid import AgGrid, GridOptionsBuilder
from preprocessing.parser import BTParser

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
    st.title("Editable Bank Transactions Table")

    csv_file = st.file_uploader("Upload your bank transactions file (CSV)", type=["csv"])
    if csv_file is not None:
        transactions = []
        parser = BTParser()
        transactions = parser.parse(csv_file, substrings_to_remove=[], sep=",")
        print(transactions[0].__dict__)
        df_transactions = pd.DataFrame([transaction.__dict__ for transaction in transactions])

        gb = GridOptionsBuilder.from_dataframe(df_transactions)
        gb.configure_default_column(editable=True)
        grid_options = gb.build()

        _ = AgGrid(df_transactions, gridOptions=grid_options, editable=True, height=400)

    st.header("Upload JSON Rules")
    json_file = st.file_uploader("Upload your rules file (json)", type=["json"])
    if json_file is not None:
        rules = load_json(json_file)
        if rules is not None:
            st.write("**Loaded Rules:**")
            st.json(rules)

if __name__ == "__main__":
    main()
