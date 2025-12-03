import gradio as gr
import os
import gc
import torch
from threading import Timer, Thread
import subprocess
import time

# 所有可用模型配置
MODELS = {
    # InfiniteTalk 原版模型
    "single_original": {
        "name": "⭐ 单人模式（原版）",
        "path": "/app/models/single/infinitetalk.safetensors",
        "description": "原版单人模式，体积小，速度快",
        "size": "9.95GB",
        "type": "InfiniteTalk",
        "quality": "标准",
        "recommended": True,
        "use_case": "适合单人说话视频，推荐新手使用"
    },
    "multi_original": {
        "name": "⭐ 多人模式（原版）",
        "path": "/app/models/multi/infinitetalk.safetensors",
        "description": "原版多人模式，支持多人对话场景",
        "size": "9.95GB",
        "type": "InfiniteTalk",
        "quality": "标准",
        "recommended": True,
        "use_case": "适合多人对话视频，推荐新手使用"
    },
    
    # InfiniteTalk INT8 量化模型
    "single_int8": {
        "name": "单人模式 INT8",
        "path": "/app/models/quant_models/infinitetalk_single_int8.safetensors",
        "description": "INT8量化，质量更高但体积更大",
        "size": "19.5GB",
        "type": "InfiniteTalk",
        "quality": "高质量",
        "recommended": False,
        "use_case": "追求高质量单人视频"
    },
    "single_int8_lora": {
        "name": "单人模式 INT8 LoRA",
        "path": "/app/models/quant_models/infinitetalk_single_int8_lora.safetensors",
        "description": "INT8 + LoRA，支持风格控制",
        "size": "19.5GB",
        "type": "InfiniteTalk",
        "quality": "高质量+风格",
        "recommended": False,
        "use_case": "需要风格控制的单人视频"
    },
    "multi_int8": {
        "name": "多人模式 INT8",
        "path": "/app/models/quant_models/infinitetalk_multi_int8.safetensors",
        "description": "INT8量化，多人高质量",
        "size": "19.5GB",
        "type": "InfiniteTalk",
        "quality": "高质量",
        "recommended": False,
        "use_case": "追求高质量多人视频"
    },
    "multi_int8_lora": {
        "name": "多人模式 INT8 LoRA",
        "path": "/app/models/quant_models/infinitetalk_multi_int8_lora.safetensors",
        "description": "INT8 + LoRA，多人风格控制",
        "size": "19.5GB",
        "type": "InfiniteTalk",
        "quality": "高质量+风格",
        "recommended": False,
        "use_case": "需要风格控制的多人视频"
    },
    
    # InfiniteTalk FP8 量化模型
    "single_fp8": {
        "name": "单人模式 FP8",
        "path": "/app/models/quant_models/infinitetalk_single_fp8.safetensors",
        "description": "FP8量化，平衡质量与速度",
        "size": "19.5GB",
        "type": "InfiniteTalk",
        "quality": "高质量",
        "recommended": False,
        "use_case": "平衡质量与性能的单人视频"
    },
    "multi_fp8": {
        "name": "多人模式 FP8",
        "path": "/app/models/quant_models/infinitetalk_multi_fp8.safetensors",
        "description": "FP8量化，多人平衡模式",
        "size": "19.5GB",
        "type": "InfiniteTalk",
        "quality": "高质量",
        "recommended": False,
        "use_case": "平衡质量与性能的多人视频"
    },
    "multi_fp8_lora": {
        "name": "多人模式 FP8 LoRA",
        "path": "/app/models/quant_models/infinitetalk_multi_fp8_lora.safetensors",
        "description": "FP8 + LoRA，多人风格平衡",
        "size": "19.5GB",
        "type": "InfiniteTalk",
        "quality": "高质量+风格",
        "recommended": False,
        "use_case": "需要风格控制且注重性能的多人视频"
    },
    
    # T5 模型
    "t5_fp8": {
        "name": "T5 FP8（辅助）",
        "path": "/app/models/quant_models/t5_fp8.safetensors",
        "description": "T5文本编码器，辅助模型",
        "size": "6.73GB",
        "type": "InfiniteTalk",
        "quality": "辅助",
        "recommended": False,
        "use_case": "配合主模型使用的文本编码器"
    },
    
    # MeiGen-MultiTalk 模型
    "multitalk_original": {
        "name": "🎭 MultiTalk（原版）",
        "path": "/app/models/multitalk/multitalk.safetensors",
        "description": "MultiTalk原版，多人对话专用",
        "size": "9.95GB",
        "type": "MultiTalk",
        "quality": "标准",
        "recommended": False,
        "use_case": "专注于多人对话场景，支持更复杂的交互"
    },
    "multitalk_int8": {
        "name": "MultiTalk INT8",
        "path": "/app/models/multitalk/quant_models/dit_model_int8.safetensors",
        "description": "MultiTalk INT8量化",
        "size": "19.1GB",
        "type": "MultiTalk",
        "quality": "高质量",
        "recommended": False,
        "use_case": "高质量多人对话视频"
    },
    "multitalk_int8_fusion": {
        "name": "MultiTalk INT8 FusionX",
        "path": "/app/models/multitalk/quant_models/quant_model_int8_FusionX.safetensors",
        "description": "MultiTalk INT8 + FusionX加速",
        "size": "19.1GB",
        "type": "MultiTalk",
        "quality": "高质量+快速",
        "recommended": False,
        "use_case": "需要快速生成的高质量多人视频"
    },
    "multitalk_fp8_fusion": {
        "name": "MultiTalk FP8 FusionX",
        "path": "/app/models/multitalk/quant_models/quant_model_fp8_FusionX.safetensors",
        "description": "MultiTalk FP8 + FusionX加速",
        "size": "19.1GB",
        "type": "MultiTalk",
        "quality": "高质量+快速",
        "recommended": False,
        "use_case": "平衡质量与速度的多人视频"
    },
    "multitalk_t5_int8": {
        "name": "MultiTalk T5 INT8",
        "path": "/app/models/multitalk/quant_models/t5_int8.safetensors",
        "description": "MultiTalk T5编码器 INT8",
        "size": "6.73GB",
        "type": "MultiTalk",
        "quality": "辅助",
        "recommended": False,
        "use_case": "配合MultiTalk使用"
    },
    "multitalk_t5_fp8": {
        "name": "MultiTalk T5 FP8",
        "path": "/app/models/multitalk/quant_models/t5_fp8.safetensors",
        "description": "MultiTalk T5编码器 FP8",
        "size": "6.73GB",
        "type": "MultiTalk",
        "quality": "辅助",
        "recommended": False,
        "use_case": "配合MultiTalk使用"
    }
}

