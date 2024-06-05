import streamlit as st
import os
from PIL import Image

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

# Set title and markdown for the "Contact Us" section
st.markdown("<h1 class='title-box'>Contact Us</h1>", unsafe_allow_html=True)
markdown_contact_us = """
1. First, Please Upload / Drag Image File to the box.
"""

st.markdown(markdown_contact_us)

# Set title and markdown for the "About Us" section
st.markdown("<h2 class='title-box'>About Us</h2>", unsafe_allow_html=True)
markdown_about_us = """
This is the About Us page. You can provide information about your project, team, or any other relevant details here.
"""

st.markdown(markdown_about_us)

# Set title for the "Team" section with center alignment
st.markdown("<h3 class='title-box'>Team</h3>", unsafe_allow_html=True)

# Path to the folder containing team member images
folder_path = "team"

# List all files in the folder
image_files = os.listdir(folder_path)

# Select the first 5 images and corresponding names and positions
team_data = [
    ("tim1", "Project Manager"),
    ("tim2", "UI/UX Specialist"),
    ("tim3", "Copy Writer"),
    ("tim4", "AI Engineer"),
    ("tim5", "Back End Engineer")
] 

# Split the page into 5 columns
columns = st.columns(5)

for i, (name, position) in enumerate(team_data):
    image_file = f"{name.lower()}.jpg"  
    image_path = os.path.join(folder_path, image_file)
    with Image.open(image_path) as img:
        # Resize image to a smaller size
        resized_img = img.resize((200, 200))  # Resize image to 200x200 pixels
        # Display image in the corresponding column
        columns[i].image(resized_img, caption=f"{name}", use_column_width=True)
        # Center-align the position text
        columns[i].write(f"<p style='text-align:center'>{position}</p>", unsafe_allow_html=True)
