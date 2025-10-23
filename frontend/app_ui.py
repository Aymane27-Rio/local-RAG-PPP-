import streamlit as st
import fitz  # PyMuPDF for preview
import requests
import json
import os

# ============================
# Configuration
# ============================
PDF_SERVICE_URL = "http://pdf_microservice:8001"
RAG_SERVICE_URL = "http://rag_microservice:8002"
CHAT_SERVICE_URL = "http://chat_microservice:8003"

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

        st.success(f"✅ PDF uploaded successfully!")

# ============================
# PDF Preview and Summary
# ============================
if uploaded_file:
    st.markdown("---")
    st.subheader("📖 PDF Preview & Summarization")

    doc = fitz.open("temp.pdf")
    num_pages = len(doc)
    st.markdown(f"**Total pages:** {num_pages}")

    page_selection = st.multiselect(
        "Select pages to summarize:",
        options=list(range(1, num_pages + 1)),
    )

    if page_selection and st.button("🧠 Summarize Selected Pages"):
        with st.spinner("Generating summaries..."):
            # Extract text for selected pages
            selected_texts = [doc[p - 1].get_text() for p in page_selection]
            joined_text = "\n\n".join(selected_texts)
            res = requests.post(f"{PDF_SERVICE_URL}/extract-text", files={"file": open("temp.pdf", "rb")})
            if res.status_code == 200:
                st.success("✅ Extracted text successfully.")
                st.text_area("📘 Extracted Text (Preview)", joined_text[:2000] + "...")
            else:
                st.error("Failed to extract text from PDF.")

# ============================
# Question Answering
# ============================
if uploaded_file:
    st.markdown("---")
    st.subheader("💬 Ask Questions About This PDF")

    question = st.text_input("🔎 Ask a question about your document:")

    if st.button("Ask"):
        if not question.strip():
            st.warning("Please enter a question first.")
        else:
            with st.spinner("🤔 Thinking..."):
                resp = requests.post(f"{RAG_SERVICE_URL}/query", json={"question": question})
                if resp.status_code == 200:
                    answer = resp.json().get("answer", "")
                    st.success(answer)

                    # Store messages in chat history
                    requests.post(f"{CHAT_SERVICE_URL}/save", json={"user": "user", "message": question})
                    requests.post(f"{CHAT_SERVICE_URL}/save", json={"user": "assistant", "message": answer})
                else:
                    st.error("Error communicating with RAG service.")

# ============================
# Conversation History
# ============================
if uploaded_file:
    st.markdown("---")
    st.subheader("🗂 Conversation History")

    if st.button("🔄 Refresh History"):
        res = requests.get(f"{CHAT_SERVICE_URL}/history")
        if res.status_code == 200:
            chats = res.json()
            if not chats:
                st.info("No conversation yet.")
            else:
                for c in chats:
                    role_icon = "🧑" if c["user"] == "user" else "🤖"
                    st.markdown(f"**{role_icon} {c['user'].capitalize()}:** {c['message']}")
        else:
            st.error("Failed to fetch conversation history.")