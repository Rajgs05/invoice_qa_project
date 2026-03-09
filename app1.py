import streamlit as st
import tempfile
import os
from PIL import Image

from src.llm_qa import ask_llm
from src.parser import parse_invoice

st.set_page_config(page_title="Invoice Q&A", layout="wide")

st.title("📄 Invoice Assistant")

# Two column layout
col1, col2 = st.columns([1, 1])

uploaded_file = st.file_uploader(
    "Upload Invoice (PDF or Image)",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file:

    # Save uploaded file to temporary path
    file_extension = uploaded_file.name.split(".")[-1]
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=f".{file_extension}"
    ) as tmp_file:
        tmp_file.write(uploaded_file.read())
        file_path = tmp_file.name

    # If image → convert to PDF (LlamaParse works best with PDF)
    if file_extension.lower() in ["png", "jpg", "jpeg"]:
        try:
            image = Image.open(file_path)
            pdf_path = file_path + ".pdf"
            image.convert("RGB").save(pdf_path)
            file_path = pdf_path
        except Exception as e:
            st.error(f"Image conversion failed: {e}")
            st.stop()

    # Parse invoice using LlamaParse
    try:
        with st.spinner("🔄 Parsing invoice..."):
            markdown_content = parse_invoice(file_path)

        if not markdown_content or len(markdown_content.strip()) == 0:
            st.error("Parsing returned empty content.")
            st.stop()

    except Exception as e:
        st.error(f"Parsing failed: {e}")
        st.stop()

    # LEFT PANEL — Markdown View
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
                white-space:pre-wrap;
            ">
            {markdown_content}
            </div>
            """,
            unsafe_allow_html=True
        )

    # RIGHT PANEL — Q&A
    with col2:
        st.subheader("💬 Ask Questions About This Invoice")

        question = st.text_input("Enter your question")

        if question:
            with st.spinner("🤖 Generating answer..."):
                try:
                    answer = ask_llm(markdown_content, question)
                    st.markdown("### 🤖 Answer")
                    st.success(answer)
                except Exception as e:
                    st.error(f"LLM failed: {e}")