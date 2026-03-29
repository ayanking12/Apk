import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import io

# Page Setup
st.set_page_config(page_title="Rajput Flex Maker", layout="centered")

st.title("🗳️ Election Flex Maker")
st.write("Photo select karein, AI khud 'Muslim Bhai' style mein cut karke set kar dega.")

# Sidebar Settings
mode = st.sidebar.radio("Selection Mode:", ["Single Person", "Multiple People"])
user_name = st.sidebar.text_input("Bande ka Naam:", "Rajput Sahab")
text_col = st.sidebar.color_picker("Naam ka Rang", "#FFCC00")

# 1. Background Load (Jo aapne upload ki hogi)
try:
    bg_img = Image.open("background.png").convert("RGBA")
except:
    st.error("Pehle 'background.png' upload karein!")
    st.stop()

# 2. Upload Photo
uploaded_file = st.file_uploader("Gallery se photo uthayein...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    with st.spinner('AI Cutting ho rahi hai...'):
        input_image = Image.open(uploaded_file)
        # AI Background Removal
        output_image = remove(input_image)
        output_image = output_image.resize((480, 580)) 

        # Positioning
        if mode == "Single Person":
            bg_img.paste(output_image, (530, 230), output_image)
        else:
            bg_img.paste(output_image, (400, 230), output_image)

        # Draw Name
        draw = ImageDraw.Draw(bg_img)
        # Note: Urdu font ke liye font file upload karni hogi, varna default chalega
        draw.text((600, 800), user_name, fill=text_col)

        st.image(bg_img, use_column_width=True)

        # Download
        buf = io.BytesIO()
        bg_img.save(buf, format="PNG")
        st.download_button("📥 Flex Download Karein", data=buf.getvalue(), file_name="flex.png")
