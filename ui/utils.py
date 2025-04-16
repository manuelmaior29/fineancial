from datetime import datetime, timedelta

import pandas as pd

def shift_interval(start_date, interval_type, direction):
    if interval_type == "Daily":
        return start_date + timedelta(days=direction)
    elif interval_type == "Weekly":
        return start_date + timedelta(weeks=direction)
    elif interval_type == "Monthly":
        return (start_date + pd.DateOffset(months=direction)).replace(day=1)
    elif interval_type == "Yearly":
        return (start_date + pd.DateOffset(years=direction)).replace(month=1, day=1)

