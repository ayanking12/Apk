import streamlit as st
from PIL import Image, ImageOps
from rembg import remove
import io
import os
import numpy as np

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Final Flex Pro", layout="wide")

st.title("🗳️ Rajput Election Flex Maker")
st.write("Doston ki photos upload karein, AI khud unhein cut karke style mein set kar dega.")

# --- Function: Muslim Bhai Style Fade (Bottom Blend) ---
def apply_style_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    
    # Neechay se 35% hisse par dhundlapann (Gradient) taake blend ho jaye
    fade_start = int(height * 0.65) # 65% height ke baad fade shuru
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha[y, :] = np.minimum(alpha[y, :], mask_value)
        
    img.putalpha(Image.fromarray(alpha))
    return img

# 1. Background Load (Jo user ne confirm kiya hai ke positions sahi hain)
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: GitHub par 'background.png' nahi mili!")
    st.stop()

# 2. Coordinates Fix (User Confirmed)
# Box 1: (x=45%, y=15%), Box 2: (x=68%, y=15%), Box 3: (x=68%, y=46%)
pos1 = (int(W * 0.45), int(H * 0.15))
pos2 = (int(W * 0.68), int(H * 0.15))
pos3 = (int(W * 0.68), int(H * 0.46))

# 3. Uploaders
cols = st.columns(3)
files = []
for i in range(3):
    with cols[i]:
        f = st.file_uploader(f"Dabba {i+1} ki Photo", type=["jpg","png","jpeg"], key=f"user_{i}")
        files.append(f)

if st.button("Final Solid Flex Banayein 🚀"):
    final_flex = bg_img.copy()
    
    uploaded_files = [f for f in files if f is not None]
    positions = [pos1, pos2, pos3][:len(uploaded_files)]
    
    for i, f in enumerate(uploaded_files):
        with st.spinner(f"Photo {i+1} ki style cutting ho rahi hai..."):
            img = Image.open(f)
            
            # Step 1: AI Auto-Cut (Crops subject automatically)
            cut = remove(img, alpha_matting=True) # Alpha matting for cleaner edges
            
            # Step 2: Resize (Dabbo ke mutabiq)
            cut_w = int(W * 0.32) # Thoda bara size taake style fit aaye
            cut_h = int(H * 0.40) # Thoda bara height taake neechay se fade ho
            cut = cut.resize((cut_w, cut_h))
            
            # Step 3: Muslim Bhai Style Fade (Neechay se blend karna)
            styled_img = apply_style_fade(cut)
            
            # Step 4: Paste solid image with blended bottom
            final_flex.paste(styled_img, positions[i], styled_img)
    
    # Result
    st.image(final_flex, use_column_width=True)
    
    # Download
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", buf.getvalue(), "rajput_styled_flex.png")
