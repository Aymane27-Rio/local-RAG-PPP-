<<<<<<< HEAD
#  Local RAG (Retrieval-Augmented Generation) Microservices App

This project is a **fully containerized local RAG system** built using **FastAPI microservices**, **Streamlit**, and **Ollama**.  
It allows users to upload PDFs, automatically embed their contents into a local vector database, and query them using an LLM — all running **completely offline**.

---

##  Features

-  **Modular microservice architecture**:
  - `ui_microservice`: Streamlit-based front-end.
  - `pdf_microservice`: Handles PDF uploads, text extraction, and embedding.
  - `rag_microservice`: Manages vector database creation, embedding, and question answering.
-  **Automatic PDF text extraction and embedding**
-  **Query documents** using locally running LLMs via Ollama
-  **Persistent vector store** (no external database required)
-  **Completely offline** — no external API keys or internet required after setup
-  **Docker-based deployment** for easy reproducibility and isolation


---

##  Requirements

- Python **3.9+**
- **Docker** and **Docker Compose**
- **Ollama** (for local LLM + embeddings)

---


##  Installation & Setup
=======
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
>>>>>>> b9adfce1630f5398fff971ea2f73482b1527b9af

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/local-rag-app.git
cd local-rag-app
```

<<<<<<< HEAD
### 2. Install Ollama
=======
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
>>>>>>> b9adfce1630f5398fff971ea2f73482b1527b9af

To do so, go to their official website https://ollama.com
After installing it, pull the required models by running the following commands:

```bash
ollama pull znbang/bge:small-en-v1.5-q8_0
ollama pull deepseek-r1:1.5b
```

<<<<<<< HEAD
### 3. Build and Run with Docker

```bash
docker compose up --build
```
then go to http://localhost:8501

##  Usage

1. **Upload a PDF file** in the web UI.
2. The **`pdf_microservice`** will extract the text and automatically send it to the **`rag_microservice`** for embedding.
3. Once embeddings are built, you can start **asking questions about the content**.
4. The answers will be generated **locally** by your **Ollama LLM** — no external APIs required.

---

##  Developer Notes

- If you modify code in any microservice, rebuild the containers:
```bash
  docker compose up --build
```
###  Logs & Ollama Connection

- To inspect logs for all running services:
```bash
  docker compose logs -f
```

The Ollama service runs on your host machine at port 11434, which the microservices connects to via: http://host.docker.internal:11434
=======
### 5. Run the App

```bash
python -m streamlit run app_ui.py
```
then go to http://localhost:8501
>>>>>>> b9adfce1630f5398fff971ea2f73482b1527b9af
