import streamlit as st
from PIL import Image
from rembg import remove
import io
import os
import numpy as np

os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Unlimited Flex", layout="wide")

# Session state: Yahan hum doston ka data save rakhenge
if 'final_poster' not in st.session_state:
    st.session_state.final_poster = None
if 'history' not in st.session_state:
    st.session_state.history = []

def apply_style_fade(img):
    img = img.convert("RGBA")
    width, height = img.size
    alpha = np.array(img.split()[-1])
    fade_start = int(height * 0.7)
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha[y, :] = np.minimum(alpha[y, :], mask_value)
    img.putalpha(Image.fromarray(alpha))
    return img

st.title("🗳️ Professional Unlimited Flex Maker")

# 1. Background Load
try:
    bg_raw = Image.open("background.png").convert("RGBA")
    W, H = bg_raw.size
    if st.session_state.final_poster is None:
        st.session_state.final_poster = bg_raw.copy()
except:
    st.error("GitHub par 'background.png' nahi mili!")
    st.stop()

# --- Sidebar: Control Panel ---
st.sidebar.header("⚙️ Setting & Control")

# Reset Button
if st.sidebar.button("Pura Poster Saaf Karein (Reset)"):
    st.session_state.final_poster = bg_raw.copy()
    st.session_state.history = []
    st.experimental_rerun()

st.sidebar.write("---")
f = st.sidebar.file_uploader("Naya Banda Add Karein", type=["jpg","png","jpeg"])

if f:
    # 1. Image Processing
    img = Image.open(f)
    with st.spinner("AI Cutting..."):
        cut = remove(img)
        styled_img = apply_style_fade(cut)
    
    st.sidebar.success("Banda Ready hai! Neeche se adjust karein.")
    
    # 2. Manual Sliders (Ungli se control ke liye)
    st.subheader("Bande ki Jagah aur Size Set Karein")
    col1, col2, col3 = st.columns(3)
    with col1:
        x_pos = st.slider("Daayen-Baayen (X)", 0, W, int(W/2))
    with col2:
        y_pos = st.slider("Upar-Neeche (Y)", 0, H, int(H/3))
    with col3:
        size = st.slider("Chota-Bada (Size)", 50, 1000, 350)

    # Preview logic
    preview_img = st.session_state.final_poster.copy()
    temp_cut = styled_img.copy()
    
    # Aspect Ratio Maintain
    aspect = temp_cut.width / temp_cut.height
    new_w = size
    new_h = int(new_w / aspect)
    temp_cut = temp_cut.resize((new_w, new_h))
    
    preview_img.paste(temp_cut, (x_pos, y_pos), temp_cut)
    st.image(preview_img, caption="Preview: Isko check karein", use_column_width=True)

    if st.button("✅ Is Bande ko Fix (Save) Karein"):
        st.session_state.final_poster = preview_img
        st.success("Banda poster mein add ho gaya! Ab agla banda upload karein.")
        st.experimental_rerun()

else:
    # Agar koi upload nahi hai to purana poster dikhayein
    st.subheader("Aapka Poster")
    st.image(st.session_state.final_poster, use_column_width=True)

# 3. Download Section
if st.session_state.final_poster:
    buf = io.BytesIO()
    st.session_state.final_poster.save(buf, format="PNG")
    st.sidebar.download_button("📥 Final Flex Download", buf.getvalue(), "rajput_final_flex.png")

