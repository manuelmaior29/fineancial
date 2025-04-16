from datetime import datetime

import streamlit as st
import pandas as pd

def init():
    default_values = {
        "interval_type": "Monthly",
        "current_interval_start": pd.to_datetime(datetime.now().replace(day=1))
    }

    for key, default in default_values.items():
        if key not in st.session_state:
            st.session_state[key] = default
