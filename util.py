import base64
import streamlit as st
from PIL import ImageOps, Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

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

def visualize_predictions(model, test_set, class_map, img_size, batch_size):
    """
    This function visualizes the predictions of a model on a given test set.

    Parameters:
        model (tensorflow.keras.Model): A trained machine learning model for image classification.
        test_set (tf.data.Dataset): A dataset containing the test images.
        class_map (dict): A dictionary mapping class indices to class names.
        img_size (tuple): A tuple containing the dimensions of the input images.
        batch_size (int): The batch size used for inference.

    Returns:
        None
    """
    images, labels = next(iter(test_set))
    images = images.numpy().reshape(batch_size, *img_size)

    fig, axes = plt.subplots(1, 3, figsize=(9, 4))
    fig.suptitle('Prediction on Test Images', y=0.98, weight='bold', size=14)
    for ax, img, label in zip(axes.flat, images, labels):
        ax.imshow(img, cmap='gray')
        [[pred_prob]] = model.predict(img.reshape(1, *img_size, -1))
        pred_label = class_map[int(pred_prob >= 0.5)]
        true_label = class_map[label]
        prob_class = 100 * pred_prob if pred_label == 'Perfect' else 100 * (1 - pred_prob)
        ax.set_title(f'Actual: {true_label}', size=12)
        ax.set_xlabel(f'Predicted: {pred_label} ({prob_class:.2f}%)', color='g' if pred_label == true_label else 'r')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    st.pyplot(fig)

def visualize_misclassified(model, test_set, class_map, img_size, batch_size):
    """
    This function visualizes misclassified images on a given test set.

    Parameters:
        model (tensorflow.keras.Model): A trained machine learning model for image classification.
        test_set (tf.data.Dataset): A dataset containing the test images.
        class_map (dict): A dictionary mapping class indices to class names.
        img_size (tuple): A tuple containing the dimensions of the input images.
        batch_size (int): The batch size used for inference.

    Returns:
        None
    """
    y_true, y_pred = [], []

    for images, labels in test_set:
        predictions = model.predict(images)
        y_true.extend(labels.numpy())
        y_pred.extend([1 if pred >= 0.5 else 0 for pred in predictions])

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    misclassified = np.nonzero(y_pred != y_true)[0]
    batch_num = misclassified // batch_size
    image_num = misclassified % batch_size

    fig, axes = plt.subplots(1, 4, figsize=(12, 4))
    fig.suptitle('Misclassified Test Images', y=0.98, weight='bold', size=14)
    for ax, bnum, inum in zip(axes.flat, batch_num, image_num):
        images, labels = next(iter(test_set.skip(bnum).take(1)))
        img = images[inum].numpy()
        ax.imshow(img.reshape(*img_size), cmap='gray')
        [[pred_prob]] = model.predict(img.reshape(1, *img_size, -1))
        pred_label = class_map[int(pred_prob >= 0.5)]
        true_label = class_map[labels[inum]]
        prob_class = 100 * pred_prob if pred_label == 'Perfect' else 100 * (1 - pred_prob)
        ax.set_title(f'Actual: {true_label}', size=12)
        ax.set_xlabel(f'Predicted: {pred_label} ({prob_class:.2f}%)',
                      color='g' if pred_label == true_label else 'r')
        ax.set_xticks([])
        ax.set_yticks([])
    plt.tight_layout()
    plt.show()
