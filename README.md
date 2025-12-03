# 🎬 InfiniteTalk & MultiTalk Deployment

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](Dockerfile)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)

A production-ready deployment solution for MeiGen-AI's InfiniteTalk and MultiTalk models, featuring automatic model management, Docker containerization, and a user-friendly Gradio interface.

## ✨ Features

- 🚀 **One-Click Deployment** - Automated model download and Docker containerization
- 📦 **Complete Model Support** - All 16 official models (InfiniteTalk + MultiTalk)
- 🎯 **Smart Model Management** - Auto-download missing models, auto-unload after 5min idle
- 🖥️ **Modern Web UI** - Gradio-based interface with real-time progress tracking
- 🔄 **Multi-Mode Support** - Image-to-video and video-to-video generation
- 💾 **Optimized Storage** - Supports INT8/FP8 quantized models (228GB total)
- 🌐 **Production Ready** - Nginx reverse proxy with SSL and authentication

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
  - [Method 1: Docker (Recommended)](#method-1-docker-recommended)
  - [Method 2: Direct Run](#method-2-direct-run)
- [Model Guide](#-model-guide)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/neosun100/infinitetalk-deployment.git
cd infinitetalk-deployment

# Start with Docker
docker-compose up -d

# Access UI at http://localhost:8418
```

## 📦 Installation

### Method 1: Docker (Recommended)

#### Prerequisites
- Docker >= 20.10
- Docker Compose >= 2.0
- NVIDIA GPU with CUDA support
- nvidia-docker2 installed

#### Step 1: Pull Docker Image

```bash
docker pull infinitetalk:latest
```

#### Step 2: Run Container

```bash
docker run -d \
  --name infinitetalk \
  --gpus all \
  -p 8418:7860 \
  -v /storage/infinitetalk/models:/app/models \
  infinitetalk:latest
```

#### Step 3: Verify

```bash
# Check container status
docker ps | grep infinitetalk

# View logs
docker logs -f infinitetalk

# Access UI
curl http://localhost:8418
```

#### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GRADIO_SERVER_PORT` | Web UI port | `7860` |
| `IDLE_TIMEOUT` | Model auto-unload timeout (seconds) | `300` |

#### Docker Compose Example

```yaml
version: '3.8'

services:
  infinitetalk:
    image: infinitetalk:latest
    container_name: infinitetalk
    restart: unless-stopped
    ports:
      - "8418:7860"
    volumes:
      - /storage/infinitetalk/models:/app/models
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    environment:
      - GRADIO_SERVER_PORT=7860
      - IDLE_TIMEOUT=300
```

### Method 2: Direct Run

#### Prerequisites
- Python 3.10+
- CUDA 11.8+ / CUDA 12.1+
- 32GB+ RAM
- 500GB+ free disk space

#### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

#### Step 2: Download Models

Models will be automatically downloaded on first run. You can also manually download:

```bash
# Download all models (228GB)
bash download_models.sh

# Or download specific models
bash download_multitalk.sh
```

#### Step 3: Start Application

```bash
python app.py
```

The application will be available at `http://localhost:7860`

## 📚 Model Guide

### InfiniteTalk Models (10 models)

| Model | Size | Type | Use Case |
|-------|------|------|----------|
| ⭐ Single (Original) | 11GB | Standard | Single person talking, **recommended for beginners** |
| ⭐ Multi (Original) | 9.95GB | Standard | Multi-person conversation, **recommended** |
| Single INT8 | 19.5GB | Quantized | Higher quality, single person |
| Single INT8 LoRA | 19.5GB | Quantized+Style | Style control support |
| Multi INT8 | 19.5GB | Quantized | Higher quality, multi-person |
| Multi INT8 LoRA | 19.5GB | Quantized+Style | Multi-person with style control |
| Single FP8 | 19.5GB | Quantized | Balanced quality/speed |
| Multi FP8 | 19.5GB | Quantized | Balanced quality/speed |
| Multi FP8 LoRA | 19.5GB | Quantized+Style | Multi-person with style |
| T5 FP8 | 6.73GB | Auxiliary | Text encoder (optional) |

### MultiTalk Models (6 models)

| Model | Size | Type | Use Case |
|-------|------|------|----------|
| 🎭 MultiTalk (Original) | 9.95GB | Standard | Multi-person conversation |
| MultiTalk INT8 | 19.1GB | Quantized | Higher quality |
| MultiTalk INT8 FusionX | 19.1GB | Fast | 2-3x faster (4-8 steps) |
| MultiTalk FP8 FusionX | 19.1GB | Fast | Balanced speed/quality |
| MultiTalk T5 INT8 | 6.73GB | Auxiliary | Text encoder |
| MultiTalk T5 FP8 | 6.73GB | Auxiliary | Text encoder |

**Total: 228GB** (all 16 models)

For detailed model selection guide, see [MODEL_GUIDE.md](MODEL_GUIDE.md)

## ⚙️ Configuration

### Nginx Reverse Proxy (Optional)

```nginx
server {
    listen 443 ssl;
    server_name infinitetalk.yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://localhost:8418;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Model Storage

Models are stored in `/app/models` inside the container, mapped to `/storage/infinitetalk/models` on the host.

```
models/
├── single/
│   └── infinitetalk.safetensors (11GB)
├── multi/
│   └── infinitetalk.safetensors (9.95GB)
├── quant_models/
│   ├── infinitetalk_single_int8.safetensors (19.5GB)
│   ├── infinitetalk_multi_fp8.safetensors (19.5GB)
│   └── ... (7 more models)
└── multitalk/
    ├── multitalk.safetensors (9.95GB)
    └── quant_models/ (5 models)
```

## 🎯 Usage

### Web Interface

1. **Select Model Type**: Choose InfiniteTalk or MultiTalk
2. **Select Model**: Pick from available models
3. **Load Model**: Click "🔄 Load Model" button
4. **Choose Mode**: Image-to-video or Video-to-video
5. **Upload Files**: Upload image/video and audio
6. **Generate**: Click "🎬 Generate Video"

### Features

- **Auto Model Management**: Models auto-download if missing
- **Smart Memory**: Auto-unload after 5 minutes of inactivity
- **Real-time Progress**: Download and generation progress tracking
- **Model Details**: View model info, size, and recommendations

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Gradio 6.0
- **Deep Learning**: PyTorch, Diffusers
- **Containerization**: Docker, Docker Compose
- **Web Server**: Nginx (reverse proxy)
- **Models**: InfiniteTalk, MultiTalk (MeiGen-AI)

## 📁 Project Structure

```
infinitetalk-deployment/
├── app.py                      # Main Gradio application
├── Dockerfile                  # Docker image definition
├── download_in_container.sh    # Auto-download script
├── download_models.sh          # Manual download script
├── MODEL_GUIDE.md             # Detailed model guide
├── README.md                  # English documentation
├── README_CN.md               # Chinese documentation
├── README_TW.md               # Traditional Chinese
├── README_JP.md               # Japanese documentation
└── models/                    # Model storage (gitignored)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Changelog

### v1.0.0 (2025-12-03)

**Initial Release**

- ✅ Complete deployment solution for InfiniteTalk & MultiTalk
- ✅ Docker containerization with auto-download
- ✅ All 16 official models support (228GB)
- ✅ Gradio web interface with real-time progress
- ✅ Auto model management (download, load, unload)
- ✅ Fixed file size calculation (GB vs GiB)
- ✅ Nginx reverse proxy configuration
- ✅ Multi-language documentation (EN/CN/TW/JP)

**Features**
- Auto-download missing models on startup
- Smart memory management (5min idle timeout)
- Real-time download progress tracking
- Model selection with detailed descriptions
- Support for both InfiniteTalk and MultiTalk
- INT8/FP8 quantized models support
- Image-to-video and video-to-video modes

**Technical Details**
- Fixed GB/GiB calculation inconsistency
- Optimized Docker CMD for proper startup
- Implemented model auto-unload mechanism
- Added comprehensive model metadata
- Created detailed model selection guide

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

The InfiniteTalk and MultiTalk models are licensed by MeiGen-AI under Apache 2.0.

## 🙏 Acknowledgments

- [MeiGen-AI](https://huggingface.co/MeiGen-AI) for the amazing InfiniteTalk and MultiTalk models
- [Gradio](https://gradio.app/) for the web interface framework
- All contributors and users of this project

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/infinitetalk-deployment&type=Date)](https://star-history.com/#neosun100/infinitetalk-deployment)

## 📱 Follow Us

![WeChat Official Account](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)

---

**Note**: This is a deployment wrapper. For the original InfiniteTalk/MultiTalk code, visit:
- InfiniteTalk: https://github.com/MeiGen-AI/InfiniteTalk
- MultiTalk: https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk
