import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader

st.set_page_config(page_title="Simple RAG")

st.title("Simple Retrieval-Augmented Generation")

# Storage for uploaded documents
docs = []

uploaded_files = st.file_uploader("Upload .txt or .pdf files", type=["txt", "pdf"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        if file.type == "application/pdf" or file.name.lower().endswith(".pdf"):
            pdf = PdfReader(file)
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        else:
            text = file.read().decode("utf-8", errors="ignore")
        docs.append({"name": file.name, "text": text})

if docs:
    st.success(f"Loaded {len(docs)} document(s)")

query = st.text_input("Search")

if st.button("Run") and query:
    corpus = [d["text"] for d in docs]
    names = [d["name"] for d in docs]
    vectorizer = TfidfVectorizer().fit(corpus + [query])
    vectors = vectorizer.transform(corpus)
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, vectors).flatten()
    top_indices = similarities.argsort()[::-1][:3]

    st.subheader("Retrieved Documents")
    retrieved = []
    for idx in top_indices:
        st.write(f"**{names[idx]}** (score: {similarities[idx]:.2f})")
        snippet = docs[idx]["text"][:500]
        st.code(snippet)
        retrieved.append(snippet)

    # Simple 'generated' answer by concatenating snippets
    answer = "\n".join(retrieved)
    st.subheader("Generated Answer")
    st.write(answer)
