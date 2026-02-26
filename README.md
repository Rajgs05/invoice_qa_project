# Invoice Q&A System (OCR + RAG + Groq)

## 🚀 Overview

This project extracts text from scanned and digital invoices and enables intelligent Question & Answering using RAG architecture.

Pipeline:
PDF → OCR (PaddleOCR) → Markdown → Embeddings (MiniLM) → FAISS → Groq LLM

---

## 🧠 Features

- Supports scanned PDFs (OCR)
- Supports digital PDFs (pdfplumber)
- Multi-page invoice support
- Markdown-based structured storage
- Local embeddings (CPU friendly)
- Groq cloud LLM integration
- Retrieval-Augmented Generation (RAG)

---

## 🛠 Tech Stack

- PaddleOCR
- PyMuPDF
- pdfplumber
- LlamaIndex
- SentenceTransformers (MiniLM)
- FAISS
- Groq API

---
