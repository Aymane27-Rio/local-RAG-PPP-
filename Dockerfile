FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# OS dependencies
RUN apt update && apt install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# working directory
WORKDIR /app

COPY . /app
# COPY requirements.txt /app/

# python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


# pull Ollama models
RUN ollama pull znbang/bge:small-en-v1.5-q8_0 && \
    ollama pull deepseek-r1:1.5b

# streamlit default port
EXPOSE 8501

# running Ollama in the background and starting Streamlit
CMD ["sh", "-c", "ollama serve & streamlit run app_ui.py --server.port 8501 --server.address 0.0.0.0"]
