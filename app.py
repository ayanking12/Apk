import streamlit as st
from PIL import Image
import io

# Page Config
st.set_page_config(page_title="Rajput Flex Maker", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #013220; }
    stButton>button { width: 100%; background-color: #ffcc00; color: black; font-weight: bold; height: 50px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🗳️ Election Flex Maker")
st.success("App live hai! Ab ye foran chalegi.")

# Sidebar Settings
mode = st.sidebar.radio("Kitne bande?", ["Single Person", "Multiple People"])
user_name = st.sidebar.text_input("Bande ka Naam:", "Rajput Sahab")

# Load Background
try:
    bg_img = Image.open("background.png").convert("RGBA")
except:
    st.error("Pehle 'background.png' upload karein!")
    st.stop()

# Upload Photo
st.warning("Note: Style cutting ke liye 'Background Removed' (PNG) photo upload karein.")
uploaded_file = st.file_uploader("Gallery se photo uthayein", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    user_img = Image.open(uploaded_file).convert("RGBA")
    
    # Resize (Muslim Bhai Style Frame)
    user_img = user_img.resize((480, 580)) 

    # Positioning
    if mode == "Single Person":
        bg_img.paste(user_img, (530, 230), user_img)
    else:
        bg_img.paste(user_img, (400, 230), user_img)

    st.image(bg_img, use_column_width=True)

    # Download
    buf = io.BytesIO()
    bg_img.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", data=buf.getvalue(), file_name="election_flex.png")
