import os
import base64
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def image_to_base64(image):
    import io
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode()

def parse_with_qwen(image):

    base64_image = image_to_base64(image)

    response = client.chat.completions.create(
        model="qwen/qwen3-vl-8b-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
You are a strict OCR engine.

Extract the invoice exactly as seen.
Do not hallucinate.
Do not infer missing values.
Preserve layout structure.
Return structured Markdown.
Preserve tables carefully.
If something is unclear, write [uncertain].
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content