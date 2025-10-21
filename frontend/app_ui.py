import streamlit as st
import fitz  # PyMuPDF for preview
import requests
import json
import os

# ============================
# Configuration
# ============================
PDF_SERVICE_URL = "http://localhost:8001"
RAG_SERVICE_URL = "http://localhost:8002"
CHAT_SERVICE_URL = "http://localhost:8003"

# ============================
# Streamlit UI Layout
# ============================
st.set_page_config(page_title="📄 Local RAG QA App", layout="wide", page_icon="📄")

st.markdown(
    """
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .sidebar .sidebar-content { padding-top: 2rem; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stDownloadButton>button {
        background-color: #007ACC;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("📄 Local RAG Document QA")
st.markdown("Upload a PDF and interact with your documents using a local AI pipeline. 🔍")

# ============================
# Sidebar: File Upload
# ============================
with st.sidebar:
    st.header("📁 Upload your PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("🔄 Extracting content from PDF..."):
            files = {"file": open("temp.pdf", "rb")}
            response = requests.post(f"{PDF_SERVICE_URL}/extract-pages", files=files)
            pdf_data = response.json()

        if "error" in pdf_data:
            st.error(f"❌ Error loading PDF: {pdf_data['error']}")
            st.stop()
        else:
            st.success(f"✅ PDF loaded ({pdf_data['page_count']} pages)")
            st.session_state["pdf_content"] = pdf_data["content"]

            # Send to RAG service to build vector DB
            with st.spinner("🔍 Building vector database..."):
                build_resp = requests.post(f"{RAG_SERVICE_URL}/build-vector-db", json=pdf_data["content"])
                if "error" in build_resp.json():
                    st.error("❌ Failed to create vector DB.")
                else:
                    st.success("✅ Vector database created and ready!")

# ============================
# Question Answering
# ============================
if "pdf_content" in st.session_state:
    st.markdown("---")
    st.subheader("💬 Ask Questions")

    question = st.text_input("🔎 Ask something about your document:")

    if question:
        with st.spinner("🤔 Thinking..."):
            resp = requests.post(f"{RAG_SERVICE_URL}/query", json=question)
            data = resp.json()
            answer = data.get("answer", "⚠️ No response from backend.")

            st.success(answer)

            # Add conversation message
            chat_payload = {"pdf_id": "default_pdf", "role": "user", "message": question}
            requests.post(f"{CHAT_SERVICE_URL}/add", json=chat_payload)
            chat_payload = {"pdf_id": "default_pdf", "role": "assistant", "message": answer}
            requests.post(f"{CHAT_SERVICE_URL}/add", json=chat_payload)

    with st.expander("🗂 Conversation History"):
        conv = requests.get(f"{CHAT_SERVICE_URL}/get/default_pdf").json()
        if conv:
            for msg in conv:
                role = "🧑" if msg["role"] == "user" else "🤖"
                st.markdown(f"**{role} {msg['role'].capitalize()}:** {msg['content']}")
        else:
            st.info("No messages yet.")

# ============================
# Summarization (Page Selection)
# ============================
if uploaded_file:
    st.markdown("---")
    st.subheader("📖 Select Pages to Summarize")

    doc = fitz.open("temp.pdf")
    num_pages = len(doc)
    st.markdown(f"**Total pages:** {num_pages}")

    page_selection = st.multiselect(
        "Select page numbers to summarize (starting from 1):",
        options=list(range(1, num_pages + 1))
    )

    if page_selection and st.button("🧠 Summarize Selected Pages"):
        with st.spinner("🧠 Generating summaries..."):
            selected_texts = [doc[p - 1].get_text() for p in page_selection]
            response = requests.post(f"{RAG_SERVICE_URL}/build-vector-db", json=selected_texts)
            summaries = [t[:500] + "..." for t in selected_texts]  # simple truncation mockup
            st.text_area("📌 Summary (preview)", "\n\n".join(summaries), height=400)
