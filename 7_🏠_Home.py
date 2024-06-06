import streamlit as st
from keras.models import load_model
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from util import classify, set_background
from datetime import datetime
import os
import auth_functions

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

# -------------------------------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------------------------------
if 'user_info' not in st.session_state:
    col1, col2, col3 = st.columns([1, 2, 1])

    # Authentication form layout
    do_you_have_an_account = col2.selectbox(label='Do you have an account?', options=('Yes', 'No', 'I forgot my password'))
    auth_form = col2.form(key='Authentication form', clear_on_submit=False)
    email = auth_form.text_input(label='Email')
    password = auth_form.text_input(label='Password', type='password') if do_you_have_an_account in {'Yes', 'No'} else auth_form.empty()
    auth_notification = col2.empty()

    # Sign In
    if do_you_have_an_account == 'Yes' and auth_form.form_submit_button(label='Sign In', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Signing in'):
            auth_functions.sign_in(email, password)

    # Create Account
    elif do_you_have_an_account == 'No' and auth_form.form_submit_button(label='Create Account', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Creating account'):
            auth_functions.create_account(email, password)

    # Password Reset
    elif do_you_have_an_account == 'I forgot my password' and auth_form.form_submit_button(label='Send Password Reset Email', use_container_width=True, type='primary'):
        with auth_notification, st.spinner('Sending password reset link'):
            auth_functions.reset_password(email)

    # Authentication success and warning messages
    if 'auth_success' in st.session_state:
        auth_notification.success(st.session_state.auth_success)
        del st.session_state.auth_success
    elif 'auth_warning' in st.session_state:
        auth_notification.warning(st.session_state.auth_warning)
        del st.session_state.auth_warning

else:
    # Set title
    st.markdown('<div class="title-box">Quality Cast</div>', unsafe_allow_html=True)

    # Set header
    st.markdown('<div class="header-box">Please upload a Casting Product Image</div>', unsafe_allow_html=True)

    # Upload file
    file = st.file_uploader('', type=['jpeg', 'jpg', 'png'])

    # Load classifier
    model = load_model('./model.h5')

    # Load class names
    with open('./model/labels.txt', 'r') as f:
        class_names = [line.strip().split(' ')[1] for line in f.readlines()]

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
            top_classes = classify(image, model, class_names, top_n=1)

            # Display the top class and its confidence score
            top_class_name, top_conf_score = top_classes[0]
            top_conf_percentage = top_conf_score * 100

            # Get the index of the second class (other than the top class)
            second_class_index = 1 if top_class_name == class_names[0] else 0

            # Get the name and score of the second class
            second_class_name = class_names[second_class_index]
            second_conf_score = 1 - top_conf_score
            second_conf_percentage = 100 - top_conf_percentage

            # Display the box with scores of both classes
            st.markdown(f"""
            <div class="box">
                <h2 style="color: white; text-align: center;">Result</h2>
                <h3 style="color: white;">{top_class_name} - {top_conf_percentage:.1f}%</h3>
                <h3 style="color: white;">{second_class_name} - {second_conf_percentage:.1f}%</h3>
            </div>
            """, unsafe_allow_html=True)

            # Create a donut chart
            fig, ax = plt.subplots()
            sizes = [top_conf_score, second_conf_score]
            labels = [f'{class_name} ({conf_percentage:.1f}%)' for class_name, conf_percentage in zip([top_class_name, second_class_name], [top_conf_percentage, second_conf_percentage])]
            colors = ['#ff9999', '#66b3ff']
            ax.pie(sizes, labels=labels, colors=colors, startangle=90, counterclock=False, wedgeprops={'width': 0.3, 'edgecolor': 'w'})
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            # Display the donut chart
            st.pyplot(fig)

            # Save the result to history
            log = pd.DataFrame([{
                "filename": file.name,
                "class_name": top_class_name,
                "confidence_score": f"{top_conf_percentage:.1f}%",
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

    # Sign out
    if st.sidebar.button(label='Sign Out', on_click=auth_functions.sign_out, type='primary'):
        pass  #

