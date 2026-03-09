# Invoice AI Lab – Current Architecture

## Goal

Compare layout parser vs Vision LLM for invoice extraction.

## Parsers Implemented

1. Unstructured.io → elements → markdown
2. Qwen3 VL 8B Instruct (OpenRouter) → image → markdown

## Flow

Upload PDF/Image
→ Convert PDF to images
→ Parser selection
→ Markdown output
→ LLM Q&A (Groq)

## Model Used

Vision Model:

- qwen/qwen3-vl-8b-instruct

QA Model:

- (Groq model name)

## Features Implemented

- Multi-page support
- Markdown view
- JSON view (Unstructured only)
- Q&A grounded on extracted markdown

## Next Goals

- Side-by-side comparison
- Hallucination testing
- Structured JSON extraction
- Token usage monitoring
- Field-level accuracy benchmark
