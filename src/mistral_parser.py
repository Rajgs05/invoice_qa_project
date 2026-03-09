import os
import base64
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))


def image_to_data_url(image):
    import io

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    base64_image = base64.b64encode(buffer.getvalue()).decode()

    return f"data:image/png;base64,{base64_image}"


def parse_with_mistral(image):

    image_data_url = image_to_data_url(image)

    response = client.ocr.process(
        model="mistral-ocr-latest",
        document={
            "type": "image_url",
            "image_url": image_data_url
        }
    )

    markdown_output = ""

    for page in response.pages:
        markdown_output += page.markdown + "\n\n"

    return markdown_output