import streamlit as st
import tempfile
import os
from PIL import Image
import json

from src.llm_qa import ask_llm
from src.unstructured_parser import parse_with_unstructured




st.set_page_config(page_title="Invoice AI Lab", layout="wide")

st.title("📄 Invoice AI Lab – Unstructured.io")

col1, col2 = st.columns([1, 1])

uploaded_file = st.file_uploader(
    "Upload Invoice (PDF or Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    file_extension = uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{file_extension}"
    ) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    if file_extension.lower() in ["png", "jpg", "jpeg"]:
        image = Image.open(file_path)
        pdf_path = file_path + ".pdf"
        image.convert("RGB").save(pdf_path)
        file_path = pdf_path

    with st.spinner("🔄 Parsing with Unstructured..."):
        elements, markdown_content = parse_with_unstructured(file_path)

    if not markdown_content.strip():
        st.error("Parsing returned empty content.")
        st.stop()

    # View Mode Toggle
    view_mode = st.radio(
        "Select View Mode:",
        ["Markdown View", "Raw Elements JSON"]
    )

    # LEFT PANEL
    with col1:
        st.subheader("📄 Document View")

        if view_mode == "Markdown View":
            st.markdown(markdown_content)

        else:
            st.json(elements)

    # RIGHT PANEL — Q&A
    with col2:
        st.subheader("💬 Ask Questions About This Invoice")

        question = st.text_input("Enter your question")

        if question:
            with st.spinner("🤖 Generating answer..."):
                answer = ask_llm(markdown_content, question)
                st.success(answer)