from datetime import datetime

import streamlit as st
import pandas as pd

def init():
    default_values = {
        "data_transactions": pd.DataFrame(),
        "input_data_transactions": 0,
        "interval_type": "Weekly",
        "current_interval_start": pd.to_datetime(datetime.now().replace(day=1)),
        "current_interval_end": pd.to_datetime(datetime.now()),
    }

    for key, default in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default
