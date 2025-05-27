import streamlit as st
from app import LocalRAGApp  # importing app

st.set_page_config(page_title="Local RAG App", layout="centered")

st.title("📄 Local RAG Document QA")
st.markdown("Upload a PDF and ask questions about it!")

app = LocalRAGApp()
data = None

with st.sidebar:
    st.header("Upload a PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        data = app.load_document("temp.pdf")
        app.create_vector_db(data)
        app.setup_retrieval_chain()
        st.success("✅ PDF uploaded succesfully !")

# Zone principale
if uploaded_file:
    st.markdown("---")
    st.subheader("💬 Ask about your PDF")

    question = st.text_input("Ask a question about your document:")
    if question:
        response = app.chain.invoke(question)
        st.markdown("### ✅ Response :")
        st.success(response)

    st.markdown("---")
    st.subheader("📚 Summary of the PDF sections")

    if st.button("Generate a simplified summary"):
        with st.spinner("Generating..."):
            app.summarize_sections(data)
            try:
                with open("summaries.txt", "r", encoding="utf-8") as f:
                    summaries = f.read()
                st.success("Summary generated succesfully !")
                st.markdown("#### 📝 Résumés :")
                st.text_area(label="", value=summaries, height=400)

                st.download_button(
                    label="Download your summary (.txt)",
                    data=summaries,
                    file_name="resume_sections.txt",
                    mime="text/plain"
                )

            except FileNotFoundError:
                st.error(" Error : Something went wrong.")
