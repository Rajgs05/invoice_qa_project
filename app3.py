import streamlit as st
import tempfile
import os
from PIL import Image
from pdf2image import convert_from_path

from src.llm_qa import ask_llm
from src.unstructured_parser import parse_with_unstructured
from src.qwen_parser import parse_with_qwen
from pdf2image import convert_from_path


st.set_page_config(page_title="Invoice AI Lab", layout="wide")

st.title("📄 Invoice AI Lab – Multi Parser")

col1, col2 = st.columns([1, 1])

# 🔹 Parser Selector
parser_choice = st.selectbox(
    "Select Parser",
    ["Unstructured", "Qwen Vision"]
)

uploaded_file = st.file_uploader(
    "Upload Invoice (PDF or Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    file_extension = uploaded_file.name.split(".")[-1]

    # Save file with proper extension
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{file_extension}"
    ) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    # 🔹 Convert image to PDF for uniform handling
    if file_extension.lower() in ["png", "jpg", "jpeg"]:
        image = Image.open(file_path)
        pdf_path = file_path + ".pdf"
        image.convert("RGB").save(pdf_path)
        file_path = pdf_path

    # 🔹 PARSER LOGIC
    markdown_content = ""
    elements = None

    with st.spinner(f"🔄 Parsing with {parser_choice}..."):

        if parser_choice == "Unstructured":
            elements, markdown_content = parse_with_unstructured(file_path)

        elif parser_choice == "Qwen Vision":

            # 🔥 Multi-page support
            pages = convert_from_path(file_path)

            full_output = ""

            for i, page in enumerate(pages):
                st.write(f"Processing Page {i+1}...")
                page_markdown = parse_with_qwen(page)
                full_output += f"\n\n## Page {i+1}\n\n{page_markdown}"

            markdown_content = full_output

    if not markdown_content.strip():
        st.error("Parsing returned empty content.")
        st.stop()

    # 🔹 View Mode Toggle (Only for Unstructured)
    if parser_choice == "Unstructured":
        view_mode = st.radio(
            "Select View Mode:",
            ["Markdown View", "Raw Elements JSON"]
        )
    else:
        view_mode = "Markdown View"

    # 🔹 LEFT PANEL
    with col1:
        st.subheader("📄 Document View")

        if view_mode == "Markdown View":
            st.markdown(markdown_content)
        else:
            st.json(elements)

    # 🔹 RIGHT PANEL — Q&A
    with col2:
        st.subheader("💬 Ask Questions About This Invoice")

        question = st.text_input("Enter your question")

        if question:
            with st.spinner("🤖 Generating answer..."):
                answer = ask_llm(markdown_content, question)
                st.success(answer)