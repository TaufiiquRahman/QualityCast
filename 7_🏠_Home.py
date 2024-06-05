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
	@@ -72,22 +75,44 @@
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
        labels = [f'{class_name} ({conf_percentage:.1f}%)', 'Other']
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
