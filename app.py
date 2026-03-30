import streamlit as st
from PIL import Image
from rembg import remove
import io
import os

# Ensuring the AI engine uses the CPU properly
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

st.set_page_config(page_title="Rajput Professional Flex", layout="wide")

st.title("🗳️ Professional 5-Person Flex Maker")

# 1. Load Background
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Error: 'background.png' not found on GitHub!")
    st.stop()

# 2. Sidebar Controls for Perfect Alignment
st.sidebar.header("Adjust Positions (If needed)")
# These defaults are set to match your Red Boxes
p1 = (st.sidebar.slider("Banda 1 (Box 1) L-R", 0, W, 480), st.sidebar.slider("Banda 1 (Box 1) U-D", 0, H, 100))
p2 = (st.sidebar.slider("Banda 2 (Box 2) L-R", 0, W, 720), st.sidebar.slider("Banda 2 (Box 2) U-D", 0, H, 100))
p3 = (st.sidebar.slider("Banda 3 (Box 3) L-R", 0, W, 720), st.sidebar.slider("Banda 3 (Box 3) U-D", 0, H, 400))
p4 = (st.sidebar.slider("Banda 4 (Left) L-R", 0, W, 100), st.sidebar.slider("Banda 4 (Left) U-D", 0, H, 300))
p5 = (st.sidebar.slider("Banda 5 (Bottom) L-R", 0, W, 400), st.sidebar.slider("Banda 5 (Bottom) U-D", 0, H, 500))

all_pos = [p1, p2, p3, p4, p5]

# 3. Photo Uploaders (Horizontal Layout)
cols = st.columns(5)
files = []
for i in range(5):
    with cols[i]:
        f = st.file_uploader(f"Banda {i+1}", type=["jpg","png","jpeg"], key=f"u_{i}")
        files.append(f)

if st.button("Final Flex Banayein 🚀"):
    # Start with a clean copy of the background
    final_flex = bg_img.copy()
    
    for i, f in enumerate(files):
        if f:
            with st.spinner(f"Processing Banda {i+1}..."):
                img = Image.open(f)
                
                # Step 1: High-Quality AI Cut
                # We use alpha_matting=True to make the edges cleaner
                cut = remove(img, alpha_matting=True) 
                
                # Step 2: Solid Resize (No heavy fading that makes them look like ghosts)
                # Box 1 and 2 are usually smaller, others larger
                if i < 2:
                    cut = cut.resize((320, 420))
                else:
                    cut = cut.resize((400, 520))
                
                # Step 3: Paste directly onto background
                final_flex.paste(cut, all_pos[i], cut)
    
    # Show the result
    st.image(final_flex, use_column_width=True)
    
    # Download Button
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Download Final Flex", buf.getvalue(), "rajput_election_flex.png")
