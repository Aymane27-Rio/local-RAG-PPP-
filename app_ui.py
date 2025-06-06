import streamlit as st
from app import LocalRAGApp #importing app.py

st.set_page_config(page_title="📄 Local RAG QA App", layout="wide", page_icon="📄")

# some styles added
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        padding-top: 2rem;
    }
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

st.title(" Local RAG Document QA")
st.markdown("Upload a PDF and ask questions. You can also generate simple summaries by section.")

app = LocalRAGApp()
data = None

with st.sidebar:
    st.header("📁 Upload your PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        data = app.load_document("temp.pdf")

        with st.spinner("🔄 Processing your document..."):
            app.create_vector_db(data)
            app.setup_retrieval_chain()

        st.success("✅ PDF processed and ready!")

if uploaded_file:
    st.markdown("---")
    st.subheader("💬 Ask Questions")

    with st.expander("Type your question below", expanded=True):
        question = st.text_input("🔎 Question:")
        if question:
            with st.spinner("⏳ Searching the document..."):
                response = app.chain.invoke(question)
            st.markdown("### ✅ Response")
            st.success(response)

    st.markdown("---")
    st.subheader("📚 Section Summarization")

    with st.expander("📄 Generate a simplified summary"):
        if st.button("🧠 Summarize PDF Sections"):
            with st.spinner("⏳ Summarizing..."):
                app.summarize_sections(data)
                try:
                    with open("summaries.txt", "r", encoding="utf-8") as f:
                        summaries = f.read()
                    st.success("✅ Summary generated!")
                    st.text_area("📝 Résumés", summaries, height=400)

                    st.download_button(
                        label="⬇️ Download Summary (.txt)",
                        data=summaries,
                        file_name="resume_sections.txt",
                        mime="text/plain"
                    )
                except FileNotFoundError:
                    st.error("⚠️ Something went wrong.")
