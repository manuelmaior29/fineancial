import hashlib

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
