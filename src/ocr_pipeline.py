import os


os.environ["FLAGS_use_mkldnn"] = "0"        
os.environ["FLAGS_enable_pir_api"] = "0"    
os.environ["FLAGS_allocator_strategy"] = "naive_best_fit"
os.environ["PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK"] = "True"

import fitz
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')


def extract_text_from_pdf(pdf_path):
    full_text = ""  

    doc = fitz.open(pdf_path)

    for page in doc:
        full_text += f"\n\n## Page {page.number + 1}\n\n"

        pix = page.get_pixmap()
        image_path = "temp_page.png"
        pix.save(image_path)

        result = ocr.ocr(image_path)

        for line in result[0]:
            full_text += line[1][0] + "\n"

        os.remove(image_path)

    return full_text


def extract_text_from_image(image_path):
    full_text = "" 

    result = ocr.ocr(image_path)

    for line in result[0]:
        full_text += line[1][0] + "\n"

    return full_text