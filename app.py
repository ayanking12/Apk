import streamlit as st
from PIL import Image
from rembg import remove
import io
import os
import numpy as np

os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Huge Flex", layout="wide")

st.title("🗳️ Unlimited Group Flex (Big Size Mode)")

# --- Function: Muslim Bhai Style Blend ---
def apply_style_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    fade_start = int(height * 0.7) # 70% ke baad fade
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

# 2. Sidebar Controls (Powerful Sliders)
st.sidebar.header("Layout Settings")
pp_row = st.sidebar.slider("Ek line mein kitne bande hon?", 1, 10, 3) # Default 3 taake baray nazar aayein
top_margin = st.sidebar.slider("Upar se Neeche (Location)", 0, H, int(H*0.2)) 
left_margin = st.sidebar.slider("Side se Jagah", 0, W, 50)
# Size Slider ab 500 tak jayega
person_scale = st.sidebar.slider("Bandon ka Size (%)", 50, 500, 150) 
vertical_gap = st.sidebar.slider("Lines ke darmiyan gap", -200, 500, 100)

# 3. Unlimited File Uploader
uploaded_files = st.file_uploader("Sab doston ki photos upload karein", 
                                  type=["jpg","png","jpeg"], 
                                  accept_multiple_files=True)

if st.button("Final Flex Banayein 🚀"):
    if not uploaded_files:
        st.warning("Pehle photos upload karein!")
    else:
        final_flex = bg_img.copy()
        
        # Calculate Base Size
        # Jitne kam bande 'per row' hon gay, utne baray nazar aayein gay
        base_w = int((W / pp_row) * (person_scale / 100))
        
        current_x = left_margin
        current_y = top_margin
        count = 0

        progress_bar = st.progress(0)
        
        for i, f in enumerate(uploaded_files):
            with st.spinner(f"Banda {i+1} set ho raha hai..."):
                img = Image.open(f)
                cut = remove(img, alpha_matting=True)
                
                # Aspect Ratio Resize
                aspect = cut.width / cut.height
                new_w = base_w
                new_h = int(new_w / aspect)
                cut = cut.resize((new_w, new_h))
                
                # Muslim Bhai Fade
                styled_img = apply_style_fade(cut)
                
                # Paste
                final_flex.paste(styled_img, (current_x, current_y), styled_img)
                
                # Next Position logic
                count += 1
                if count >= pp_row:
                    count = 0
                    current_x = left_margin
                    current_y += (new_h + vertical_gap)
                else:
                    current_x += int(W / pp_row)
            
            progress_bar.progress((i + 1) / len(uploaded_files))

        st.image(final_flex, use_column_width=True)
        
        buf = io.BytesIO()
        final_flex.save(buf, format="PNG")
        st.download_button("📥 Flex Download", buf.getvalue(), "big_group_flex.png")
