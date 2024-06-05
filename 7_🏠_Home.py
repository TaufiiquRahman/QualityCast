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

# Function to classify images
def classify(image, model, class_names):
    # Preprocess the image
    image = image.resize((300, 300))  # Resize image
    image_array = np.array(image) / 255.0  # Normalize image
    image_array = np.expand_dims(image_array, axis=0)  # Add batch dimension

    # Make prediction
    prediction = model.predict(image_array)[0]

    # Get class names and scores
    class_names = np.array(class_names)
    top_indices = np.argsort(prediction)[::-1][:2]  # Top 2 classes
    top_classes = class_names[top_indices]
    top_scores = prediction[top_indices]

    return top_classes, top_scores

# Load model and class names
model = load_model('./model.h5')
with open('./model/labels.txt', 'r') as f:
    class_names = [line.strip() for line in f]

# Set background
set_background('./bgrd/bg.jpg')

# Set title and header
st.markdown('<div class="title-box">Casting Quality Control</div>', unsafe_allow_html=True)
st.markdown('<div class="header-box">Please upload a Casting Product Image</div>', unsafe_allow_html=True)

# Upload file
file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])

# Display image and classification results
if file is not None:
    col1, col2 = st.columns(2)
    with col1:
        image = Image.open(file).convert('RGB')
        st.image(image, use_column_width=True)
        st.markdown(f'<div class="filename-box">Uploaded file: {file.name}</div>', unsafe_allow_html=True)
    with col2:
        # Classify image
        classes, scores = classify(image, model, class_names)

        # Display classification results
        for cls, score in zip(classes, scores):
            st.markdown(f'<div class="box"><h2>{cls}</h2><h3>Score: {score:.4f}</h3></div>', unsafe_allow_html=True)

        # Save the result to history
        log = pd.DataFrame([{
            "filename": file.name,
            "class_name": cls,
            "confidence_score": f"{score:.4f}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        } for cls, score in zip(classes, scores)])

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
