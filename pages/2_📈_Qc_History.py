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
try:
    history = pd.read_csv(history_path)

    # Add filename column to the table
    history_with_filename = history.copy()
    history_with_filename['filename'] = history_with_filename['filename'].apply(lambda x: os.path.basename(x))
    
    # Filter history by class_name
    defect_history = history_with_filename[history_with_filename['class_name'] == 'Defect'][['filename', 'class_name', 'confidence_score', 'timestamp']]
    perfect_history = history_with_filename[history_with_filename['class_name'] == 'Perfect'][['filename', 'class_name', 'confidence_score', 'timestamp']]

    # Display the filtered histories
    st.markdown('<h2 style="color: white;">Defect History</h2>', unsafe_allow_html=True)
    st.table(defect_history)

    st.markdown('<h2 style="color: white;">Perfect History</h2>', unsafe_allow_html=True)
    st.table(perfect_history)

except FileNotFoundError:
    st.write("No history available. Please upload and classify images using the home page.")
