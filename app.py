import streamlit as st
from PIL import Image
from rembg import remove
import io
import os

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Professional Flex", layout="wide")

st.title("🗳️ Rajput Election Flex Maker")

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Error: GitHub par 'background.png' nahi mili!")
    st.stop()

# 2. Sidebar Positions (Jo aapne boxes bataye thay)
st.sidebar.header("Doston ki Jagah")
p1 = (st.sidebar.slider("Box 1 (Right) L-R", 0, W, 500), st.sidebar.slider("Box 1 U-D", 0, H, 150))
p2 = (st.sidebar.slider("Box 2 (Far Right) L-R", 0, W, 750), st.sidebar.slider("Box 2 U-D", 0, H, 150))
p3 = (st.sidebar.slider("Box 3 (Bottom Right) L-R", 0, W, 750), st.sidebar.slider("Box 3 U-D", 0, H, 450))

# 3. Uploaders
f1 = st.file_uploader("Pehli Photo (Box 1)", type=["jpg","png","jpeg"], key="b1")
f2 = st.file_uploader("Doosri Photo (Box 2)", type=["jpg","png","jpeg"], key="b2")
f3 = st.file_uploader("Teesri Photo (Box 3)", type=["jpg","png","jpeg"], key="b3")

if st.button("Final Flex Banayein 🚀"):
    final_flex = bg_img.copy()
    files = [f1, f2, f3]
    all_pos = [p1, p2, p3]
    
    for i, f in enumerate(files):
        if f:
            with st.spinner(f"Photo {i+1} ki cutting ho rahi hai..."):
                img = Image.open(f)
                # Pure AI Cutting (Matting True taake edges saaf hon)
                cut = remove(img, alpha_matting=True)
                # Solid Resize (No Fading)
                cut = cut.resize((380, 500))
                # Paste directly on background
                final_flex.paste(cut, all_pos[i], cut)
    
    st.image(final_flex, use_column_width=True)
    
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", buf.getvalue(), "rajput_flex.png")
