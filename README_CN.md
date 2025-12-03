# 🎬 InfiniteTalk & MultiTalk 部署方案

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](Dockerfile)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)

MeiGen-AI 的 InfiniteTalk 和 MultiTalk 模型的生产级部署方案，具有自动模型管理、Docker 容器化和友好的 Gradio 界面。

## ✨ 功能特性

- 🚀 **一键部署** - 自动模型下载和 Docker 容器化
- 📦 **完整模型支持** - 全部 16 个官方模型（InfiniteTalk + MultiTalk）
- 🎯 **智能模型管理** - 自动下载缺失模型，5分钟空闲自动卸载
- 🖥️ **现代化 Web UI** - 基于 Gradio 的界面，实时进度跟踪
- 🔄 **多模式支持** - 图片转视频和视频转视频生成
- 💾 **优化存储** - 支持 INT8/FP8 量化模型（总计 228GB）
- 🌐 **生产就绪** - Nginx 反向代理，支持 SSL 和身份验证

## 📋 目录

- [功能特性](#-功能特性)
- [快速开始](#-快速开始)
- [安装部署](#-安装部署)
  - [方式一：Docker 运行（推荐）](#方式一docker-运行推荐)
  - [方式二：直接运行](#方式二直接运行)
- [模型指南](#-模型指南)
- [配置说明](#-配置说明)
- [使用方法](#-使用方法)
- [技术栈](#-技术栈)
- [项目结构](#-项目结构)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/yourusername/infinitetalk-deployment.git
cd infinitetalk-deployment

# 使用 Docker 启动
docker-compose up -d

# 访问 UI：http://localhost:8418
```

## 📦 安装部署

### 方式一：Docker 运行（推荐）

#### 前置条件
- Docker >= 20.10
- Docker Compose >= 2.0
- NVIDIA GPU 支持 CUDA
- 已安装 nvidia-docker2

#### 步骤 1：拉取 Docker 镜像

```bash
docker pull infinitetalk:latest
```

#### 步骤 2：运行容器

```bash
docker run -d \
  --name infinitetalk \
  --gpus all \
  -p 8418:7860 \
  -v /storage/infinitetalk/models:/app/models \
  infinitetalk:latest
```

#### 步骤 3：验证

```bash
# 检查容器状态
docker ps | grep infinitetalk

# 查看日志
docker logs -f infinitetalk

# 访问 UI
curl http://localhost:8418
```

#### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `GRADIO_SERVER_PORT` | Web UI 端口 | `7860` |
| `IDLE_TIMEOUT` | 模型自动卸载超时（秒） | `300` |

#### Docker Compose 示例

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

### 方式二：直接运行

#### 前置条件
- Python 3.10+
- CUDA 11.8+ / CUDA 12.1+
- 32GB+ 内存
- 500GB+ 可用磁盘空间

#### 步骤 1：安装依赖

```bash
pip install -r requirements.txt
```

#### 步骤 2：下载模型

模型会在首次运行时自动下载。你也可以手动下载：

```bash
# 下载所有模型（228GB）
bash download_models.sh

# 或下载特定模型
bash download_multitalk.sh
```

#### 步骤 3：启动应用

```bash
python app.py
```

应用将在 `http://localhost:7860` 可用

## 📚 模型指南

### InfiniteTalk 模型（10个）

| 模型 | 大小 | 类型 | 使用场景 |
|------|------|------|----------|
| ⭐ 单人模式（原版） | 11GB | 标准 | 单人说话，**推荐新手** |
| ⭐ 多人模式（原版） | 9.95GB | 标准 | 多人对话，**推荐** |
| 单人模式 INT8 | 19.5GB | 量化 | 更高质量，单人 |
| 单人模式 INT8 LoRA | 19.5GB | 量化+风格 | 支持风格控制 |
| 多人模式 INT8 | 19.5GB | 量化 | 更高质量，多人 |
| 多人模式 INT8 LoRA | 19.5GB | 量化+风格 | 多人风格控制 |
| 单人模式 FP8 | 19.5GB | 量化 | 平衡质量/速度 |
| 多人模式 FP8 | 19.5GB | 量化 | 平衡质量/速度 |
| 多人模式 FP8 LoRA | 19.5GB | 量化+风格 | 多人风格 |
| T5 FP8 | 6.73GB | 辅助 | 文本编码器（可选） |

### MultiTalk 模型（6个）

| 模型 | 大小 | 类型 | 使用场景 |
|------|------|------|----------|
| 🎭 MultiTalk（原版） | 9.95GB | 标准 | 多人对话 |
| MultiTalk INT8 | 19.1GB | 量化 | 更高质量 |
| MultiTalk INT8 FusionX | 19.1GB | 快速 | 2-3倍速度（4-8步） |
| MultiTalk FP8 FusionX | 19.1GB | 快速 | 平衡速度/质量 |
| MultiTalk T5 INT8 | 6.73GB | 辅助 | 文本编码器 |
| MultiTalk T5 FP8 | 6.73GB | 辅助 | 文本编码器 |

**总计：228GB**（全部 16 个模型）

详细模型选择指南请参见 [MODEL_GUIDE.md](MODEL_GUIDE.md)

## ⚙️ 配置说明

### Nginx 反向代理（可选）

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

### 模型存储

模型存储在容器内的 `/app/models`，映射到宿主机的 `/storage/infinitetalk/models`。

```
models/
├── single/
│   └── infinitetalk.safetensors (11GB)
├── multi/
│   └── infinitetalk.safetensors (9.95GB)
├── quant_models/
│   ├── infinitetalk_single_int8.safetensors (19.5GB)
│   ├── infinitetalk_multi_fp8.safetensors (19.5GB)
│   └── ... (另外7个模型)
└── multitalk/
    ├── multitalk.safetensors (9.95GB)
    └── quant_models/ (5个模型)
```

## 🎯 使用方法

### Web 界面

1. **选择模型类型**：选择 InfiniteTalk 或 MultiTalk
2. **选择模型**：从可用模型中选择
3. **加载模型**：点击"🔄 加载模型"按钮
4. **选择模式**：图片转视频或视频转视频
5. **上传文件**：上传图片/视频和音频
6. **生成**：点击"🎬 生成视频"

### 功能

- **自动模型管理**：缺失模型自动下载
- **智能内存**：5分钟不活动后自动卸载
- **实时进度**：下载和生成进度跟踪
- **模型详情**：查看模型信息、大小和推荐

## 🛠️ 技术栈

- **后端**：Python 3.10, Gradio 6.0
- **深度学习**：PyTorch, Diffusers
- **容器化**：Docker, Docker Compose
- **Web 服务器**：Nginx（反向代理）
- **模型**：InfiniteTalk, MultiTalk (MeiGen-AI)

## 📁 项目结构

```
infinitetalk-deployment/
├── app.py                      # 主 Gradio 应用
├── Dockerfile                  # Docker 镜像定义
├── download_in_container.sh    # 自动下载脚本
├── download_models.sh          # 手动下载脚本
├── MODEL_GUIDE.md             # 详细模型指南
├── README.md                  # 英文文档
├── README_CN.md               # 中文文档
├── README_TW.md               # 繁体中文
├── README_JP.md               # 日文文档
└── models/                    # 模型存储（已忽略）
```

## 🤝 贡献指南

欢迎贡献！请随时提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 更新日志

### v1.0.0 (2025-12-03)

**首次发布**

- ✅ InfiniteTalk & MultiTalk 完整部署方案
- ✅ Docker 容器化，支持自动下载
- ✅ 全部 16 个官方模型支持（228GB）
- ✅ Gradio Web 界面，实时进度显示
- ✅ 自动模型管理（下载、加载、卸载）
- ✅ 修复文件大小计算（GB vs GiB）
- ✅ Nginx 反向代理配置
- ✅ 多语言文档（英/中/繁/日）

**功能特性**
- 启动时自动下载缺失模型
- 智能内存管理（5分钟空闲超时）
- 实时下载进度跟踪
- 模型选择与详细描述
- 支持 InfiniteTalk 和 MultiTalk
- INT8/FP8 量化模型支持
- 图片转视频和视频转视频模式

**技术细节**
- 修复 GB/GiB 计算不一致问题
- 优化 Docker CMD 正确启动
- 实现模型自动卸载机制
- 添加完整模型元数据
- 创建详细模型选择指南

## 📄 许可证

本项目采用 Apache License 2.0 许可证 - 详见 [LICENSE](LICENSE) 文件。

InfiniteTalk 和 MultiTalk 模型由 MeiGen-AI 以 Apache 2.0 许可。

## 🙏 致谢

- [MeiGen-AI](https://huggingface.co/MeiGen-AI) 提供的优秀 InfiniteTalk 和 MultiTalk 模型
- [Gradio](https://gradio.app/) 提供的 Web 界面框架
- 本项目的所有贡献者和用户

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/infinitetalk-deployment&type=Date)](https://star-history.com/#yourusername/infinitetalk-deployment)

## 📱 关注公众号

![公众号](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)

---

**注意**：这是一个部署包装器。原始 InfiniteTalk/MultiTalk 代码请访问：
- InfiniteTalk: https://github.com/MeiGen-AI/InfiniteTalk
- MultiTalk: https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk
