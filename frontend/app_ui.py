import streamlit as st
import fitz  # PyMuPDF for preview
import requests
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
st.markdown("Upload a PDF and interact with your documents using your local AI pipeline. 🔍")

# ============================
# Sidebar: File Upload
# ============================
with st.sidebar:
    st.header("📁 Upload your PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        st.success(f"✅ PDF '{uploaded_file.name}' uploaded successfully!")

        # 🔥 Automatically call extract-and-embed when PDF is uploaded
        with st.spinner("Building embeddings for your PDF..."):
            files = {"file": open("temp.pdf", "rb")}
            res = requests.post(f"{PDF_SERVICE_URL}/extract-and-embed", files=files)

            if res.status_code == 200:
                st.success("✅ Embeddings built successfully! You can now ask questions about this document.")
            else:
                st.error(f"❌ Failed to build embeddings: {res.text}")

# ============================
# PDF Preview
# ============================
if uploaded_file:
    st.markdown("---")
    st.subheader("📖 PDF Preview")

    doc = fitz.open("temp.pdf")
    num_pages = len(doc)
    st.markdown(f"**Total pages:** {num_pages}")

    page_to_view = st.slider("Select a page to preview", 1, num_pages, 1)
    page_text = doc[page_to_view - 1].get_text()
    st.text_area(f"📘 Page {page_to_view} Preview", page_text[:2000] + "...")

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

                    # Save to chat history
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
