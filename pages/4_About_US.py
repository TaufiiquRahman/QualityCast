import streamlit as st
import os
from PIL import Image

# Define CSS for the title, header, image name, and text boxes
markdown = """

Web App URL: <https://qualitycastapp.streamlit.app/>
GitHub Repository: <https://github.com/TaufiiquRahman/QualityCast>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


# Set title
st.title("Casting Quality Control")


# Set title
st.title("Contact Us")




# Set title
st.title("Team")

# Add content for the About Us page
st.write("This is the About Us page. You can provide information about your project, team, or any other relevant details here.")

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
