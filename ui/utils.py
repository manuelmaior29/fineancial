from datetime import datetime, timedelta
import hashlib

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

def string_to_rgb(s: str) -> str:
    """
    Converts a string to a consistent RGB color in hex format (e.g. '#aabbcc').

    Args:
        s (str): Input string (e.g., category name).

    Returns:
        str: Hex color string suitable for Plotly (e.g., '#1f77b4').
    """
    hash_digest = hashlib.md5(s.encode()).hexdigest()
    
    r = int(hash_digest[0:2], 16)
    g = int(hash_digest[2:4], 16)
    b = int(hash_digest[4:6], 16)

    def normalize_channel(c):
        return max(80, c) 

    r, g, b = map(normalize_channel, (r, g, b))

    return f"rgb({r},{g},{b})"

def string_to_emoji(text):
    emoji_pool = [
        "🍔", "🍕", "🍎", "🍩", "🚗", "✈️", "📦", "💡", "📚", "🏥", 
        "🎬", "🎧", "🛒", "💸", "🖥️", "📱", "🎮", "🧠", "🌍", "🧾"
    ]
    hash_val = int(hashlib.sha256(text.encode()).hexdigest(), 16)
    return emoji_pool[hash_val % len(emoji_pool)]
