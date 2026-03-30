import streamlit as st
from PIL import Image
from rembg import remove
import io

# Page Setup
st.set_page_config(page_title="Rajput 5-Person Flex", layout="centered")

st.title("🗳️ Multi-Person Style Flex")
st.write("Ek ek karke 5 doston ki photos upload karein. AI sab ko sahi jagah set kar dega.")

# Load Background
try:
    bg_img = Image.open("background.png").convert("RGBA")
except:
    st.error("Pehle 'background.png' upload karein!")
    st.stop()

# 5 Photos ke liye Uploaders
col1, col2 = st.columns(2)
files = []
with col1:
    f1 = st.file_uploader("Pehla Banda (Main)", type=["jpg","png","jpeg"], key="1")
    f2 = st.file_uploader("Doosra Banda", type=["jpg","png","jpeg"], key="2")
    f3 = st.file_uploader("Teesra Banda", type=["jpg","png","jpeg"], key="3")
with col2:
    f4 = st.file_uploader("Chotha Banda", type=["jpg","png","jpeg"], key="4")
    f5 = st.file_uploader("Paanchwan Banda", type=["jpg","png","jpeg"], key="5")

uploaded_files = [f1, f2, f3, f4, f5]

if st.button("Flex Banayein 🚀"):
    final_flex = bg_img.copy()
    
    # X aur Y Coordinates (Aap inhe thoda change kar sakte hain)
    # Format: (X-axis, Y-axis)
    positions = [
        (530, 230), # Banda 1 (Right Side - Main)
        (350, 250), # Banda 2 (Center-Right)
        (180, 280), # Banda 3 (Center-Left)
        (720, 300), # Banda 4 (Far Right)
        (50, 320)   # Banda 5 (Far Left)
    ]

    progress_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        if uploaded_file is not None:
            with st.status(f"Banda {i+1} ki cutting ho rahi hai...", expanded=False):
                img = Image.open(uploaded_file)
                # AI Style Cutting
                cut_img = remove(img)
                # Size adjustment (Piche wale bande thode chote)
                size = (400, 500) if i == 0 else (350, 450)
                cut_img = cut_img.resize(size)
                
                # Paste on specific position
                final_flex.paste(cut_img, positions[i], cut_img)
        
        progress_bar.progress((i + 1) / 5)

    st.image(final_flex, use_column_width=True)

    # Download
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Final Flex Download", data=buf.getvalue(), file_name="rajput_group_flex.png")
