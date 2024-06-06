import streamlit as st
from PIL import Image
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(page_title="About Us", page_icon=":busts_in_silhouette:", layout="wide")

# Function to construct file paths relative to the parent directory
def construct_file_path(file_name):
    # Construct absolute path from current file's directory
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'team'))
    return os.path.join(base_path, file_name)

def check_and_load_image(file_path):
    logger.info(f"Trying to load image from: {file_path}")
    if os.path.exists(file_path):
        try:
            img = Image.open(file_path)
            return img
        except Exception as e:
            st.error(f"Error loading image at {file_path}: {e}")
    else:
        st.error(f"Image file not found at {file_path}")
    return None

with st.container():
    st.subheader("Quality Control Casting Production :microscope: ")
    st.write("This project aims to develop a quality control system for casting production results. The system will use deep learning algorithms to classify production results as either Perfect or defect.")

with st.container():
    st.markdown("---")
    st.subheader("Contacts Us :envelope: ")
    st.write("If you have any questions or would like to learn more about us, please contact us by email at qualitycastingapp@mail.com or send us a direct message on LinkedIn and Instagram.")
with st.container():
    st.markdown("---")
    st.subheader("Team :package:")
    
    team_members = [
        {"name": "Daniel Nuralamsyah", "role": "Project Manager", "image": construct_file_path('daniel.jpg')},
        {"name": "Kiki Zakiah Nafsi", "role": "Copywriter", "image": construct_file_path('kiki.png')},
        {"name": "Mailani Elisa", "role": "Designer", "image": construct_file_path('mailani.jpg')},
        {"name": "Taufiqu Rahman", "role": "AI Engineer", "image": construct_file_path('taufiqu.png')},
        {"name": "Abdan Syakura", "role": "Backend Engineer", "image": construct_file_path('abdan.jpg')}
    ]
    
    cols = st.columns(len(team_members))
    for col, member in zip(cols, team_members):
        img = check_and_load_image(member["image"])
        if img:
            col.image(img, caption=f"{member['name']} as {member['role']}")
        else:
            col.error(f"Image for {member['name']} not found.")

# Displaying additional images in one line, centered
with st.container():
    st.markdown('<style>div.Widget.row-widget.stHorizontal {flex-direction: row; justify-content: center;}</style>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    kampus_merdeka_icon_path = construct_file_path("kampus_merdeka.jpg")
    skilvul_icon_path = construct_file_path("skilvul.jpg")
    github_icon_path = construct_file_path("github-mark.png")
    linkedin_icon_path = construct_file_path("linkedin.jpg")
    instagram_icon_path = construct_file_path("instagram.jpg")


    
    
    if os.path.exists(kampus_merdeka_icon_path):
        col1.image(kampus_merdeka_icon_path, width=75)
    else:
        col1.error("Kampus Merdeka icon not found.")
    
    
    if os.path.exists(skilvul_icon_path):
        col2.image(skilvul_icon_path, width=75)
    else:
        col2.error("Skilvul icon not found.")
    

    if os.path.exists(github_icon_path):
        col3.image(github_icon_path, width=75)
    else:
        col3.error("GitHub icon not found.")
    
    
    if os.path.exists(linkedin_icon_path):
        col4.image(linkedin_icon_path, width=75)
    else:
        col4.error("LinkedIn icon not found.")
    
    
    if os.path.exists(instagram_icon_path):
        col5.image(instagram_icon_path, width=75)
    else:
        col5.error("Instagram icon not found.")
    
    
# Display copyright notice centered below the icons
with st.container():
    st.markdown('<p style="text-align:center;">Hak Cipta © 2024 QualityCast</p>', unsafe_allow_html=True)
