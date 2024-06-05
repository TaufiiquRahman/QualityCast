import base64
import streamlit as st
from PIL import ImageOps, Image
import numpy as np
import tensorflow as tf

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

def classify(image, model, class_names):
    """
    This function takes an image, a model, and a list of class names and returns the predicted class and confidence
    score of the image.

    Parameters:
        image (PIL.Image.Image): An image to be classified.
        model (tensorflow.keras.Model): A trained machine learning model for image classification.
        class_names (list): A list of class names corresponding to the classes that the model can predict.

    Returns:
        A tuple of the predicted class name and the confidence score for that prediction.
    """
    # Check if the image is grayscale
    if image.mode != 'L':
        image = ImageOps.grayscale(image)

    # Resize the image to match the input shape expected by the model
    image = image.resize((300, 300))

    # Convert image to numpy array and normalize
    image_array = np.array(image) / 255.0

    # Expand dimensions to match the input shape expected by the model
    image_array = np.expand_dims(image_array, axis=-1)  # Add channel dimension for grayscale image
    image_array = np.expand_dims(image_array, axis=0)   # Add batch dimension

    # Make prediction
    prediction = model.predict(image_array)

    # Determine the predicted class and confidence score
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name, confidence_score
