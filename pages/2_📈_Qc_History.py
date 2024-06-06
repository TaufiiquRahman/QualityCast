import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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
    # Drop the class_name column
    history.drop(columns=['class_name'], inplace=True)
    st.table(history)

    # Add a download button
    csv = history.to_csv(index=False)
    st.download_button(
        label="Download History (CSV)",
        data=csv,
        file_name='classification_history.csv',
        mime='text/csv'
    )

    # Define the function to share via email
    def share_via_email(history):
        # Email configuration
        sender_email = "qualitycastapp@gmail.com"
        sender_password = "p123456-*"
        receiver_email = "taufiiqurahman@gmail.com"
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Classification History"

        # Attach history as a CSV file
        csv_data = history.to_csv(index=False)
        attachment = MIMEText(csv_data, 'csv')
        attachment.add_header('Content-Disposition', 'attachment', filename='classification_history.csv')
        message.attach(attachment)

        # Connect to SMTP server and send email
        try:
            with smtplib.SMTP_SSL('smtp.example.com', 465) as server:
                server.login(sender_email, sender_password)
                server.send_message(message)
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Add a button to share the history via Email
    if st.button("Share via Email"):
        share_via_email(history)


except FileNotFoundError:
    st.write("No history available. Please upload and classify images using the home page.")
