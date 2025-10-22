# frontend/Dockerfile
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required by PyMuPDF and Streamlit
RUN apt update && apt install -y \
    libstdc++6 \
    libgl1 \
    libglib2.0-0 \
    curl \
    git \
    bash \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_ui.py", "--server.port=8501", "--server.address=0.0.0.0"]
