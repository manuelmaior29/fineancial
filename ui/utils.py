from datetime import datetime, timedelta

import pandas as pd

def calculate_interval_end(start_date: datetime, interval_type: str) -> datetime:
    if interval_type == "Daily":
        return start_date + timedelta(days=1)
    elif interval_type == "Weekly":
        return start_date + timedelta(weeks=1)
    elif interval_type == "Monthly":
        return (pd.Timestamp(start_date) + pd.DateOffset(months=1)).to_pydatetime()
    elif interval_type == "Yearly":
        return (pd.Timestamp(start_date) + pd.DateOffset(years=1)).to_pydatetime()
    else:
        raise ValueError(f"Unsupported interval type: {interval_type}")
