from fastapi import FastAPI, UploadFile, File, Form
import fitz  # PyMuPDF
import tempfile
import os

app = FastAPI(title="PDF Service", version="1.0")

@app.get("/")
def root():
    return {"message": "PDF Service is running"}

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    """Extract text from uploaded PDF"""
    doc = fitz.open(stream=await file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return {"text": text[:2000] + "..."}  # return preview only

@app.post("/extract-pages")
async def extract_pages(file: UploadFile = File(...), pages: str = Form(None)):
    """
    Upload PDF and optionally extract specific pages.
    'pages' is a comma-separated list (e.g., "0,2,3")
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

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

        return {"page_count": len(selected_texts), "content": selected_texts}

    except Exception as e:
        return {"error": str(e)}