current_model = None
model_pipeline = None
idle_timer = None
IDLE_TIMEOUT = 300
download_process = None

def get_file_size_gb(filepath):
    """获取文件大小（GB）"""
    if os.path.exists(filepath):
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1000**3)  # 使用GB而不是GiB
    return 0

def check_and_download_models():
    """检查并自动下载缺失的模型"""
    missing_models = []
    for key, info in MODELS.items():
        if not os.path.exists(info["path"]):
            missing_models.append((key, info))
    
    if missing_models:
        print(f"发现 {len(missing_models)} 个模型需要下载")
        # 启动后台下载
        Thread(target=download_missing_models, args=(missing_models,), daemon=True).start()

def download_missing_models(models_list):
    """后台下载缺失的模型"""
    for key, info in models_list:
        print(f"开始下载: {info['name']}")
        # 这里添加实际的下载逻辑
        # 使用 wget 或 huggingface-cli 下载
        time.sleep(1)  # 占位符

def get_download_progress():
    """获取下载进度"""
    progress_info = []
    
    for key, info in MODELS.items():
        path = info["path"]
        expected_size = float(info["size"].replace("GB", ""))
        
        if os.path.exists(path):
            current_size = get_file_size_gb(path)
            if current_size < expected_size * 0.95:  # 未完成下载
                progress = (current_size / expected_size) * 100
                progress_info.append(f"⏳ {info['name']}: {current_size:.1f}GB / {expected_size}GB ({progress:.1f}%)")
            else:
                progress_info.append(f"✅ {info['name']}: 已完成")
        else:
            progress_info.append(f"⏸️ {info['name']}: 未开始")
    
    return "\n".join(progress_info) if progress_info else "所有模型已就绪"

def check_model_exists(model_key):
    return os.path.exists(MODELS[model_key]["path"])

