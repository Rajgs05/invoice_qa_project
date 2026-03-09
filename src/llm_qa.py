import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_llm(markdown_text: str, question: str):
    prompt = f"""
You are an intelligent invoice assistant.

You must answer strictly using ONLY the provided invoice content.
Do not hallucinate or make up answers. Be concise.
Read from the document and answer the question based on that information.
If there is any gramatical inconsistency or uncertainty in the question asked by the user, acknowledge/correct it and answer example if a user asks "what is the order numer",instead of "what is the order number" you should correct the spelling mistake and search it from the content and answer.
If multiple totals exist, choose the final payable total for that invoice.
If multiple invoices exist, answer for the most recent invoice (last page).
If the answer is not present, say: "Not found in document."



INVOICE CONTENT:
----------------
{markdown_text}

----------------

QUESTION:
{question}

Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.0  
    )

    return response.choices[0].message.content.strip()