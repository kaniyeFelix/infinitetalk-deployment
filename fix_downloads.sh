#!/bin/bash
cd /app/models

# 删除所有93%的不完整文件并重新下载
rm -f multi/infinitetalk.safetensors
rm -f quant_models/infinitetalk_*.safetensors
rm -f quant_models/t5_fp8.safetensors
rm -f multitalk/multitalk.safetensors
rm -f multitalk/quant_models/*.safetensors

# 重新下载
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/multi/infinitetalk.safetensors -O multi/infinitetalk.safetensors &
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_single_int8.safetensors -O quant_models/infinitetalk_single_int8.safetensors &
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_single_int8_lora.safetensors -O quant_models/infinitetalk_single_int8_lora.safetensors &
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_int8.safetensors -O quant_models/infinitetalk_multi_int8.safetensors &
wait
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_int8_lora.safetensors -O quant_models/infinitetalk_multi_int8_lora.safetensors &
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_single_fp8.safetensors -O quant_models/infinitetalk_single_fp8.safetensors &
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_fp8.safetensors -O quant_models/infinitetalk_multi_fp8.safetensors &
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/infinitetalk_multi_fp8_lora.safetensors -O quant_models/infinitetalk_multi_fp8_lora.safetensors &
wait
wget -c https://huggingface.co/MeiGen-AI/InfiniteTalk/resolve/main/quant_models/t5_fp8.safetensors -O quant_models/t5_fp8.safetensors &
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/multitalk.safetensors -O multitalk/multitalk.safetensors &
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/dit_model_int8.safetensors -O multitalk/quant_models/dit_model_int8.safetensors &
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_int8_FusionX.safetensors -O multitalk/quant_models/quant_model_int8_FusionX.safetensors &
wait
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/quant_model_fp8_FusionX.safetensors -O multitalk/quant_models/quant_model_fp8_FusionX.safetensors &
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_int8.safetensors -O multitalk/quant_models/t5_int8.safetensors &
wget -c https://huggingface.co/MeiGen-AI/MeiGen-MultiTalk/resolve/main/quant_models/t5_fp8.safetensors -O multitalk/quant_models/t5_fp8.safetensors &
wait

echo "所有下载完成"
