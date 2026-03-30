import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import io
import os

# AI Engine ko CPU par set karne ke liye
os.environ["ONNXRUNTIME_BACKEND"] = "cpu"

# Page Setup
st.set_page_config(page_title="Rajput 5-Person Flex Pro", layout="wide")

st.title("🗳️ Multi-Person Style Flex (Names & Positions)")
st.write("Doston ki photos upload karein, naam likhein aur sliders se jagah set karein.")

# Load Background
try:
    bg_img = Image.open("background.png").convert("RGBA")
    W, H = bg_img.size
except:
    st.error("Pehle 'background.png' upload karein!")
    st.stop()

# --- SIDEBAR: Positioning & Names ---
st.sidebar.header("Doston ki Details")

def person_controls(label, def_x, def_y):
    with st.sidebar.expander(f"⚙️ {label} Settings"):
        name = st.text_input(f"{label} ka Naam:", f"Rajput {label[-1]}")
        x = st.slider(f"{label} (Left-Right)", 0, W, def_x)
        y = st.slider(f"{label} (Up-Down)", 0, H, def_y)
        color = st.color_picker(f"{label} Naam ka Rang", "#FFCC00")
    return name, (x, y), color

# 5 doston ke controls
n1, p1, c1 = person_controls("Banda 1", 530, 230)
n2, p2, c2 = person_controls("Banda 2", 350, 250)
n3, p3, c3 = person_controls("Banda 3", 180, 280)
n4, p4, c4 = person_controls("Banda 4", 720, 300)
n5, p5, c5 = person_controls("Banda 5", 50, 320)

names = [n1, n2, n3, n4, n5]
positions = [p1, p2, p3, p4, p5]
colors = [c1, c2, c3, c4, c5]

# --- MAIN INTERFACE: Uploaders ---
cols = st.columns(5)
uploaded_files = []
for i in range(5):
    with cols[i]:
        f = st.file_uploader(f"Banda {i+1} Photo", type=["jpg","png","jpeg"], key=f"u_{i}")
        uploaded_files.append(f)

if st.button("Flex Banayein (AI Process) 🚀"):
    final_flex = bg_img.copy()
    draw = ImageDraw.Draw(final_flex)
    
    # Koshish karein ke default font use ho, varna Urdu font upload karna hoga
    try:
        font = ImageFont.load_default()
    except:
        font = None

    progress_bar = st.progress(0)
    
    for i, uploaded_file in enumerate(uploaded_files):
        if uploaded_file is not None:
            with st.spinner(f"Banda {i+1} ki cutting ho rahi hai..."):
                img = Image.open(uploaded_file)
                # AI Style Cutting
                cut_img = remove(img)
                
                # Resize
                size = (450, 550) if i == 0 else (380, 480)
                cut_img = cut_img.resize(size)
                
                # Paste Image
                final_flex.paste(cut_img, positions[i], cut_img)
                
                # Draw Name (Photo ke thoda niche)
                name_x, name_y = positions[i]
                draw.text((name_x + 50, name_y + 450), names[i], fill=colors[i], font=font)
        
        progress_bar.progress((i + 1) / 5)

    st.image(final_flex, use_column_width=True)

    # Download
    buf = io.BytesIO()
    final_flex.save(buf, format="PNG")
    st.download_button("📥 Flex Download Karein", data=buf.getvalue(), file_name="rajput_final_flex.png")
