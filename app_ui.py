import streamlit as st
from app import LocalRAGApp #importing app

st.set_page_config(page_title="Local RAG App", layout="centered")

st.title("📄 Local RAG Document QA")
st.markdown("Upload a PDF and ask questions about it!")

app = LocalRAGApp()
data = None

with st.sidebar:
    st.header("Step 1: Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        data = app.load_document("temp.pdf")
    
        if st.button("🔍 Générer résumé par sections"):
            app.summarize_sections(data)
            with open("summaries.txt", "r", encoding="utf-8") as f:
                summaries_text = f.read()
            st.text_area("📑 Résumés des sections", summaries_text, height=400)
    
        app.create_vector_db(data)
        app.setup_retrieval_chain()
        st.success("✅ Document chargé et base vectorielle créée !")



if uploaded_file:
    question = st.text_input("Ask a question about your document:")
    if question:
        response = app.chain.invoke(question)
        st.markdown("### Answer:")
        st.success(response)
