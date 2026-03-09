import os
from llama_parse import LlamaParse

def parse_invoice(file_path):
    api_key = os.environ.get("LLAMA_CLOUD_API_KEY")

    if not api_key:
        raise ValueError("LLAMA_CLOUD_API_KEY not set")

    parser = LlamaParse(
        result_type="markdown",
    )

    documents = parser.load_data(file_path)

    if not documents:
        return ""

    full_markdown = ""

    for i, doc in enumerate(documents):
        full_markdown += f"\n\n## Page {i+1}\n\n"
        full_markdown += doc.text

    return full_markdown