import fitz

def is_digital_pdf(path):
    doc = fitz.open(path)
    for page in doc:
        if page.get_text().strip():
            return True
    return False