# Use a smaller base image
FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# OS dependencies (Alpine uses apk)
RUN apk add --no-cache \
    curl \
    git \
    bash

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh || true

WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies more efficiently
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source
COPY . .

# (Optional) Comment these lines to avoid downloading large models during build
# RUN ollama pull znbang/bge:small-en-v1.5-q8_0 && \
#     ollama pull deepseek-r1:1.5b

# Streamlit default port
EXPOSE 8501

# Run Ollama in the background and start Streamlit
CMD ["sh", "-c", "ollama serve & streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0"]