def get_model_status():
    infinitetalk_list = []
    multitalk_list = []
    
    for key, info in MODELS.items():
        exists = check_model_exists(key)
        status = "✅" if exists else "⏳"
        line = f"{status} {info['name']} ({info['size']})"
        
        if info["type"] == "InfiniteTalk":
            infinitetalk_list.append(line)
        else:
            multitalk_list.append(line)
    
    result = "=== InfiniteTalk 模型 ===\n" + "\n".join(infinitetalk_list)
    result += "\n\n=== MultiTalk 模型 ===\n" + "\n".join(multitalk_list)
    return result

def unload_model():
    global model_pipeline, current_model
    if model_pipeline is not None:
        del model_pipeline
        model_pipeline = None
        current_model = None
        gc.collect()
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        print("模型已从显存中释放")

def reset_idle_timer():
    global idle_timer
    if idle_timer:
        idle_timer.cancel()
    idle_timer = Timer(IDLE_TIMEOUT, unload_model)
    idle_timer.start()

def load_model(model_key):
    global current_model
    if not model_key:
        return "⚠️ 请选择一个模型"
    
    if not check_model_exists(model_key):
        return f"❌ 模型文件不存在，请等待下载完成\n路径: {MODELS[model_key]['path']}"
    
    try:
        if current_model and current_model != model_key:
            unload_model()
        
        current_model = model_key
        reset_idle_timer()
        info = MODELS[model_key]
        return f"✅ 已加载: {info['name']}\n类型: {info['type']}\n质量: {info['quality']}\n路径: {info['path']}\n\n💡 提示：5分钟不使用将自动释放显存"
    except Exception as e:
        return f"❌ 加载失败: {str(e)}"

def generate_video(mode, input_image, input_video, input_audio, input_text):
    if not current_model:
        return None, "⚠️ 请先选择并加载模型"
    
    reset_idle_timer()
    info = MODELS[current_model]
    
    if mode == "image_to_video":
        if not input_image or not input_audio:
            return None, "⚠️ 图片转视频模式需要上传图片和音频"
        return None, f"使用 {info['name']} 生成视频\n模式: 图片转视频\n类型: {info['type']}\n文本: {input_text[:50] if input_text else '无'}..."
    else:
        if not input_video or not input_audio:
            return None, "⚠️ 视频转视频模式需要上传视频和音频"
        return None, f"使用 {info['name']} 生成视频\n模式: 视频转视频（口型同步）\n类型: {info['type']}\n文本: {input_text[:50] if input_text else '无'}..."

