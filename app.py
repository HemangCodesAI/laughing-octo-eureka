import streamlit as st
import os
import base64
from main import get_shit,process_shit
from PyPDF2 import PdfReader
from markdownify import markdownify
# Set up the Streamlit app
st.set_page_config("Boss ka project",page_icon="random",layout="wide")

st.title("HR Ki maa ki chut")


def pdf_to_markdown(pdf_path, markdown_path='inputs/resume.md'):
    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return
    
    # Read the PDF file
    reader = PdfReader(pdf_path)
    extracted_text = ""
    
    for page in reader.pages:
        extracted_text += page.extract_text() + "\n\n"  # Extract text and add spacing

    # Convert the extracted text to Markdown
    markdown_content = markdownify(extracted_text)
    
    # Save the Markdown content to a file
    with open(markdown_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)
    
    print(f"Markdown file saved at: {markdown_path}")

tab1, tab2= st.tabs(["Job Post Maker", "Candidate Analysis"])
with tab1:
    prompt=st.text_input('Enter some text')
    b=st.button('generate shit') 
    if b:
        # Show a spinner during a process
        with st.spinner(text='In progress'):
            shit=get_shit(prompt)
        st.markdown(shit)
        # st.balloons()
        st.snow()
        st.toast('TADA!!!!')
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        # st.write("upload post")
        a=st.file_uploader("upload post",key=1)
        if a is not None:
            # Get the uploaded file name
            file_name = a.name
            # Define the full path to save the file
            save_path = os.path.join("inputs", file_name)
            # Save the file to the directory
            with open(save_path, "wb") as f:
                f.write(a.getbuffer())
    with col2:
        # st.write("upload post")
        b=st.file_uploader("upload resume",key=2)
        if b is not None:
            # Get the uploaded file name
            file_name = b.name
            # Define the full path to save the file
            save_path = os.path.join("inputs", file_name)
            # Save the file to the directory
            with open(save_path, "wb") as f:
                f.write(b.getbuffer())
            pdf_to_markdown(save_path)
            # delete the pdf file
            os.remove(save_path)
    c=st.button("Process candidate")
    if c:
        with st.spinner("Analyzing"):
            analysis=process_shit()
        st.markdown(analysis)
        # st.balloons()
        st.snow()
        st.toast('TADA!!!!')
st.sidebar.title("Created Job posts")
directory_path = "data"

files = os.listdir(directory_path)

if files:
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)

        # Create a download link for the file
        with open(file_path, "rb") as file:
            file_data = file.read()
            b64 = base64.b64encode(file_data).decode()
            href = f'<a href="data:file/octet-stream;base64,{b64}" download="{file_name}">{file_name}</a>'
        
        # Display file download link in sidebar
        st.sidebar.markdown(href, unsafe_allow_html=True)
else:
    st.sidebar.write("No files found in the directory.")
