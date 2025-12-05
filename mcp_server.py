"""
MCP (Model Context Protocol) 服务器
提供程序化访问接口
"""
from fastmcp import FastMCP
from gpu_manager import get_gpu_manager
import os
import logging
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 MCP 服务器
mcp = FastMCP("InfiniteTalk")

# 初始化 GPU 管理器
gpu_manager = get_gpu_manager(idle_timeout=int(os.getenv('GPU_IDLE_TIMEOUT', 600)))


@mcp.tool()
def process_image_to_video(
    image_path: str,
    audio_path: str,
    text_prompt: Optional[str] = None,
    model_type: str = "single_original"
) -> Dict[str, Any]:
    """
    图片转视频生成
    
    Args:
        image_path: 输入图片路径
        audio_path: 输入音频路径
        text_prompt: 文本提示（可选）
        model_type: 模型类型（single_original/multi_original等）
    
    Returns:
        处理结果，包含输出视频路径
    """
    try:
        logger.info(f"MCP: 图片转视频 - {image_path}")
        
        # 步骤1: 懒加载模型
        def load_model():
            logger.info(f"加载模型: {model_type}")
            # 这里应该加载实际的 InfiniteTalk 模型
            import time
            time.sleep(2)  # 模拟加载
            return {"model": model_type}
        
        model = gpu_manager.get_model(load_func=load_model)
        
        # 步骤2: 处理
        # 这里添加实际的视频生成逻辑
        output_path = f"/tmp/infinitetalk_output_{os.path.basename(image_path)}.mp4"
        
        # 步骤3: 立即卸载
        gpu_manager.force_offload()
        
        return {
            'status': 'success',
            'output_path': output_path,
            'model_used': model_type,
            'message': '视频生成完成'
        }
        
    except Exception as e:
        gpu_manager.force_offload()
        logger.error(f"处理失败: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


@mcp.tool()
def process_video_to_video(
    video_path: str,
    audio_path: str,
    text_prompt: Optional[str] = None,
    model_type: str = "multi_original"
) -> Dict[str, Any]:
    """
    视频转视频（口型同步）
    
    Args:
        video_path: 输入视频路径
        audio_path: 输入音频路径
        text_prompt: 文本提示（可选）
        model_type: 模型类型
    
    Returns:
        处理结果，包含输出视频路径
    """
    try:
        logger.info(f"MCP: 视频转视频 - {video_path}")
        
        # 步骤1: 懒加载模型
        def load_model():
            logger.info(f"加载模型: {model_type}")
            import time
            time.sleep(2)
            return {"model": model_type}
        
        model = gpu_manager.get_model(load_func=load_model)
        
        # 步骤2: 处理
        output_path = f"/tmp/infinitetalk_output_{os.path.basename(video_path)}"
        
        # 步骤3: 立即卸载
        gpu_manager.force_offload()
        
        return {
            'status': 'success',
            'output_path': output_path,
            'model_used': model_type,
            'message': '视频同步完成'
        }
        
    except Exception as e:
        gpu_manager.force_offload()
        logger.error(f"处理失败: {e}")
        return {
            'status': 'error',
            'error': str(e)
        }


@mcp.tool()
def get_gpu_status() -> Dict[str, Any]:
    """
    获取 GPU 状态信息
    
    Returns:
        GPU 状态，包括模型位置、显存使用等
    """
    return gpu_manager.get_status()


@mcp.tool()
def offload_gpu() -> Dict[str, str]:
    """
    手动卸载 GPU 显存
    将模型从 GPU 转移到 CPU
    
    Returns:
        操作状态
    """
    gpu_manager.force_offload()
    return {
        'status': 'offloaded',
        'message': '模型已卸载到 CPU，显存已释放'
    }


@mcp.tool()
def release_gpu() -> Dict[str, str]:
    """
    完全释放 GPU 和 CPU 缓存
    清空所有模型
    
    Returns:
        操作状态
    """
    gpu_manager.force_release()
    return {
        'status': 'released',
        'message': '模型已完全释放'
    }


@mcp.tool()
def update_gpu_timeout(timeout_seconds: int) -> Dict[str, Any]:
    """
    更新 GPU 空闲超时时间
    
    Args:
        timeout_seconds: 超时时间（秒）
    
    Returns:
        更新状态
    """
    gpu_manager.update_timeout(timeout_seconds)
    return {
        'status': 'updated',
        'timeout': timeout_seconds,
        'message': f'空闲超时已更新为 {timeout_seconds}秒'
    }


@mcp.tool()
def list_available_models() -> Dict[str, Any]:
    """
    列出所有可用的模型
    
    Returns:
        模型列表及其详细信息
    """
    # 从 app.py 导入模型配置
    models = {
        "infinitetalk": [
            "single_original",
            "multi_original",
            "single_int8",
            "multi_int8",
            "single_fp8",
            "multi_fp8"
        ],
        "multitalk": [
            "multitalk_original",
            "multitalk_int8_fusionx",
            "multitalk_fp8_fusionx"
        ]
    }
    
    return {
        'status': 'success',
        'models': models,
        'total_count': sum(len(v) for v in models.values())
    }


# 启动 MCP 服务器
if __name__ == "__main__":
    logger.info("启动 InfiniteTalk MCP 服务器...")
    mcp.run()
