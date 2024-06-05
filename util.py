import base64
import streamlit as st
from PIL import ImageOps, Image
import numpy as np
import tensorflow as tf
import os

def set_background(image_file):
    """
    This function sets the background of a Streamlit app to an image specified by the given image file.

    Parameters:
        image_file (str): The path to the image file to be used as the background.

    Returns:
        None
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

def classify_new(image, model, class_names):
    """
    This function takes an image, a model, and a list of class names and returns the predicted class and confidence
    score of the image using a different prediction approach.

    Parameters:
        image (PIL.Image.Image): An image to be classified.
        model (tensorflow.keras.Model): A trained machine learning model for image classification.
        class_names (list): A list of class names corresponding to the classes that the model can predict.

    Returns:
        A tuple of the predicted class name and the confidence score for that prediction.
    """
    # Convert image to grayscale if not already
    if image.mode != 'L':
        image = ImageOps.grayscale(image)
    
    # Resize the image to the input shape expected by the model
    image = image.resize((300, 300))

    # Convert image to numpy array and normalize
    image_array = np.array(image) / 255.0

    # Add batch dimension (1, 300, 300, 1)
    image_array = np.expand_dims(image_array, axis=(0, -1))

    # Make prediction using the model
    prediction = model.predict(image_array)

    # Get the index of the class with the highest probability
    predicted_index = np.argmax(prediction, axis=1)[0]

    # Get the class name and confidence score
    predicted_class = class_names[predicted_index]
    confidence_score = prediction[0][predicted_index]

    return predicted_class, confidence_score
