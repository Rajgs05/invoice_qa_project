from src.pdf_detector import is_digital_pdf
from src.ocr_pipeline import extract_text_from_pdf
from src.markdown_converter import convert_to_markdown
from src.rag_pipeline import build_query_engine
import pdfplumber

pdf_path = "data/raw_pdfs/invoice.pdf"

if is_digital_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text += f"\n\n## Page {i+1}\n\n"
            text += page.extract_text() + "\n"
else:
    text = extract_text_from_pdf(pdf_path)

convert_to_markdown(text, "data/markdown/Test.md")

query_engine = build_query_engine("data/markdown")

while True:
    question = input("Ask your question: ")
    response = query_engine.query(
    f"""
    Answer ONLY from the invoice document.
    If the answer is not present, say 'Not found in document'.
    Do not hallucinate or make up answers. Be concise.
    Read from the document and answer the question based on that information.
    Question: {question}
    """
)
    print("\nAnswer:\n", response)