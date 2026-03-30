import streamlit as st
from PIL import Image
from rembg import remove
import io
import os
import numpy as np

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Professional Flex", layout="wide")

# --- Fade Function (Isay kam kiya hai taake pic saaf dikhe) ---
def apply_style_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    # Sirf neche se 20% fade (Halka sa mix karne ke liye)
    fade_start = int(height * 0.8)
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha[y, :] = np.minimum(alpha[y, :], mask_value)
    img.putalpha(Image.fromarray(alpha))
    return img

st.title("🗳️ Professional 5-Person Flex Maker")

try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: 'background.png' nahi mili!")
    st.stop()

# --- 5 Doston ki Positions (Aapke Boxes ke mutabiq) ---
st.sidebar.header("Photos ki Setting")
# Aap in numbers ko sliders se mazeed set kar sakte hain
p1 = (st.sidebar.slider("Box 1: L-R", 0, W, 450), st.sidebar.slider("Box 1: U-D", 0, H, 150))
p2 = (st.sidebar.slider("Box 2: L-R", 0, W, 700), st.sidebar.slider("Box 2: U-D", 0, H, 150))
p3 = (st.sidebar.slider("Box 3: L-R", 0, W, 700), st.sidebar.slider("Box 3: U-D", 0, H, 450))
p4 = (st.sidebar.slider("Box 4: L-R", 0, W, 200), st.sidebar.slider("Box 4: U-D", 0, H, 300))
p5 = (st.sidebar.slider("Box 5: L-R", 0, W, 50), st.sidebar.slider("Box 5: U-D", 0, H, 450))

all_pos = [p1, p2, p3, p4, p5]

# Uploaders
cols = st.columns(5)
files = []
for i in range(5):
    with cols[i]:
        f = st.file_uploader(f"Banda {i+1}", type=["jpg","png","jpeg"], key=f"user_{i}")
        files.append(f)

if st.button("Final Flex Banayein 🚀"):
    final_flex = bg_img.copy()
    
    for i, f in enumerate(files):
        if f:
            with st.spinner(f"Banda {i+1} ki Cutting ho rahi hai..."):
                img = Image.open(f)
                # 1. AI Auto-Cut
                cut = remove(img)
                # 2. Resize
                cut = cut.resize((380, 500)) 
                # 3. Fade Effect
                styled_img = apply_style_fade(cut)
                # 4. Paste
                final_flex.paste(styled_img, all_pos[i], styled_img)
    
    st.image(final_flex, use_column_width=True)
    
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download", buf.getvalue(), "final_rajput_flex.png")
