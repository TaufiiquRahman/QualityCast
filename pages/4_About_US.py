import streamlit as st
import os
from PIL import Image

# Set title
st.title("About Us")
    
# Add content for the About Us page
st.write("This is the About Us page. You can provide information about your project, team, or any other relevant details here.")

# Path to the folder containing team member images
folder_path = "team"

# List all files in the folder
image_files = os.listdir(folder_path)

# Select the first 5 images and corresponding names and positions
team_data = [
    ("tim1", "Desainer"),
    ("tim2", "Pemasaran"),
    ("tim3", "Pengembang"),
    ("tim4", "Manajer Proyek"),
    ("tim5", "Spesialis UI/UX")
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


#st.markdown(markdown, unsafe_allow_html=True)
