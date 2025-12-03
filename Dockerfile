FROM python:3.10-slim

WORKDIR /app

# 安装必要工具
RUN apt-get update && apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir gradio torch

COPY app.py /app/
COPY download_in_container.sh /app/

RUN chmod +x /app/download_in_container.sh

VOLUME /app/models

EXPOSE 8418

# 启动时先检查下载，然后启动应用
CMD ["/bin/bash", "-c", "/app/download_in_container.sh && python app.py"]
