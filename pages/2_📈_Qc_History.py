import streamlit as st
import pandas as pd
import os

# Define CSS for the title and table
st.markdown(
    """
    <style>
    .title-box {
        border: 1px solid #000;
        padding: 10px;
        border-radius: 5px;
        background-color: #333;
        color: white;
        text-align: center;
        font-size: 32px;
        font-weight: bold;
        margin-top: 20px;
    }
    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 5px;
        overflow: hidden;
    }
    .stDataFrame table {
        border-collapse: collapse;
        width: 100%;
    }
    .stDataFrame th, .stDataFrame td {
        text-align: left;
        padding: 8px;
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #ff7f50;  /* Coral color */
    }
    .stDataFrame tr:nth-child(odd) {
        background-color: #fff;
    }
    .stDataFrame tr:hover {
        background-color: #ff6347;  /* Darker coral color for hover */
    }
    </style>
    """, unsafe_allow_html=True
)

# Set title for history page
st.markdown('<div class="title-box">Classification History</div>', unsafe_allow_html=True)

# Load the history
history_path = os.path.join(os.path.dirname(__file__), 'history.csv')
st.write(f"History file path: {history_path}")

# Check if the file exists
if not os.path.exists(history_path):
    st.write("History file not found.")
else:
    try:
        history = pd.read_csv(history_path)
        st.table(history)
    except Exception as e:
        st.write(f"Error reading history.csv: {e}")
#
