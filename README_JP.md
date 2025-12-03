# 🎬 InfiniteTalk & MultiTalk デプロイメント

[English](README.md) | [简体中文](README_CN.md) | [繁體中文](README_TW.md) | [日本語](README_JP.md)

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](Dockerfile)
[![Python](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/)

MeiGen-AIのInfiniteTalkとMultiTalkモデルのプロダクショングレードのデプロイメントソリューション。自動モデル管理、Dockerコンテナ化、使いやすいGradioインターフェースを備えています。

## ✨ 機能

- 🚀 **ワンクリックデプロイ** - 自動モデルダウンロードとDockerコンテナ化
- 📦 **完全なモデルサポート** - 全16の公式モデル（InfiniteTalk + MultiTalk）
- 🎯 **スマートモデル管理** - 不足モデルの自動ダウンロード、5分間のアイドル後自動アンロード
- 🖥️ **モダンなWeb UI** - Gradioベースのインターフェース、リアルタイム進捗追跡
- 🔄 **マルチモードサポート** - 画像から動画、動画から動画への生成
- 💾 **最適化されたストレージ** - INT8/FP8量子化モデルサポート（合計228GB）
- 🌐 **プロダクション対応** - Nginxリバースプロキシ、SSL、認証サポート

## 🚀 クイックスタート

```bash
# リポジトリをクローン
git clone https://github.com/neosun100/infinitetalk-deployment.git
cd infinitetalk-deployment

# Dockerで起動
docker-compose up -d

# UIにアクセス：http://localhost:8418
```

## 📦 インストール

### 方法1：Docker実行（推奨）

```bash
docker run -d \
  --name infinitetalk \
  --gpus all \
  -p 8418:7860 \
  -v /storage/infinitetalk/models:/app/models \
  infinitetalk:latest
```

### 方法2：直接実行

```bash
# 依存関係をインストール
pip install -r requirements.txt

# アプリケーションを起動
python app.py
```

## 📚 モデルガイド

### InfiniteTalkモデル（10個）

- ⭐ シングル（オリジナル）- 11GB、**初心者におすすめ**
- ⭐ マルチ（オリジナル）- 9.95GB、**おすすめ**
- シングル/マルチ INT8 - 19.5GB、高品質
- シングル/マルチ FP8 - 19.5GB、品質/速度のバランス
- T5 FP8 - 6.73GB、テキストエンコーダー

### MultiTalkモデル（6個）

- 🎭 MultiTalk（オリジナル）- 9.95GB
- MultiTalk INT8/FP8 FusionX - 19.1GB、2-3倍高速
- MultiTalk T5 - 6.73GB、テキストエンコーダー

**合計：228GB**（全16モデル）

詳細なガイドは [MODEL_GUIDE.md](MODEL_GUIDE.md) を参照してください

## 🛠️ 技術スタック

- **バックエンド**：Python 3.10, Gradio 6.0
- **ディープラーニング**：PyTorch, Diffusers
- **コンテナ化**：Docker, Docker Compose
- **モデル**：InfiniteTalk, MultiTalk (MeiGen-AI)

## 📝 変更履歴

### v1.0.0 (2025-12-03)

**初回リリース**

- ✅ InfiniteTalk & MultiTalk完全デプロイメントソリューション
- ✅ Dockerコンテナ化、自動ダウンロードサポート
- ✅ 全16公式モデルサポート（228GB）
- ✅ Gradio Webインターフェース、リアルタイム進捗表示
- ✅ 自動モデル管理（ダウンロード、ロード、アンロード）
- ✅ ファイルサイズ計算の修正（GB vs GiB）
- ✅ 多言語ドキュメント（英/中/繁/日）

## 📄 ライセンス

このプロジェクトはApache License 2.0の下でライセンスされています。

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=neosun100/infinitetalk-deployment&type=Date)](https://star-history.com/#neosun100/infinitetalk-deployment)

## 📱 公式アカウントをフォロー

![WeChat公式アカウント](https://img.aws.xin/uPic/扫码_搜索联合传播样式-标准色版.png)

---

**注意**：これはデプロイメントラッパーです。オリジナルコードは以下を参照：
- InfiniteTalk: https://github.com/MeiGen-AI/InfiniteTalk
- MultiTalk: https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk
