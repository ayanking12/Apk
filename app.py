import streamlit as st
from PIL import Image
from rembg import remove
from streamlit_cropper import st_cropper
import io
import os

os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Visual Flex", layout="wide")

st.title("🗳️ Ungli se Photo Set Karein (Visual Mode)")

# 1. Background Load
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: background.png nahi mili!")
    st.stop()

# 2. Photo Uploader
f = st.file_uploader("Apni Photo Upload Karein", type=["jpg","png","jpeg"])

if f:
    # Processing
    with st.spinner("AI Cutting ho rahi hai..."):
        img = Image.open(f)
        cut = remove(img)
    
    st.write("---")
    st.subheader("👆 Poster par ungli se dabba hila kar jagah set karein")
    
    # Visual Box Selection (Cropper)
    # Is dabbe ko aap ungli se hila sakte hain poster ke oopar
    rect = st_cropper(bg_img, realtime_update=True, box_color='#FF0000', aspect_ratio=None)
    
    # Calculate Coordinates from Box
    # Ye khud hi "Lines" ka hisab laga lega
    x = st.session_state.get('cropper_res', {}).get('left', 400)
    y = st.session_state.get('cropper_res', {}).get('top', 200)
    w = st.session_state.get('cropper_res', {}).get('width', 300)
    h = st.session_state.get('cropper_res', {}).get('height', 400)

    if st.button("✅ Is Jagah Par Photo Set Karein"):
        final_flex = bg_img.copy()
        
        # Photo ko dabbe ke size ke mutabiq resize karna
        resized_cut = cut.resize((int(w), int(h)))
        
        # Paste
        final_flex.paste(resized_cut, (int(x), int(y)), resized_cut)
        
        st.image(final_flex, caption="Aapka Result", use_column_width=True)
        
        # Download
        buf = io.BytesIO()
        final_flex.save(buf, format="PNG")
        st.download_button("📥 Flex Download", buf.getvalue(), "flex.png")
