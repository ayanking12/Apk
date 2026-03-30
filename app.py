import streamlit as st
from PIL import Image
from rembg import remove
import io
import os
import numpy as np

# AI Engine Setup
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Professional Flex", layout="wide")

# --- Function: Photo ko Neechay se Fade (Dhundla) karne ke liye ---
def apply_bottom_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    
    # Neechay se 45% hisse par fade effect taake wo background mein mix ho jaye
    fade_start = int(height * 0.55)
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha[y, :] = np.minimum(alpha[y, :], mask_value)
        
    img.putalpha(Image.fromarray(alpha))
    return img

st.title("🗳️ Professional Layered Flex Maker")

# 1. Background Load
try:
    # background.png wo honi chahiye jisme Arslan Mani wali jagah khali hai
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Pehle 'background.png' upload karein!")
    st.stop()

# 2. Sidebar Sliders (Aapke Red Boxes ke mutabiq)
st.sidebar.header("Dabbo ki Positioning")
p1_pos = (st.sidebar.slider("Dabba 1 (Left-Right)", 0, W, 430), st.sidebar.slider("Dabba 1 (Up-Down)", 0, H, 130))
p2_pos = (st.sidebar.slider("Dabba 2 (Left-Right)", 0, W, 680), st.sidebar.slider("Dabba 2 (Up-Down)", 0, H, 130))
p3_pos = (st.sidebar.slider("Dabba 3 (Left-Right)", 0, W, 700), st.sidebar.slider("Dabba 3 (Up-Down)", 0, H, 480))

# 3. Photo Uploaders
cols = st.columns(3)
files = []
for i in range(3):
    with cols[i]:
        f = st.file_uploader(f"Dabba {i+1} ki Photo", type=["jpg","png","jpeg"], key=f"box_{i}")
        files.append(f)

if st.button("Final Flex Tayyar Karein 🚀"):
    # Pehle ek Khali Transparent Canvas banayein
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    all_pos = [p1_pos, p2_pos, p3_pos]
    
    for i, f in enumerate(files):
        if f:
            with st.spinner(f"Banda {i+1} process ho raha hai..."):
                img = Image.open(f)
                # AI Auto-Cut
                cut = remove(img)
                # Resize (Dabbo ke size ke mutabiq)
                cut = cut.resize((420, 550)) 
                # Neechay se fade effect
                styled_img = apply_bottom_fade(cut)
                # Canvas par paste karein
                canvas.paste(styled_img, all_pos[i], styled_img)
    
    # --- Sab se Aham Step: Background ko Oopar Rakhna ---
    # Isse naye doston ki photos aapke design (Muslim Bhai) ke PEECHAY nazar aayengi
    final_flex = Image.alpha_composite(canvas, bg_img)
    
    st.image(final_flex, use_column_width=True)
    
    # Download
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", buf.getvalue(), "professional_flex.png")
