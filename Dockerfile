FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV CUDA_HOME=/usr/local/cuda

RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    wget \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY app.py gpu_manager.py api_server.py mcp_server.py download_in_container.sh ./

RUN mkdir -p /app/models /tmp/infinitetalk_uploads /tmp/infinitetalk_results

EXPOSE 7860

CMD ["/bin/bash", "-c", "/app/download_in_container.sh && python3 app.py"]
