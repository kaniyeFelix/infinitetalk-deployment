# 🎬 InfiniteTalk & MultiTalk 部署方案

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](Dockerfile)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)

MeiGen-AI 的 InfiniteTalk 和 MultiTalk 模型的生產級部署方案，具有自動模型管理、Docker 容器化和友好的 Gradio 界面。

## ✨ 功能特性

- 🚀 **一鍵部署** - 自動模型下載和 Docker 容器化
- 📦 **完整模型支援** - 全部 16 個官方模型（InfiniteTalk + MultiTalk）
- 🎯 **智能模型管理** - 自動下載缺失模型，5分鐘空閒自動卸載
- 🖥️ **現代化 Web UI** - 基於 Gradio 的界面，實時進度追蹤
- 🔄 **多模式支援** - 圖片轉視頻和視頻轉視頻生成
- 💾 **優化存儲** - 支援 INT8/FP8 量化模型（總計 228GB）
- 🌐 **生產就緒** - Nginx 反向代理，支援 SSL 和身份驗證

## 🚀 快速開始

```bash
# 克隆倉庫
git clone https://github.com/yourusername/infinitetalk-deployment.git
cd infinitetalk-deployment

# 使用 Docker 啟動
docker-compose up -d

# 訪問 UI：http://localhost:8418
```

## 📦 安裝部署

### 方式一：Docker 運行（推薦）

```bash
docker run -d \
  --name infinitetalk \
  --gpus all \
  -p 8418:7860 \
  -v /storage/infinitetalk/models:/app/models \
  infinitetalk:latest
```

### 方式二：直接運行

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動應用
python app.py
```

## 📚 模型指南

### InfiniteTalk 模型（10個）

- ⭐ 單人模式（原版）- 11GB，**推薦新手**
- ⭐ 多人模式（原版）- 9.95GB，**推薦**
- 單人/多人 INT8 - 19.5GB，更高質量
- 單人/多人 FP8 - 19.5GB，平衡質量/速度
- T5 FP8 - 6.73GB，文本編碼器

### MultiTalk 模型（6個）

- 🎭 MultiTalk（原版）- 9.95GB
- MultiTalk INT8/FP8 FusionX - 19.1GB，2-3倍速度
- MultiTalk T5 - 6.73GB，文本編碼器

**總計：228GB**（全部 16 個模型）

詳細指南請參見 [MODEL_GUIDE.md](MODEL_GUIDE.md)

## 🛠️ 技術棧

- **後端**：Python 3.10, Gradio 6.0
- **深度學習**：PyTorch, Diffusers
- **容器化**：Docker, Docker Compose
- **模型**：InfiniteTalk, MultiTalk (MeiGen-AI)

## 📝 更新日誌

### v1.0.0 (2025-12-03)

**首次發布**

- ✅ InfiniteTalk & MultiTalk 完整部署方案
- ✅ Docker 容器化，支援自動下載
- ✅ 全部 16 個官方模型支援（228GB）
- ✅ Gradio Web 界面，實時進度顯示
- ✅ 自動模型管理（下載、加載、卸載）
- ✅ 修復文件大小計算（GB vs GiB）
- ✅ 多語言文檔（英/中/繁/日）

## 📄 許可證

本項目採用 Apache License 2.0 許可證。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/infinitetalk-deployment&type=Date)](https://star-history.com/#yourusername/infinitetalk-deployment)

## 📱 關注公眾號

![公眾號](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)

---

**注意**：這是一個部署包裝器。原始代碼請訪問：
- InfiniteTalk: https://github.com/MeiGen-AI/InfiniteTalk
- MultiTalk: https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk
