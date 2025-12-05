#!/bin/bash
# 自动完成所有模型下载

cd /app/models
LOG="/tmp/download_progress.log"

echo "开始下载所有剩余模型 $(date)" | tee -a $LOG

# 删除所有不完整的文件
rm -f multi/infinitetalk.safetensors
rm -f quant_models/infinitetalk_*.safetensors
rm -f quant_models/t5_fp8.safetensors
rm -f multitalk/multitalk.safetensors
rm -f multitalk/quant_models/*.safetensors

# 下载函数
download_file() {
    local url=$1
    local output=$2
    local name=$3
    
    echo "[$name] 开始下载 $(date)" | tee -a $LOG
    if wget -c "$url" -O "$output" 2>&1 | tee -a $LOG; then
        echo "[$name] 完成 $(date)" | tee -a $LOG
        return 0
    else
        echo "[$name] 失败 $(date)" | tee -a $LOG
        return 1
    fi
}

# InfiniteTalk 模型
download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/multi/infinitetalk.safetensors" "multi/infinitetalk.safetensors" "多人模式原版"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_single_int8.safetensors" "quant_models/infinitetalk_single_int8.safetensors" "单人INT8"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_single_int8_lora.safetensors" "quant_models/infinitetalk_single_int8_lora.safetensors" "单人INT8 LoRA"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_int8.safetensors" "quant_models/infinitetalk_multi_int8.safetensors" "多人INT8"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_int8_lora.safetensors" "quant_models/infinitetalk_multi_int8_lora.safetensors" "多人INT8 LoRA"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_single_fp8.safetensors" "quant_models/infinitetalk_single_fp8.safetensors" "单人FP8"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_fp8.safetensors" "quant_models/infinitetalk_multi_fp8.safetensors" "多人FP8"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_fp8_lora.safetensors" "quant_models/infinitetalk_multi_fp8_lora.safetensors" "多人FP8 LoRA"

download_file "https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/t5_fp8.safetensors" "quant_models/t5_fp8.safetensors" "T5 FP8"

# MultiTalk 模型
download_file "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/multitalk.safetensors" "multitalk/multitalk.safetensors" "MultiTalk原版"

download_file "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/dit_model_int8.safetensors" "multitalk/quant_models/dit_model_int8.safetensors" "MultiTalk INT8"

download_file "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_int8_FusionX.safetensors" "multitalk/quant_models/quant_model_int8_FusionX.safetensors" "MultiTalk INT8 FusionX"

download_file "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_fp8_FusionX.safetensors" "multitalk/quant_models/quant_model_fp8_FusionX.safetensors" "MultiTalk FP8 FusionX"

download_file "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_int8.safetensors" "multitalk/quant_models/t5_int8.safetensors" "MultiTalk T5 INT8"

download_file "https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_fp8.safetensors" "multitalk/quant_models/t5_fp8.safetensors" "MultiTalk T5 FP8"

echo "所有下载完成！$(date)" | tee -a $LOG
