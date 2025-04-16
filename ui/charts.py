import sys

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

sys.path.append("../src")
from utils import string_to_rgb

def show_trends_chart(df: pd.DataFrame, x: str, y: str, color: str, title: str, x_title: str, y_title: str):
    fig = go.Figure(data=[go.Scatter(
        x=df[x],
        y=df[y],
        mode="lines",
        name="Running Balance",
        line=dict(color=color),
    )])
    fig.update_layout(
        title=title,
        xaxis_title=x_title,
        yaxis_title=y_title,
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, x_title: str, y_title: str):
    fig = go.Figure(data=[go.Bar(x=df[x], 
                                 y=df[y], 
                                 marker_color=[string_to_rgb(category) for category in df[x]])])
    fig.update_layout(title=title, xaxis_title=x_title, yaxis_title=y_title)
    st.plotly_chart(fig)