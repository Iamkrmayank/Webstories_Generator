import pandas as pd
import streamlit as st

# Streamlit app title
st.title('Story Template Generator')

# File upload for Excel and HTML
uploaded_excel = st.file_uploader("Upload the Excel file (for replacements)", type="xlsx")
uploaded_html = st.file_uploader("Upload the HTML file", type="html")

# Proceed if both files are uploaded
if uploaded_excel and uploaded_html:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_excel, header=None)

    # Read the uploaded HTML file
    html_content = uploaded_html.read().decode('utf-8')

    # The first row (index 0) contains placeholders like {{storytitle}}, {{coverinfo1}}, etc.
    placeholders = df.iloc[0, :].tolist()
    # The second row (index 1) contains the actual values
    actual_values = df.iloc[1, :].tolist()

    # Perform batch replacement by iterating through placeholders and corresponding actual values
    for placeholder, actual_value in zip(placeholders, actual_values):
        html_content = html_content.replace(placeholder, str(actual_value))

    # Create a download button for the modified HTML
    st.download_button(label="Download Modified HTML", 
                       data=html_content, 
                       file_name='Listerr_master_template.html', 
                       mime='text/html')

    st.success("HTML content modified. Click the button above to download the modified file.")
else:
    st.info("Please upload both an Excel file and an HTML file.")
