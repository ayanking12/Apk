import streamlit as st
from PIL import Image
from rembg import remove
import io
import os

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Final Flex", layout="wide")

st.title("🗳️ Rajput Election Flex (Solid Fix)")

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: GitHub par 'background.png' nahi mili!")
    st.stop()

# 2. Coordinates Fix (Percentage based taake galti na ho)
# Box 1: (x=45%, y=15%), Box 2: (x=68%, y=15%), Box 3: (x=68%, y=46%)
pos1 = (int(W * 0.45), int(H * 0.15))
pos2 = (int(W * 0.68), int(H * 0.15))
pos3 = (int(W * 0.68), int(H * 0.46))

# 3. Uploaders
cols = st.columns(3)
f1 = cols[0].file_uploader("Box 1", type=["jpg","png","jpeg"], key="b1")
f2 = cols[1].file_uploader("Box 2", type=["jpg","png","jpeg"], key="b2")
f3 = cols[2].file_uploader("Box 3", type=["jpg","png","jpeg"], key="b3")

if st.button("Final Flex Tayyar Karein 🚀"):
    final_flex = bg_img.copy()
    
    files = [f1, f2, f3]
    positions = [pos1, pos2, pos3]
    
    for i, f in enumerate(files):
        if f:
            with st.spinner(f"Banda {i+1} set ho raha hai..."):
                img = Image.open(f)
                # Pure Solid AI Cutting
                cut = remove(img)
                # Size adjust (Dabbo ke mutabiq)
                cut_w = int(W * 0.28) # Width 28% of background
                cut_h = int(H * 0.35) # Height 35% of background
                cut = cut.resize((cut_w, cut_h))
                # Paste solid image
                final_flex.paste(cut, positions[i], cut)
    
    # Result
    st.image(final_flex, use_column_width=True)
    
    # Download
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", buf.getvalue(), "rajput_final.png")
