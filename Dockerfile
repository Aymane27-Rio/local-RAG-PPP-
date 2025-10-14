# Base image
FROM python:3.10-slim

# Prevent .pyc and buffer logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#  OS dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# working dir
WORKDIR /app

# fixing the ci by copying only the requirements file for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# copy the rest of the app
COPY . .

# Ollama models
RUN ollama pull znbang/bge:small-en-v1.5-q8_0 && \
    ollama pull deepseek-r1:1.5b

# streamlit port
EXPOSE 8501

# Run Ollama and Streamlit
CMD ["sh", "-c", "ollama serve & streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0"]
