from src.pdf_detector import is_digital_pdf
from src.ocr_pipeline import extract_text_from_pdf
from src.markdown_converter import convert_to_markdown
from src.rag_pipeline import build_query_engine
import pdfplumber

pdf_path = "data/raw_pdfs/invoice.pdf"

if is_digital_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
else:
    text = extract_text_from_pdf(pdf_path)

convert_to_markdown(text, "data/markdown/invoice1.md")

query_engine = build_query_engine("data/markdown")

while True:
    question = input("Ask your question: ")
    response = query_engine.query(question)
    print("\nAnswer:\n", response)