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
model = load_model('./modelcast.h5')

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
        class_name, conf_score = classify(image, model, class_names)
        conf_percentage = conf_score * 100
        
        # Write classification in a box
        st.markdown(f"""
        <div class="box">
            <h2>{class_name}</h2>
            <h3>score: {conf_percentage:.1f}%</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Create a donut chart
        fig, ax = plt.subplots()
        sizes = [conf_score, 1 - conf_score]
        labels = [f'{class_name} ({conf_percentage:.1f}%)', 'Perfect']
        colors = ['#ff9999','#66b3ff']
        ax.pie(sizes, labels=labels, colors=colors, startangle=90, counterclock=False, wedgeprops={'width': 0.3, 'edgecolor': 'w'})
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        
        # Display the donut chart
        st.pyplot(fig)
        
        # Save the result to history
        log = pd.DataFrame([{
            "filename": file.name,
            "class_name": class_name,
            "confidence_score": f"{conf_percentage:.1f}%",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }])
        
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

# Button to show predictions on test images
if st.button('Show Predictions on Test Images'):
    class_map = {0: 'Defect', 1: 'Perfect'}
    
    # Assuming you have a test_set and related parameters defined
    # Please replace the following placeholders with your actual values or data loading logic
    test_set = ...  # Load your test set here
    img_size = (300, 300)  # Replace with your actual image size
    batch_size = 3  # Replace with your actual batch size

    images, labels = next(iter(test_set))
    images = images.reshape(batch_size, *img_size)

    fig, axes = plt.subplots(1, 3, figsize=(9, 4))
    fig.suptitle('Prediction on Test Images', y=0.98, weight='bold', size=14)
    for ax, img, label in zip(axes.flat, images, labels):
        ax.imshow(img, cmap='gray')
        [[pred_prob]] = model.predict(img.reshape(1, *img_size, -1))
        pred_label = class_map[int(pred_prob >= 0.5)]
        true_label = class_map[label]
        prob_class = 100 * pred_prob if pred_label == 'Perfect' else 100 * (1 - pred_prob)
        ax.set_title(f'Actual: {true_label}', size=12)
        ax.set_xlabel(f'Predicted: {pred_label} ({prob_class:.2f}%)',
                      color='g' if pred_label == true_label else 'r')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    st.pyplot(fig)
