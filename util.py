import base64
import streamlit as st
from PIL import ImageOps, Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

def set_background(image_file):
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
    if image.mode != 'L':
        image = ImageOps.grayscale(image)

    image = image.resize((300, 300))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=-1)
    image_array = np.expand_dims(image_array, axis=0)

    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name, confidence_score

def visualize_predictions(model, test_set, class_map, img_size, batch_size):
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
        prob_class = 100 * pred_prob if
