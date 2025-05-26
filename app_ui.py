import streamlit as st
from app import LocalRAGApp  # importing app

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
        app.create_vector_db(data)
        app.setup_retrieval_chain()
        st.success("✅ Document chargé et base vectorielle créée !")

# Zone principale
if uploaded_file:
    st.markdown("---")
    st.subheader("💬 Posez votre question sur le document")

    question = st.text_input("Ask a question about your document:")
    if question:
        response = app.chain.invoke(question)
        st.markdown("### ✅ Réponse :")
        st.success(response)

    st.markdown("---")
    st.subheader("📚 Résumé des sections du document")

    if st.button("✨ Générer le résumé simplifié"):
        with st.spinner("Génération des résumés..."):
            app.summarize_sections(data)
            try:
                with open("summaries.txt", "r", encoding="utf-8") as f:
                    summaries = f.read()
                st.success("Résumé généré avec succès !")
                st.markdown("#### 📝 Résumés :")
                st.text_area(label="", value=summaries, height=400)

                st.download_button(
                    label="📥 Télécharger le résumé (.txt)",
                    data=summaries,
                    file_name="resume_sections.txt",
                    mime="text/plain"
                )

            except FileNotFoundError:
                st.error("❌ Erreur : le fichier summaries.txt est introuvable.")
