import streamlit as st
from app import LocalRAGApp #importing app

st.set_page_config(page_title="Local RAG App", layout="centered")

st.title("📄 Local RAG Document QA")
st.markdown("Upload a PDF and ask questions about it!")

app = LocalRAGApp()


with st.sidebar:
    st.header("Step 1: Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        data = app.load_document("temp.pdf")
        app.create_vector_db(data)
        app.setup_retrieval_chain()
        st.success("Document loaded and vector DB created!")


if uploaded_file:
    question = st.text_input("Ask a question about your document:")
    if question:
        response = app.chain.invoke(question)
        st.markdown("### Answer:")
        st.success(response)
