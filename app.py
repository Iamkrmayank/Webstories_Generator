import pandas as pd
import streamlit as st
import zipfile
import io

# Streamlit app title
st.title('Story Generator')

# File upload for Excel and HTML
uploaded_excel = st.file_uploader("Upload the Excel file (for replacements)", type="xlsx")
uploaded_html = st.file_uploader("Upload the HTML file", type="html")

# Proceed if both files are uploaded
if uploaded_excel and uploaded_html:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_excel, header=None)

    # Read the uploaded HTML file
    html_content_template = uploaded_html.read().decode('utf-8')

    # First row (index 0) contains placeholders like {{storytitle}}, {{coverinfo1}}, etc.
    placeholders = df.iloc[0, :].tolist()

    # Prepare an in-memory zip file to store all modified HTML files
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        # Loop through each row from index 1 onward to perform replacements
        for row_index in range(1, len(df)):
            actual_values = df.iloc[row_index, :].tolist()

            # Copy the original HTML template content
            html_content = html_content_template

            # Perform batch replacement for each placeholder in the row
            for placeholder, actual_value in zip(placeholders, actual_values):
                html_content = html_content.replace(placeholder, str(actual_value))

            # Create a unique filename for each modified HTML file
            output_filename = f"modified_template_row_{row_index}.html"

            # Add the modified HTML content to the in-memory zip
            zf.writestr(output_filename, html_content)

    # Seek to the beginning of the buffer to prepare for download
    zip_buffer.seek(0)

    # Create a download button for the zip file containing all modified HTML files
    st.download_button(
        label="Download All Modified HTML Files (as ZIP)",
        data=zip_buffer,
        file_name='modified_html_templates.zip',
        mime='application/zip'
    )

    st.success("HTML content modified for all rows. Click the button above to download the modified files.")
else:
    st.info("Please upload both an Excel file and an HTML file.")
