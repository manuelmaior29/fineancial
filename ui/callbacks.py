from datetime import timedelta

import pandas as pd
import streamlit as st

def shift_time_interval(direction: str):
    """
    Shifts the current time interval one step in the specified direction.
    <br> It uses the following values stored in the Streamlit session state:
    * 'current_interval_start': The start date of the current time interval.
    * 'current_interval_end': The end date of the current time interval.
    * 'interval_type': The type of time interval (e.g., "Weekly", "Monthly", "Yearly").

    Args:
        direction (str): "previous" or "next".
    """
    current_start = st.session_state["current_interval_start"]
    interval_type = st.session_state["interval_type"]

    if interval_type == "Weekly":
        new_start = pd.to_datetime(current_start).replace(hour=0, minute=0, second=0, microsecond=0)
        new_start -= pd.to_timedelta(new_start.weekday(), unit='D')
        delta = timedelta(weeks=1)
    elif interval_type == "Monthly":
        new_start = pd.to_datetime(current_start).replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        delta = pd.DateOffset(months=1)
    elif interval_type == "Yearly":
        new_start = pd.to_datetime(current_start).replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        delta = pd.DateOffset(years=1)
    else:
        return

    if direction == "previous":
        new_start -= delta
    elif direction == "next":
        new_start += delta
    else:
        return 
    new_end = new_start + delta
    st.session_state["current_interval_start"] = new_start
    st.session_state["current_interval_end"] = new_end