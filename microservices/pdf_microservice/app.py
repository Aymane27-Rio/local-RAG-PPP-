from fastapi import FastAPI, UploadFile, File, Form
import fitz  # PyMuPDF
import tempfile
import os
import requests

RAG_SERVICE_URL = os.getenv("RAG_SERVICE_URL", "http://rag_microservice:8002")

app = FastAPI(title="PDF Service", version="1.1")

@app.get("/")
def root():
    return {"message": "PDF Service is running"}


@app.post("/extract-and-embed")
async def extract_and_embed(file: UploadFile = File(...), pages: str = Form(None)):
    """
    Upload PDF, optionally select pages, extract text, and send to RAG for embedding.
    """
    try:
        # ✅ Step 1: Save the PDF temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        # ✅ Step 2: Extract text from all or selected pages
        doc = fitz.open(tmp_path)
        selected_texts = []

        if pages:
            indices = [int(p.strip()) for p in pages.split(",") if p.strip().isdigit()]
            for i in indices:
                if 0 <= i < len(doc):
                    selected_texts.append(doc[i].get_text())
        else:
            for page in doc:
                selected_texts.append(page.get_text())

        doc.close()
        os.remove(tmp_path)

        print(f"📄 Extracted {len(selected_texts)} pages from {file.filename}")

        # ✅ Step 3: Send text chunks to RAG microservice for embedding
        try:
            response = requests.post(
                f"{RAG_SERVICE_URL}/build-vector-db",
                json=selected_texts,  # ✅ send list directly
                timeout=120
            )

            if response.status_code == 200:
                print("✅ Embeddings built successfully by RAG service.")
                return {
                    "status": "success",
                    "pdf": file.filename,
                    "pages_embedded": len(selected_texts),
                    "rag_response": response.json()
                }
            else:
                print("❌ RAG service returned an error:", response.text)
                return {"error": f"RAG service failed: {response.text}"}

        except Exception as e:
            print(f"❌ Failed to call RAG service: {e}")
            return {"error": f"Failed to send data to RAG service: {e}"}

    except Exception as e:
        print(f"❌ Error in PDF processing: {e}")
        return {"error": str(e)}
