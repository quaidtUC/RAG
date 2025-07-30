import argparse
import os
import json
import PyPDF2
import faiss
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump


def extract_text(pdf_path: str) -> str:
    """Extract all text from a PDF file using PyPDF2."""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def chunk_text(text: str, size: int = 1000, overlap: int = 100):
    """Yield chunks of text with optional overlap."""
    start = 0
    while start < len(text):
        end = start + size
        yield text[start:end]
        start += size - overlap


def build_index(pdf_dir: str, index_path: str, metadata_path: str, vectorizer_path: str,
                chunk_size: int = 1000, overlap: int = 100):
    """Build a FAISS index from PDFs in *pdf_dir* and store metadata."""
    pdf_files = [
        os.path.join(pdf_dir, f)
        for f in os.listdir(pdf_dir)
        if f.lower().endswith(".pdf")
    ]

    texts = []
    metadata = []
    for pdf_file in pdf_files:
        text = extract_text(pdf_file)
        for i, chunk in enumerate(chunk_text(text, chunk_size, overlap)):
            texts.append(chunk)
            metadata.append({"source": os.path.basename(pdf_file), "chunk": i})

    if not texts:
        raise ValueError("No text extracted from PDFs")

    vectorizer = TfidfVectorizer(max_features=4096)
    embeddings = vectorizer.fit_transform(texts).toarray().astype("float32")
    dump(vectorizer, vectorizer_path)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, index_path)
    with open(metadata_path, "w") as f:
        json.dump(metadata, f)

    print(f"Indexed {len(texts)} text chunks from {len(pdf_files)} PDFs")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a FAISS index from PDF files")
    parser.add_argument("pdf_dir", help="Directory containing PDF files")
    parser.add_argument("--index", "-i", default="index.faiss", help="Output FAISS index path")
    parser.add_argument("--metadata", "-m", default="metadata.json", help="Output metadata JSON path")
    parser.add_argument(
        "--vectorizer", "-v", default="vectorizer.joblib", help="Path to store fitted vectorizer"
    )
    parser.add_argument("--chunk-size", type=int, default=1000, help="Number of characters per chunk")
    parser.add_argument("--overlap", type=int, default=100, help="Overlap between chunks")
    args = parser.parse_args()

    build_index(
        pdf_dir=args.pdf_dir,
        index_path=args.index,
        metadata_path=args.metadata,
        vectorizer_path=args.vectorizer,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )


if __name__ == "__main__":
    main()
