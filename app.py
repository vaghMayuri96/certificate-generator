import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import io

st.title("🎓 Certificate Generator App")

st.markdown("""
Upload your certificate background image and a CSV file with a 'Name' column.
You can preview and download personalized certificates as images!
""")

# 1. Upload background image
bg_file = st.file_uploader("Upload certificate background (JPG/PNG)", type=["jpg", "jpeg", "png"])

# 2. Upload CSV file
csv_file = st.file_uploader("Upload names CSV (must have 'Name' column)", type=["csv"])

# 3. Text settings
font_size = st.number_input("Name Font Size", min_value=20, max_value=200, value=60)
font_color = st.color_picker("Name Color", "#000080")
x_pos = st.number_input("Name X Position (px)", min_value=0, value=300)
y_pos = st.number_input("Name Y Position (px)", min_value=0, value=350)
sample_name = st.text_input("Preview name", "Aman Singh")

# 4. (Optional) Font selection
font_file = st.file_uploader("Upload a .ttf font for names (optional, e.g. cursive)", type=["ttf"])
if font_file:
    font_bytes = io.BytesIO(font_file.read())
    font = ImageFont.truetype(font_bytes, font_size)
else:
    font = ImageFont.load_default()

# Preview
if bg_file:
    img = Image.open(bg_file).convert("RGB")
    img_w, img_h = img.size

    # Draw sample name for preview
    preview = img.copy()
    draw = ImageDraw.Draw(preview)
    draw.text((x_pos, y_pos), sample_name, font=font, fill=font_color)
    st.image(preview, caption="Certificate Preview", use_column_width=True)

    # If CSV is uploaded, show names and allow download
    if csv_file:
        df = pd.read_csv(csv_file)
        st.write("First few names:", df.head())

        if st.button("Generate and Download Certificates (ZIP)"):
            import zipfile

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "a") as zipf:
                for idx, row in df.iterrows():
                    cert_img = img.copy()
                    draw = ImageDraw.Draw(cert_img)
                    name = str(row["Name"])
                    draw.text((x_pos, y_pos), name, font=font, fill=font_color)
                    img_byte_arr = io.BytesIO()
                    cert_img.save(img_byte_arr, format='PNG')
                    zipf.writestr(f"certificate_{name.replace(' ', '_')}.png", img_byte_arr.getvalue())
            zip_buffer.seek(0)
            st.success("Done! Download your certificates below:")
            st.download_button("Download All Certificates (ZIP)", data=zip_buffer, file_name="certificates.zip")

else:
    st.info("Upload a certificate background image to get started.")

