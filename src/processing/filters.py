from datetime import datetime
import pandas as pd

def filter_by_date_period(df: pd.DataFrame, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    df_out = df[(df["date"] >= start_date) & (df["date"] <= end_date)]
    df_out = df_out.sort_values("date", ascending=True)
    return df_out
