import sys

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

sys.path.append("../src")
import ui.utils

def show_trends_chart(df: pd.DataFrame, x: str, y: str, color: str, title: str, x_title: str, y_title: str):
    fig = go.Figure(data=[go.Scatter(
        x=df[x],
        y=df[y],
        mode="lines",
        name=title,
        line=dict(color=color),
    )])
    fig.update_layout(
        title={
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=f"{x_title}",
        yaxis_title=f"{y_title}",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, x_title: str, y_title: str):
    fig = go.Figure(data=[go.Bar(x=df[x], 
                                 y=df[y], 
                                 marker_color=[ui.utils.string_to_rgb(category) for category in df[x]])])
    fig.update_layout(
        title={
            'text': title,
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title=f"{x_title}",
        yaxis_title=f"{y_title}",
    )
    st.plotly_chart(fig)