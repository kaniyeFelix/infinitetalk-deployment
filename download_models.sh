#!/bin/bash
cd /storage/infinitetalk/models

echo "开始下载所有 InfiniteTalk 模型到 /storage..."

# 创建目录
mkdir -p single multi quant_models

# 下载原版单人模型
echo "=== 下载原版单人模型 (9.95GB) ==="
cd single
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/single/infinitetalk.safetensors

# 下载原版多人模型
echo "=== 下载原版多人模型 (9.95GB) ==="
cd ../multi
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/multi/infinitetalk.safetensors

# 下载量化模型
echo "=== 下载量化模型 ==="
cd ../quant_models

# INT8 量化模型
for model in infinitetalk_single_int8 infinitetalk_single_int8_lora infinitetalk_multi_int8 infinitetalk_multi_int8_lora; do
    echo "下载 ${model}.safetensors (19.5GB)..."
    wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/${model}.safetensors
    wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/${model}.json
done

# FP8 量化模型
for model in infinitetalk_single_fp8 infinitetalk_multi_fp8 infinitetalk_multi_fp8_lora; do
    echo "下载 ${model}.safetensors (19.5GB)..."
    wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/${model}.safetensors
    wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/${model}.json
done

# T5 模型
echo "下载 t5_fp8.safetensors (6.73GB)..."
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/t5_fp8.safetensors
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/t5_map_fp8.json

echo "=== 所有模型下载完成！==="
cd /storage/infinitetalk/models
du -sh *
