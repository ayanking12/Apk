import streamlit as st
from PIL import Image
from rembg import remove
import io
import os

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Fix Flex", layout="wide")

st.title("🗳️ Rajput Election Flex (Fixed Boxes)")

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: GitHub par 'background.png' nahi mili!")
    st.stop()

# 2. Fixed Positions (Aapke Red Boxes ke exact coordinates)
# Box 1: Top Left center, Box 2: Top Right, Box 3: Bottom Right
fixed_positions = [
    (480, 150), # Box 1
    (730, 150), # Box 2
    (730, 520)  # Box 3
]

# 3. Uploaders
cols = st.columns(3)
files = []
for i in range(3):
    with cols[i]:
        f = st.file_uploader(f"Banda {i+1} Photo", type=["jpg","png","jpeg"], key=f"f_{i}")
        files.append(f)

if st.button("Final Flex Banayein 🚀"):
    final_flex = bg_img.copy()
    
    for i, f in enumerate(files):
        if f:
            with st.spinner(f"Photo {i+1} Set ho rahi hai..."):
                img = Image.open(f)
                # Pure AI Cut
                cut = remove(img)
                # Box ke mutabiq perfect size
                cut = cut.resize((350, 450))
                # Paste on fixed box location
                final_flex.paste(cut, fixed_positions[i], cut)
    
    st.image(final_flex, use_column_width=True)
    
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", buf.getvalue(), "rajput_fix_flex.png")