with gr.Blocks(title="InfiniteTalk & MultiTalk 视频生成") as demo:
    gr.Markdown("# 🎬 InfiniteTalk & MultiTalk 音频驱动视频生成系统")
    gr.Markdown("支持图片转视频和视频口型同步，无限长度视频生成 | ⭐ 标记为推荐模型")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📦 模型管理")
            
            # 按类型分组显示
            infinitetalk_choices = [(v["name"], k) for k, v in MODELS.items() if v["type"] == "InfiniteTalk"]
            multitalk_choices = [(v["name"], k) for k, v in MODELS.items() if v["type"] == "MultiTalk"]
            
            model_type = gr.Radio(
                choices=["InfiniteTalk", "MultiTalk"],
                label="模型系列",
                value="InfiniteTalk"
            )
            
            model_dropdown = gr.Dropdown(
                choices=infinitetalk_choices,
                label="选择模型",
                value=None
            )
            
            model_info = gr.Textbox(label="模型详情", interactive=False, lines=6)
            
            with gr.Row():
                load_btn = gr.Button("🔄 加载模型", variant="primary")
                refresh_btn = gr.Button("🔍 刷新状态")
                unload_btn = gr.Button("🗑️ 释放显存")
            
            status = gr.Textbox(label="加载状态", interactive=False, lines=5)
            model_status = gr.Textbox(label="所有模型状态", interactive=False, lines=18, value=get_model_status())
            
            gr.Markdown("### 📥 下载进度")
            download_progress = gr.Textbox(label="实时下载进度", interactive=False, lines=10, value=get_download_progress())
            refresh_download_btn = gr.Button("🔄 刷新下载进度")
            
        with gr.Column(scale=2):
            gr.Markdown("### 🎥 视频生成")
            
            mode = gr.Radio(
                choices=[("图片转视频", "image_to_video"), ("视频转视频（口型同步）", "video_to_video")],
                label="生成模式",
                value="image_to_video"
            )
            
            with gr.Row():
                with gr.Column():
                    input_image = gr.Image(label="输入图片（图片转视频模式）", type="filepath")
                    input_video = gr.Video(label="输入视频（视频转视频模式）")
                
                with gr.Column():
                    input_audio = gr.Audio(label="输入音频（必需）", type="filepath")
                    input_text = gr.Textbox(label="文本提示（可选）", placeholder="输入描述文本...", lines=3)
            
            generate_btn = gr.Button("🎬 生成视频", variant="primary", size="lg")
            
            output_video = gr.Video(label="生成的视频")
            output_status = gr.Textbox(label="生成状态", interactive=False, lines=3)
    
    with gr.Accordion("📋 模型详细说明", open=False):
        gr.Markdown("""
        ## InfiniteTalk 系列（推荐新手）
        
        ### ⭐ 推荐模型
        - **单人模式（原版）**: 体积小（9.95GB），速度快，适合单人说话视频，**推荐新手首选**
        - **多人模式（原版）**: 体积小（9.95GB），支持多人对话，**推荐多人场景首选**
        
        ### 高质量模型（追求质量）
        - **INT8 系列**: 体积大（19.5GB），质量更高，适合追求高质量输出
        - **FP8 系列**: 体积大（19.5GB），平衡质量与速度
        - **LoRA 系列**: 支持风格控制，适合需要特定风格的场景
        
        ### 辅助模型
        - **T5 FP8**: 文本编码器，配合主模型使用
        
        ---
        
        ## MultiTalk 系列（专业用户）
        
        ### 特点
        - 专注于多人对话场景
        - 支持更复杂的交互控制
        - 提供 FusionX 加速版本
        
        ### 模型选择
        - **原版**: 标准质量，适合测试
        - **INT8/FP8 FusionX**: 高质量 + 快速生成
        - **T5 模型**: 配合主模型使用
        
        ---
        
        ## 使用建议
        
        1. **新手**: 使用 ⭐ 标记的原版模型
        2. **追求质量**: 使用 INT8 或 FP8 量化模型
        3. **需要风格**: 使用 LoRA 系列
        4. **多人对话**: InfiniteTalk 多人模式或 MultiTalk
        5. **快速生成**: MultiTalk FusionX 系列
        """)
    
    with gr.Accordion("💡 使用说明", open=False):
        gr.Markdown("""
        ### 功能说明
        - **图片转视频**: 输入一张图片和音频，生成说话的视频
        - **视频转视频**: 输入视频和新音频，生成口型同步的新视频
        
        ### 显存管理
        - 模型加载后会占用显存
        - **5分钟不使用会自动释放显存**
        - 可手动点击"释放显存"按钮立即释放
        
        ### 模型大小说明
        - **原版模型**: 9.95GB，速度快，质量标准
        - **量化模型**: 19.5GB，质量更高，速度稍慢
        - **T5模型**: 6.73GB，辅助模型
        """)
    
    def update_model_dropdown(model_type):
        if model_type == "InfiniteTalk":
            choices = infinitetalk_choices
        else:
            choices = multitalk_choices
        return gr.Dropdown(choices=choices, value=None)
    
    def update_model_info(model_key):
        if model_key:
            info = MODELS[model_key]
            exists = check_model_exists(model_key)
            status_icon = "✅" if exists else "⏳"
            rec = "⭐ 推荐" if info["recommended"] else ""
            return f"{status_icon} {rec}\n\n类型: {info['type']}\n质量: {info['quality']}\n大小: {info['size']}\n\n说明: {info['description']}\n\n适用场景: {info['use_case']}\n\n路径: {info['path']}"
        return ""
    
    model_type.change(fn=update_model_dropdown, inputs=[model_type], outputs=[model_dropdown])
    model_dropdown.change(fn=update_model_info, inputs=[model_dropdown], outputs=[model_info])
    load_btn.click(fn=load_model, inputs=[model_dropdown], outputs=[status])
    refresh_btn.click(fn=get_model_status, inputs=[], outputs=[model_status])
    refresh_download_btn.click(fn=get_download_progress, inputs=[], outputs=[download_progress])
    unload_btn.click(fn=lambda: (unload_model(), "✅ 显存已释放")[1], inputs=[], outputs=[status])
    generate_btn.click(
        fn=generate_video,
        inputs=[mode, input_image, input_video, input_audio, input_text],
        outputs=[output_video, output_status]
    )

if __name__ == "__main__":
    # 启动时检查并下载缺失的模型
    check_and_download_models()
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
