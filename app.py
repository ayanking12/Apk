import streamlit as st
from PIL import Image
from rembg import remove
import io
import os
import numpy as np

os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Unlimited Flex", layout="wide")

st.title("🗳️ Unlimited Group Flex Maker")
st.write("Jitne marzi doston ki photos upload karein, AI sab ko grid mein set kar dega.")

# --- Function: Muslim Bhai Style Blend ---
def apply_style_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    fade_start = int(height * 0.6)
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha[y, :] = np.minimum(alpha[y, :], mask_value)
    img.putalpha(Image.fromarray(alpha))
    return img

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: GitHub par 'background.png' upload karein!")
    st.stop()

# 2. Sidebar Controls
st.sidebar.header("Layout Settings")
pp_row = st.sidebar.slider("Ek line mein kitne bande hon?", 2, 10, 4)
top_margin = st.sidebar.slider("Upar se kitni jagah chorna?", 0, H, 200)
left_margin = st.sidebar.slider("Side se kitni jagah chorna?", 0, W, 50)
person_scale = st.sidebar.slider("Bandon ka size (%)", 10, 100, 30)

# 3. Unlimited File Uploader
uploaded_files = st.file_uploader("Sab doston ki photos ek sath select karke upload karein", 
                                  type=["jpg","png","jpeg"], 
                                  accept_multiple_files=True)

if st.button("Unlimited Flex Banayein 🚀"):
    if not uploaded_files:
        st.warning("Pehle kuch photos to upload karein jani!")
    else:
        final_flex = bg_img.copy()
        
        # Calculate Sizes
        max_person_w = int((W - (left_margin * 2)) / pp_row)
        person_w = int(max_person_w * (person_scale / 100))
        person_h = int(person_w * 1.3) # Maintain decent height
        
        current_x = left_margin
        current_y = top_margin
        count = 0

        progress_bar = st.progress(0)
        
        for i, f in enumerate(uploaded_files):
            with st.spinner(f"Banda {i+1} process ho raha hai..."):
                img = Image.open(f)
                # AI Cut
                cut = remove(img, alpha_matting=True)
                # Aspect Ratio Resize
                aspect = cut.width / cut.height
                new_h = person_h
                new_w = int(new_h * aspect)
                cut = cut.resize((new_w, new_h))
                # Fade
                styled_img = apply_style_fade(cut)
                
                # Paste
                final_flex.paste(styled_img, (current_x, current_y), styled_img)
                
                # Update Coordinates for next person
                count += 1
                if count >= pp_row:
                    count = 0
                    current_x = left_margin
                    current_y += (person_h - 50) # Thoda oopar charha kar (overlap)
                else:
                    current_x += max_person_w
            
            progress_bar.progress((i + 1) / len(uploaded_files))

        st.image(final_flex, use_column_width=True)
        
        buf = io.BytesIO()
        final_flex.save(buf, format="PNG")
        st.download_button("📥 Full Group Flex Download", buf.getvalue(), "rajput_unlimited_flex.png")
