import streamlit as st
from PIL import Image
from rembg import remove
import io
import os
import numpy as np

os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Flex Pro", layout="wide")

# --- Photo ko neechay se dhundla (Fade) karne ka function ---
def apply_bottom_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    
    # Neechay se 50% hisse ko fade karna taake wo background mein mix ho jaye
    fade_start = int(height * 0.5)
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha[y, :] = np.minimum(alpha[y, :], mask_value)
        
    img.putalpha(Image.fromarray(alpha))
    return img

st.title("🗳️ Professional Flex Maker")

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: 'background.png' nahi mili!")
    st.stop()

# 2. Sidebar Sliders (Aapke Red Boxes wali jagah)
st.sidebar.header("Doston ki Jagah Set Karein")
p1_pos = (st.sidebar.slider("Banda 1: Left-Right", 0, W, 430), st.sidebar.slider("Banda 1: Up-Down", 0, H, 130))
p2_pos = (st.sidebar.slider("Banda 2: Left-Right", 0, W, 680), st.sidebar.slider("Banda 2: Up-Down", 0, H, 130))

# 3. Uploaders
f1 = st.file_uploader("Dabba 1 ki Photo", type=["jpg","png","jpeg"], key="b1")
f2 = st.file_uploader("Dabba 2 ki Photo", type=["jpg","png","jpeg"], key="b2")

if st.button("Final Flex Tayyar Karein 🚀"):
    # Pehle Background ko canvas banayein
    final_flex = bg_img.copy()
    
    files = [f1, f2]
    all_pos = [p1_pos, p2_pos]
    
    for i, f in enumerate(files):
        if f:
            with st.spinner(f"Banda {i+1} ki setting ho rahi hai..."):
                img = Image.open(f)
                cut = remove(img)
                # Size thoda chota rakha hai taake dabbo mein fit aaye
                cut = cut.resize((350, 450)) 
                # Fade effect lagana (Arrow wala style)
                styled_img = apply_bottom_fade(cut)
                # Ab ye photos Background ke OOPAR lagengi
                final_flex.paste(styled_img, all_pos[i], styled_img)
    
    st.image(final_flex, use_column_width=True)
    
    # Download
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", buf.getvalue(), "rajput_flex.png")
