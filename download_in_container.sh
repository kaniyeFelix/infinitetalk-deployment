#!/bin/bash
# 容器内自动下载脚本

cd /app/models

# 检查并下载 InfiniteTalk 模型
check_and_download() {
    local file=$1
    local url=$2
    
    if [ ! -f "$file" ] || [ $(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null) -lt 1000000 ]; then
        echo "下载: $file"
        wget -c -q --show-progress "$url" -O "$file" 2>&1 | tail -1
    fi
}

# InfiniteTalk 原版模型
mkdir -p single multi quant_models

check_and_download "single/infinitetalk.safetensors" "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/single/infinitetalk.safetensors"
check_and_download "multi/infinitetalk.safetensors" "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/multi/infinitetalk.safetensors"

# InfiniteTalk 量化模型
for model in infinitetalk_single_int8 infinitetalk_single_int8_lora infinitetalk_multi_int8 infinitetalk_multi_int8_lora infinitetalk_single_fp8 infinitetalk_multi_fp8 infinitetalk_multi_fp8_lora; do
    check_and_download "quant_models/${model}.safetensors" "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/${model}.safetensors"
done

check_and_download "quant_models/t5_fp8.safetensors" "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/t5_fp8.safetensors"

# MultiTalk 模型
mkdir -p multitalk/quant_models

check_and_download "multitalk/multitalk.safetensors" "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/multitalk.safetensors"
check_and_download "multitalk/quant_models/dit_model_int8.safetensors" "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/dit_model_int8.safetensors"
check_and_download "multitalk/quant_models/quant_model_int8_FusionX.safetensors" "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_int8_FusionX.safetensors"
check_and_download "multitalk/quant_models/quant_model_fp8_FusionX.safetensors" "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_fp8_FusionX.safetensors"
check_and_download "multitalk/quant_models/t5_int8.safetensors" "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_int8.safetensors"
check_and_download "multitalk/quant_models/t5_fp8.safetensors" "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_fp8.safetensors"

echo "下载检查完成"
