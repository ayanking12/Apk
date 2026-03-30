import streamlit as st
from PIL import Image, ImageFilter
from rembg import remove
import io
import os
import numpy as np

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput HD Photo Blender", layout="centered")

st.title("✂️ HD AI Photo Blender (No Pixel Burst)")
st.write("HD photo upload karein, AI iska background saaf karega aur kinare soft karega, jab ke size bara hi rahega.")

# --- Function: Edges aur Bottom ko Fade (Soft) karna (No Resize inside) ---
def make_soft_edges(img):
    img = img.convert("RGBA")
    width, height = img.size
    
    # 1. Kinaro ko soft karna (Feathering) - Radius 3 for subtlety in HD
    alpha = img.split()[-1]
    alpha = alpha.filter(ImageFilter.GaussianBlur(radius=3))
    
    # 2. Neechay se 35% blend gradient
    alpha_data = np.array(alpha)
    fade_start = int(height * 0.65) # 65% ke baad fade
    
    for y in range(fade_start, height):
        mask_value = int(255 * (1 - (y - fade_start) / (height - fade_start)))
        alpha_data[y, :] = np.minimum(alpha_data[y, :], mask_value)
        
    # 3. Sides blend (line nikalne ke liye)
    side_fade = int(width * 0.08) # 8% sides
    for x in range(0, side_fade):
        mask_val = int(255 * (x / side_fade))
        alpha_data[:, x] = np.minimum(alpha_data[:, x], mask_val)
    for x in range(width - side_fade, width):
        mask_val = int(255 * (1 - (x - (width - side_fade)) / side_fade))
        alpha_data[:, x] = np.minimum(alpha_data[:, x], mask_val)

    new_alpha = Image.fromarray(alpha_data, mode='L')
    img.putalpha(new_alpha)
    return img

# --- Function: Enhanced HD Quality (Subtle Sharpening) ---
def enhance_hd_quality(img):
    img = img.convert("RGBA")
    # Apply subtle sharpening filter to enhance HD details
    enhanced_img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    return enhanced_img

# --- UI Section ---
uploaded_file = st.file_uploader("Apni HD Photo Select Karein", type=["jpg", "png", "jpeg"])

if uploaded_file:
    with st.spinner("AI cutting aur HD blending ho rahi hai..."):
        # Original Image load
        input_img = Image.open(uploaded_file)
        
        # Original dimensions save rakhenge
        orig_w, orig_h = input_img.size
        st.write(f"ℹ️ Original Photo Size: {orig_w} x {orig_h} pixels (Bara size barkarar rahega)")
        
        # 1. AI Background Removal (Alpha matting for hair details)
        cut_img = remove(input_img, alpha_matting=True)
        
        # 2. Soft Edges & Bottom Fade Apply (Maintain original resolution)
        styled_img = make_soft_edges(cut_img)
        
        # 3. HD Quality Enhancement
        final_hd_img = enhance_hd_quality(styled_img)
        
        st.success("Bande ki HD soft photo tayyar hai! Neeche download karein.")
        
        # Visual Preview - shows it smaller, but download is full size
        # Reassure user: preview might seem small, download is big
        st.warning("ℹ️ Preview mein photo choti lag sakti hai, lekin download bara milega.")
        st.image(final_hd_img, caption="Preview (Faded Bottom/Edges)", width=400) # Preview width fixed to 400 for viewability

        # 4. Download Button (Lossless PNG to keep HD quality)
        buf = io.BytesIO()
        final_hd_img.save(buf, format="PNG") # Always save as lossless PNG
        st.download_button(
            label="📥 Download HD Soft Photo (PNG)",
            data=buf.getvalue(),
            file_name="rajput_hd_soft_photo.png",
            mime="image/png"
        )

st.info("💡 Note: Ye tool photo ko bilkul chota nahi karta. Download hone wali photo ka size wahi rahega jo aapki original photo ka tha, pixel bilkul nahi phaten gay.")
