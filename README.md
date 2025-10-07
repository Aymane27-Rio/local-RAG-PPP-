# 📄 Local RAG Document QA App (Streamlit + Ollama)

This project lets you upload a PDF document, process it into a vector database using Ollama embeddings, and ask questions about its content using a locally running LLM (e.g., DeepSeek).

## 🚀 Features
- Upload any PDF document
- Uses `Ollama` for local embedding and chat model (no OpenAI API required)
- Ask questions and get accurate, document-based answers
- Clean UI built with Streamlit

---

## 📦 Requirements

- Python 3.9+
- Ollama (for local models)
- Pip (Python package manager)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/local-rag-app.git
cd local-rag-app
```

### 2. Create a Virtual Environment (usually recommended)

```bash
python3 -m venv venv
source venv/Scripts/activate  # On Windows
# OR
source venv/bin/activate  # On Linux/Mac
```

### 3. Install The Necessary Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Ollama

To do so, go to their official website https://ollama.com
After installing it, pull the required models by running the following commands:

```bash
ollama pull znbang/bge:small-en-v1.5-q8_0
ollama pull deepseek-r1:1.5b
```

### 5. Run the App

```bash
python -m streamlit run app_ui.py
```
then go to http://localhost:8501
