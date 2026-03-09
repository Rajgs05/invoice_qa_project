import streamlit as st
import os
import tempfile
import pdfplumber

from src.pdf_detector import is_digital_pdf
from src.ocr_pipeline import extract_text_from_pdf,extract_text_from_image
from src.markdown_converter import convert_to_markdown
from src.llm_qa import ask_llm

st.set_page_config(page_title="Invoice Q&A", layout="wide")

st.title(" Invoice  Assistant")

# Two-column layout
col1, col2 = st.columns([1, 1])

uploaded_file = st.file_uploader(
    "Upload Invoice (PDF or Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    markdown_path = "temp_invoice.md"

    # Extract text
    if uploaded_file.type == "application/pdf":
        if is_digital_pdf(file_path):
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    text += f"\n\n## Page {i+1}\n\n"
                    text += page.extract_text() + "\n"
        else:
            text = extract_text_from_pdf(file_path)
    else:
        # Image case → OCR directly
        text = extract_text_from_image(file_path)
        

    # Convert to markdown
    convert_to_markdown(text, markdown_path)

    # Load markdown
    with open(markdown_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # LEFT PANEL — Markdown Viewer
    with col1:
        st.subheader("📄 Extracted Invoice (Markdown View)")
        st.markdown(
            f"""
            <div style="
                background-color:#111;
                padding:20px;
                border-radius:10px;
                height:600px;
                overflow-y:scroll;
                font-size:14px;
            ">
            {markdown_content}
            </div>
            """,
            unsafe_allow_html=True
        )

    # RIGHT PANEL — Q&A
    with col2:
        st.subheader(" Ask Questions About This Invoice")

        question = st.text_input("Enter your question")

        if question:
            answer = ask_llm(markdown_content, question)

            st.markdown("###  Answer")
            st.success(answer)