def convert_to_markdown(text, output_path):
    structured = f"# Invoice Document\n\n{text}"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(structured)