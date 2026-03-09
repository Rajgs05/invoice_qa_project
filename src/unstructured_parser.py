import os
from dotenv import load_dotenv
from unstructured_client import UnstructuredClient
from unstructured_client.models import operations, shared

load_dotenv()

def parse_with_unstructured(file_path):

    client = UnstructuredClient(
        api_key_auth=os.getenv("UNSTRUCTURED_API_KEY"),
    )

    with open(file_path, "rb") as f:
        files = shared.Files(
            content=f.read(),
            file_name=os.path.basename(file_path),
        )

    req = operations.PartitionRequest(
        partition_parameters=shared.PartitionParameters(
            files=files,
            strategy="hi_res",   # OCR + layout aware
        )
    )

    res = client.general.partition(request=req)

    elements = res.elements

    markdown = ""

    for el in elements:
        text = el.get("text", "").strip()
        category = el.get("type", "")

        if not text:
            continue

        if category == "Title":
            markdown += f"\n\n# {text}\n\n"

        elif category == "ListItem":
            markdown += f"- {text}\n"

        elif category == "Table":
            markdown += f"\n\n```\n{text}\n```\n\n"

        elif category == "Header":
            markdown += f"\n\n## {text}\n\n"

        else:
            markdown += text + "\n\n"

    return elements, markdown