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
# Load classifier for binary classification (Defect or Perfect)
model = load_model('./modelcast.h5')

# Load class names for binary classification
with open('./model/labels.txt', 'r') as f:
    class_names = [line.strip() for line in f]

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
        class_index = classify(image, model, class_names)
        
        # Predicted class and confidence score
        predicted_class = class_names[class_index]
        conf_score = 100  # For binary classification, confidence is not available from the model directly
        
        # Write classification in a box
        st.markdown(f"""
        <div class="box">
            <h2>{predicted_class}</h2>
            <h3>Confidence score: {conf_score:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a donut chart
        fig, ax = plt.subplots()
        sizes = [100, 0]  # Sizes should sum up to 100 for the donut chart
        labels = [f'{predicted_class} ({conf_score:.1f}%)', 'Other']
        colors = ['#ff9999','#66b3ff']
        ax.pie(sizes, labels=labels, colors=colors, startangle=90, counterclock=False, wedgeprops={'width': 0.3, 'edgecolor': 'w'})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        # Display the donut chart
        st.pyplot(fig)
        
        # Save the result to history
        log = pd.DataFrame([{
            "filename": file.name,
            "class_names": predicted_class,
            "confidence_score": f"{conf_score:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        
        # Load existing history if available
        history_path = os.path.join(os.path.dirname(__file__), 'pages/history.csv')
        try:
            history = pd.read_csv(history_path)
        except FileNotFoundError:
            history = pd.DataFrame(columns=["filename", "class_names", "confidence_score", "timestamp"])
        
        # Append new log using pd.concat
        history = pd.concat([history, log], ignore_index=True)
        
        # Save updated history
        history.to_csv(history_path, index=False)
