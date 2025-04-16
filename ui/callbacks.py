from datetime import timedelta

import pandas as pd
import streamlit as st

def shift_time_interval(direction: str):
    """
    Shifts the current time interval one step in the specified direction.
    <br> It uses the following values stored in the Streamlit session state:
    * 'current_interval_start': The start date of the current time interval.
    * 'interval_type': The type of time interval (e.g., "Daily", "Weekly", "Monthly", "Yearly").

    Args:
        direction (str): "previous" or "next".
    """

    current = st.session_state["current_interval_start"]
    interval_type = st.session_state["interval_type"]

    if interval_type == "Daily":
        delta = timedelta(days=1)
    elif interval_type == "Weekly":
        delta = timedelta(weeks=1)
    elif interval_type == "Monthly":
        delta = pd.DateOffset(months=1)
    elif interval_type == "Yearly":
        delta = pd.DateOffset(years=1)
    else:
        return

    if direction == "previous":
        st.session_state["current_interval_start"] = current - delta
    elif direction == "next":
        st.session_state["current_interval_start"] = current + delta
