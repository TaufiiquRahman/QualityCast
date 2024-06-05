import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import classify, set_background
from datetime import datetime
import os

# Set background
set_background('./bgrd/bg.jpg')

# Define CSS for the title, header, image name, and text boxes
st.markdown(
    """
    <style>
    .title-box, .header-box, .filename-box, .box {
        border: 1px solid #000;
        padding: 10px;
        border-radius: 5px;
        background-color: #333;
        color: white;
        margin-top: 20px;
    }
    .title-box {
        text-align: center;
        font-size: 32px;
        font-weight: bold;
    }
    .header-box {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
    }
    .filename-box {
        text-align: center;
        font-size: 18px;
    }
    .box h2, .box h3 {
        margin: 0;
        color: white; /* Add this line to set text color to white */
    }
    </style>
    """, unsafe_allow_html=True
)
# Set title
st.markdown('<div class="title-box">Casting Quality Control</div>', unsafe_allow_html=True)

# Set header
st.markdown('<div class="header-box">Please upload a Casting Product Image</div>', unsafe_allow_html=True)

# Upload file
file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])

# Load classifier
model = load_model('./model.h5')

# Load class names
with open('./model/labels.txt', 'r') as f:
    class_names = [a[:-1].split(' ')[1] for a in f.readlines()]

# Display image and classification results
if file is not None:
    # Create two columns for layout
    col1, col2 = st.columns(2)
    
    # Column 1: Image and file name
    with col1:
        image = Image.open(file).convert('RGB')
        st.image(image, use_column_width=True)
        st.markdown(f'<div class="filename-box">Uploaded file: {file.name}</div>', unsafe_allow_html=True)
    
    # Column 2: Classification result and donut chart
    with col2:
        # Classify image
        top_classes = classify(image, model, class_names, top_n=5)
        
        # Calculate percentages for Perfect and Defect
        perfect_percentage = sum([score for class_name, score in top_classes if class_name == "Perfect"]) * 100
        defect_percentage = sum([score for class_name, score in top_classes if class_name == "Defect"]) * 100
        
        # Create a box to display percentage results
        st.markdown(f'<div class="box"><h2>Perfect</h2><h3>Percentage: {perfect_percentage:.1f}%</h3></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="box"><h2>Defect</h2><h3>Percentage: {defect_percentage:.1f}%</h3></div>', unsafe_allow_html=True)
        
        # Create a donut chart for Perfect and Defect predictions
        fig, ax = plt.subplots()
        sizes = [score for class_name, score in top_classes]
        labels = [f'{class_name} ({score*100:.1f}%)' for class_name, score in top_classes]
        colors = ['white' if class_name == "Perfect" else 'red' for class_name, _ in top_classes]
        ax.pie(sizes, labels=labels, colors=colors, startangle=90, counterclock=False, wedgeprops={'width': 0.3, 'edgecolor': 'w'})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
        
        # Save the result to history
        log = pd.DataFrame([{
            "filename": file.name,
            "class_name": class_name,
            "confidence_score": f"{conf_score*100:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } for class_name, conf_score in top_classes])
        
        # Load existing history if available
        history_path = os.path.join(os.path.dirname(__file__), 'pages/history.csv')
        try:
            history = pd.read_csv(history_path)
        except FileNotFoundError:
            history = pd.DataFrame(columns=["filename", "class_name", "confidence_score", "timestamp"])
        
        # Append new log using pd.concat
        history = pd.concat([history, log], ignore_index=True)
        
        # Save updated history
        history.to_csv(history_path, index=False)
