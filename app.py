import streamlit as st
from PIL import Image
from rembg import remove
import io
import os

os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Professional Flex", layout="wide")

st.title("🗳️ Rajput Flex - Manual Positioning")

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: GitHub par 'background.png' nahi mili!")
    st.stop()

# 2. Uploaders (Sirf 3 Box abhi taake asaan rahe)
cols = st.columns(3)
with cols[0]:
    f1 = st.file_uploader("Box 1 ki Photo", type=["jpg","png","jpeg"], key="b1")
    # Slider for Box 1
    x1 = st.slider("Box 1: Daayen-Baayen", 0, W, 450)
    y1 = st.slider("Box 1: Upar-Neeche", 0, H, 100)
    s1 = st.slider("Box 1 ka Size", 100, 800, 350)

with cols[1]:
    f2 = st.file_uploader("Box 2 ki Photo", type=["jpg","png","jpeg"], key="b2")
    x2 = st.slider("Box 2: Daayen-Baayen", 0, W, 700)
    y2 = st.slider("Box 2: Upar-Neeche", 0, H, 100)
    s2 = st.slider("Box 2 ka Size", 100, 800, 350)

with cols[2]:
    f3 = st.file_uploader("Box 3 ki Photo", type=["jpg","png","jpeg"], key="b3")
    x3 = st.slider("Box 3: Daayen-Baayen", 0, W, 700)
    y3 = st.slider("Box 3: Upar-Neeche", 0, H, 450)
    s3 = st.slider("Box 3 ka Size", 100, 800, 350)

if st.button("Final Flex Banayein 🚀"):
    final_flex = bg_img.copy()
    
    # Processing Photos
    data = [(f1, x1, y1, s1), (f2, x2, y2, s2), (f3, x3, y3, s3)]
    
    for i, (f, x, y, s) in enumerate(data):
        if f:
            with st.spinner(f"Photo {i+1} set ho rahi hai..."):
                img = Image.open(f)
                cut = remove(img)
                # Aspect ratio barkarar rakhne ke liye
                w_ratio = s / float(cut.size[0])
                h_size = int(float(cut.size[1]) * float(w_ratio))
                cut = cut.resize((s, h_size))
                # Paste
                final_flex.paste(cut, (x, y), cut)
    
    st.image(final_flex, use_column_width=True)
    
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download", buf.getvalue(), "flex.png")
