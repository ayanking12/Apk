import streamlit as st
from PIL import Image
from rembg import remove
import io
import os
import numpy as np

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Final Flex Pro", layout="wide")

st.title("🗳️ Rajput Election Flex Maker (Chehre Fix)")
st.write("Doston ki photos upload karein, ab chehre apni asli shakal mein fit hon gay, lambay nahi hon gay.")

# --- Function to Fade Bottom and Blend (Muslim Bhai Style) ---
def apply_style_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    
    # Neechay se 35% blend
    fade_start = int(height * 0.65)
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha[y, :] = np.minimum(alpha[y, :], mask_value)
        
    img.putalpha(Image.fromarray(alpha))
    return img

# --- Function to Maintain Aspect Ratio while Fitting into a Box ---
# This fixes the "long face" issue
def resize_contain(img, max_w, max_h):
    orig_w, orig_h = img.size
    orig_aspect = orig_w / orig_h
    box_aspect = max_w / max_h
    
    # Calculate new size while maintaining original aspect ratio
    if orig_aspect > box_aspect:
        # Too wide, fit to width
        new_w = max_w
        new_h = int(new_w / orig_aspect)
    else:
        # Too tall, fit to height
        new_h = max_h
        new_w = int(new_h * orig_aspect)
        
    return img.resize((new_w, new_h))

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: GitHub par 'background.png' nahi mili!")
    st.stop()

# 2. coordinates Fix (Percentages based - Previously confirmed correct)
# Box 1: (x=45%, y=15%), Box 2: (x=68%, y=15%), Box 3: (x=68%, y=46%)
pos1 = (int(W * 0.45), int(H * 0.15))
pos2 = (int(W * 0.68), int(H * 0.15))
pos3 = (int(W * 0.68), int(H * 0.46))

# Define max box sizes for containing images without stretching
box1_max = (int(W * 0.30), int(H * 0.38)) # Smaller box size constraint
box3_max = (int(W * 0.32), int(H * 0.45)) # Taller box size constraint

box_constraints = [box1_max, box1_max, box3_max]

# 3. Uploaders
cols = st.columns(3)
files = []
for i in range(3):
    with cols[i]:
        f = st.file_uploader(f"Dabba {i+1} ki Photo", type=["jpg","png","jpeg"], key=f"user_{i}")
        files.append(f)

if st.button("Asli Shakal mein Flex Banayein 🚀"):
    final_flex = bg_img.copy()
    
    uploaded_files = [f for f in files if f is not None]
    # Filter constraints to match uploaded file count
    current_constraints = box_constraints[:len(uploaded_files)]
    
    for i, f in enumerate(uploaded_files):
        with st.spinner(f"Photo {i+1} set ho rahi hai..."):
            img = Image.open(f)
            
            # Step 1: AI Auto-Cut
            cut = remove(img, alpha_matting=True)
            
            # Step 2: Fit into box without stretching (fixes long faces)
            box_w, box_h = current_constraints[i]
            styled_img = resize_contain(cut, box_w, box_h)
            
            # Step 3: Fade Bottom and Blend
            styled_img = apply_style_fade(styled_img)
            
            # Step 4: Paste
            # Define pasting coordinates (adjust for centering if needed, but let's stick to base confirmed)
            positions = [pos1, pos2, pos3][:len(uploaded_files)]
            final_flex.paste(styled_img, positions[i], styled_img)
    
    # Result
    st.image(final_flex, use_column_width=True)
    
    # Download
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", buf.getvalue(), "rajput_chehre_fix_flex.png")
