import streamlit as st
from PIL import Image
from rembg import remove
import io

st.set_page_config(page_title="Rajput Multi-Flex", layout="wide")

st.title("🗳️ Multi-Person Flex Maker")
st.write("4-5 doston ki photos upload karein, AI sab ko style mein cut kar dega.")

# Requirements check for rembg
# Yaad rakhein requirements.txt mein 'rembg' dubara add karna hoga

try:
    bg_img = Image.open("background.png").convert("RGBA")
except:
    st.error("Background image nahi mili!")
    st.stop()

# Upload Multiple Files
uploaded_files = st.file_uploader("4 se 5 Photos select karein", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    if len(uploaded_files) > 5:
        st.warning("Sirf 5 log tak allow hain.")
        uploaded_files = uploaded_files[:5]

    with st.spinner('Sab doston ki cutting ho rahi hai...'):
        # Initial Position (X, Y) - Aap ise adjust kar sakte hain
        positions = [(550, 230), (350, 230), (750, 230), (150, 300), (950, 300)]
        
        for i, file in enumerate(uploaded_files):
            img = Image.open(file)
            # AI Auto-Cut
            cut_img = remove(img)
            # Resize
            cut_img = cut_img.resize((350, 450)) # Thoda chota resize taake 5 log purey ayein
            
            # Paste on Background
            bg_img.paste(cut_img, positions[i], cut_img)

    st.image(bg_img, use_column_width=True)
    
    # Download
    buf = io.BytesIO()
    bg_img.save(buf, format="PNG")
    st.download_button("📥 Final Flex Download", data=buf.getvalue(), file_name="multi_flex.png")
