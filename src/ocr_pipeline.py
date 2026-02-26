import os
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"


from paddleocr import PaddleOCR
import fitz


ocr = PaddleOCR(use_angle_cls=True, lang='en')

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text += f"\n\n## Page {page.number + 1}\n\n"

    for page in doc:
        pix = page.get_pixmap()
        image_path = "temp_page.png"
        pix.save(image_path)

        result = ocr.ocr(image_path)
        for line in result[0]:
            full_text += line[1][0] + "\n"

        os.remove(image_path)

    return full_text