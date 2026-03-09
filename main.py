from src.pdf_detector import is_digital_pdf
from src.ocr_pipeline import extract_text_from_pdf
from src.markdown_converter import convert_to_markdown
from src.llm_qa import ask_llm
import pdfplumber

pdf_path = "data/raw_pdfs/invoice.pdf"
markdown_path = "data/markdown/invoice_llmtest.md"

# Extract text
if is_digital_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text += f"\n\n## Page {i+1}\n\n"
            text += page.extract_text() + "\n"
else:
    text = extract_text_from_pdf(pdf_path)

# Convert to markdown
convert_to_markdown(text, markdown_path)

# Load markdown
with open(markdown_path, "r", encoding="utf-8") as f:
    markdown_content = f.read()

# Question loop
while True:
    question = input("Ask your question: ")
    answer = ask_llm(markdown_content, question)
    print("\nAnswer:\n", answer)