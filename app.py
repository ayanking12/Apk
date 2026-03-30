import streamlit as st
from PIL import Image, ImageDraw
from rembg import remove
from streamlit_cropper import st_cropper
import io
import os
import numpy as np

# AI Engine Fix
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Dynamic Flex Pro", layout="wide")

# Session state initialization
if 'placed_people' not in st.session_state:
    st.session_state.placed_people = [] # Each element: {'processed_img_bytes': BytesIO, 'x_percent': float, 'y_percent': float, 'w_percent': float, 'h_percent': float}

# --- Function: Muslim Bhai Style Blend (Fade) ---
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

st.title("🗳️ Professional Dynamic Group Flex Maker")
st.write("Doston ki photos bari bari daal kar professional Muslim Bhai style unlimited group poster banayein.")

# 1. Background Load
try:
    # background.png wo honi chahiye jisme Arslan Mani wali jagah khali hai
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Galti: GitHub par 'background.png' upload karein!")
    st.stop()

# --- Section "Add a New Person" ---
st.divider()
st.subheader("Banda Add Karein")
f_new = st.file_uploader("1 photo select karein", type=["jpg","png","jpeg"], key="new_u")

if f_new:
    with st.spinner("AI Auto-Cut aur Style ho rahi hai..."):
        # Process the new friend's photo
        img_raw = Image.open(f_new)
        # 1. AI Auto-Cut
        cut = remove(img_raw, alpha_matting=True)
        # 2. Muslim Bhai Style Blend (Fade)
        styled_cut = apply_style_fade(cut)
        # Store processed image bytes in state
        cut_bytes = io.BytesIO()
        styled_cut.save(cut_bytes, format="PNG")
        st.session_state.processed_img_bytes = cut_bytes

    # Show user the cut image for confirmation
    st.image(styled_cut, caption="AI cut ho gaya. Ab isey visually position karein.", use_column_width=False)
    
    # --- Visually position/size with streamlit-cropper ---
    st.write("---")
    st.subheader("Position aur Size Set Karein")
    st.info("Niche wale poster par **Selection Box** ko ungli se hila kar aur resize karke dost ki sahi jagah aur size set karein.")
    
    # Use cropper on a transparent overlay of the poster background
    # This allows visual positioning and sizing via percentages
    aspect_ratio = (1, 1) # Force square box selection, which can be resized.
    selection = st_cropper(bg_img, box_color='#FF0000', aspect_ratio=aspect_ratio, key="cropper")
    
    # Calculate percentages from selection coordinates
    real_x = selection['left']
    real_y = selection['top']
    real_w = selection['width']
    real_h = selection['height']
    
    x_percent = real_x / W
    y_percent = real_y / H
    w_percent = real_w / W
    h_percent = real_h / H
    
    # Button to confirm placement
    if st.button("Is Bande ko Place Karein"):
        # Save placement data to state
        new_person_data = {
            'processed_img_bytes': st.session_state.processed_img_bytes,
            'x_percent': x_percent,
            'y_percent': y_percent,
            'w_percent': w_percent,
            'h_percent': h_percent
        }
        st.session_state.placed_people.append(new_person_data)
        
        # Clear temporary processed image bytes and raw file uploader
        del st.session_state.processed_img_bytes
        st.experimental_rerun() # Force re-render to clear added components and update poster

# --- Section "Your Poster so far" ---
st.divider()
st.subheader("Aapka Poster")
if not st.session_state.placed_people:
    st.warning("Abhi tak koi dost place nahi kiya.")
else:
    # Sequentially generate the final poster image from state data
    final_flex = bg_img.copy()
    
    for i, person in enumerate(st.session_state.placed_people):
        # Convert processed bytes back to PIL Image
        processed_img = Image.open(person['processed_img_bytes']).convert("RGBA")
        
        # Calculate pixel-based coordinates from percentages
        p_x = int(W * person['x_percent'])
        p_y = int(H * person['y_percent'])
        p_w = int(W * person['w_percent'])
        p_h = int(H * person['h_percent'])
        
        # Resize friend's image to selected size (Maintain original aspect ratio, no stretching)
        # We don't need resize_contain here as we already know the target width/height
        resized_img = processed_img.resize((p_w, p_h))
        
        # Paste sequentially to build the final poster
        final_flex.paste(resized_img, (p_x, p_y), resized_img)
        
    st.image(final_flex, use_column_width=True, caption="Aapka Dynamic unlimited people poster.")

    # --- Section "Generate Final Poster" ---
    st.divider()
    st.subheader("Download Final Flex")
    if st.button("Final Flex Download Link"):
        # Final sequential generation for download
        final_output = bg_img.copy()
        for person in st.session_state.placed_people:
            processed_img = Image.open(person['processed_img_bytes']).convert("RGBA")
            p_w = int(W * person['w_percent'])
            p_h = int(H * person['h_percent'])
            resized_img = processed_img.resize((p_w, p_h))
            final_output.paste(resized_img, (int(W * person['x_percent']), int(H * person['y_percent'])), resized_img)
        
        buf = io.BytesIO()
        final_output.save(buf, format="PNG")
        st.download_button("📥 Dynamic Flex Download", buf.getvalue(), "dynamic_rajput_flex.png")
