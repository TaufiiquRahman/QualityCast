import streamlit as st


markdown = """
Web App URL: <https://qualitycastapp.streamlit.app/>
GitHub Repository: <https://github.com/TaufiiquRahman/QualityCast>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)


st.title("How To Use")

st.header("Instructions")

markdown = """
1. Firts Please Upload / Drag Image File to box 

"""

st.markdown(markdown)


