#!/bin/bash
cd /storage/infinitetalk/models

echo "开始下载 MeiGen-MultiTalk 模型..."

# 创建目录
mkdir -p multitalk/quant_models

# 下载原版模型
echo "=== 下载 MultiTalk 原版模型 (9.95GB) ==="
cd multitalk
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/multitalk.safetensors

# 下载量化模型
echo "=== 下载 MultiTalk 量化模型 ==="
cd quant_models

echo "下载 dit_model_int8.safetensors (19.1GB)..."
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/dit_model_int8.safetensors
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/dit_model_map_int8.json

echo "下载 quant_model_int8_FusionX.safetensors (19.1GB)..."
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_int8_FusionX.safetensors
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quantization_map_int8_FusionX.json

echo "下载 quant_model_fp8_FusionX.safetensors (19.1GB)..."
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_fp8_FusionX.safetensors
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quantization_map_fp8_FusionX.json

echo "下载 t5_int8.safetensors (6.73GB)..."
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_int8.safetensors
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_map_int8.json

echo "下载 t5_fp8.safetensors (6.73GB)..."
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_fp8.safetensors
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_map_fp8.json

echo "=== MultiTalk 模型下载完成！==="
cd /storage/infinitetalk/models
du -sh multitalk
