from datetime import datetime

import streamlit as st
import pandas as pd

import ui.utils

def init():
    default_values = {
        "data_transactions": pd.DataFrame(),
        "input_data_transactions": 0,
        "interval_type": "Weekly",
        "current_interval_start": pd.to_datetime(datetime.now().replace(hour=0, minute=0, second=0)),
        "current_interval_end": ui.utils.calculate_interval_end(
            pd.to_datetime(datetime.now().replace(hour=0, minute=0, second=0)),
            interval_type="Weekly"
        ),
    }

    for key, default in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default
