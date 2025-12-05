# MCP (Model Context Protocol) 使用指南

## 📋 概述

MCP 服务器提供程序化访问 InfiniteTalk 的接口，适合集成到其他应用或自动化工作流中。

## 🚀 快速开始

### 1. 启动 MCP 服务器

```bash
# 方式一：直接运行
python3 mcp_server.py

# 方式二：通过 Docker
docker exec infinitetalk python3 mcp_server.py
```

### 2. 配置 MCP 客户端

在你的 MCP 客户端配置文件中添加：

```json
{
  "mcpServers": {
    "infinitetalk": {
      "command": "python3",
      "args": ["/path/to/mcp_server.py"],
      "env": {
        "GPU_IDLE_TIMEOUT": "600"
      }
    }
  }
}
```

## 🛠️ 可用工具

### 1. process_image_to_video

图片转视频生成

**参数：**
- `image_path` (string, required): 输入图片路径
- `audio_path` (string, required): 输入音频路径
- `text_prompt` (string, optional): 文本提示
- `model_type` (string, optional): 模型类型，默认 "single_original"

**返回：**
```json
{
  "status": "success",
  "output_path": "/path/to/output.mp4",
  "model_used": "single_original",
  "message": "视频生成完成"
}
```

**示例：**
```python
result = await mcp_client.call_tool(
    "process_image_to_video",
    {
        "image_path": "/path/to/image.jpg",
        "audio_path": "/path/to/audio.wav",
        "text_prompt": "A person talking",
        "model_type": "single_original"
    }
)
```

### 2. process_video_to_video

视频转视频（口型同步）

**参数：**
- `video_path` (string, required): 输入视频路径
- `audio_path` (string, required): 输入音频路径
- `text_prompt` (string, optional): 文本提示
- `model_type` (string, optional): 模型类型，默认 "multi_original"

**返回：**
```json
{
  "status": "success",
  "output_path": "/path/to/output.mp4",
  "model_used": "multi_original",
  "message": "视频同步完成"
}
```

### 3. get_gpu_status

获取 GPU 状态信息

**参数：** 无

**返回：**
```json
{
  "model_location": "GPU",
  "idle_time": 30,
  "idle_timeout": 60,
  "gpu_available": true,
  "gpu_memory_allocated_gb": 8.5,
  "gpu_memory_reserved_gb": 9.0,
  "gpu_name": "NVIDIA GeForce RTX 4090"
}
```

### 4. offload_gpu

手动卸载 GPU 显存

**参数：** 无

**返回：**
```json
{
  "status": "offloaded",
  "message": "模型已卸载到 CPU，显存已释放"
}
```

### 5. release_gpu

完全释放 GPU 和 CPU 缓存

**参数：** 无

**返回：**
```json
{
  "status": "released",
  "message": "模型已完全释放"
}
```

### 6. update_gpu_timeout

更新 GPU 空闲超时时间

**参数：**
- `timeout_seconds` (integer, required): 超时时间（秒）

**返回：**
```json
{
  "status": "updated",
  "timeout": 300,
  "message": "空闲超时已更新为 300秒"
}
```

### 7. list_available_models

列出所有可用的模型

**参数：** 无

**返回：**
```json
{
  "status": "success",
  "models": {
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
  },
  "total_count": 9
}
```

## 📝 使用示例

### Python 客户端

```python
from mcp import ClientSession
import asyncio

async def main():
    async with ClientSession() as session:
        # 1. 检查 GPU 状态
        status = await session.call_tool("get_gpu_status", {})
        print(f"GPU 状态: {status}")
        
        # 2. 生成视频
        result = await session.call_tool(
            "process_image_to_video",
            {
                "image_path": "/path/to/image.jpg",
                "audio_path": "/path/to/audio.wav",
                "model_type": "single_original"
            }
        )
        print(f"生成结果: {result}")
        
        # 3. 手动卸载 GPU
        await session.call_tool("offload_gpu", {})

asyncio.run(main())
```

### CLI 调用

```bash
# 使用 mcp CLI
mcp call process_image_to_video '{
  "image_path": "/path/to/image.jpg",
  "audio_path": "/path/to/audio.wav"
}'

# 查看 GPU 状态
mcp call get_gpu_status '{}'

# 手动卸载
mcp call offload_gpu '{}'
```

## 🔄 MCP vs API 对比

| 特性 | MCP | REST API |
|------|-----|----------|
| 访问方式 | 程序化调用 | HTTP 请求 |
| 适用场景 | 自动化、集成 | Web 应用、测试 |
| 类型安全 | ✅ 强类型 | ⚠️ 需验证 |
| 文档 | 自动生成 | Swagger |
| 性能 | 🚀 更快 | 标准 |

## 💡 最佳实践

1. **GPU 管理**
   - 处理完成后立即调用 `offload_gpu`
   - 长时间不用时调用 `release_gpu`
   - 定期检查 `get_gpu_status`

2. **错误处理**
   - 始终检查返回的 `status` 字段
   - 捕获异常并记录日志
   - 失败时确保调用 `offload_gpu`

3. **性能优化**
   - 批量处理时复用模型
   - 合理设置 `GPU_IDLE_TIMEOUT`
   - 监控显存使用情况

## 🐛 故障排查

### 问题：MCP 服务器无法启动

**解决方案：**
```bash
# 检查依赖
pip3 install fastmcp

# 查看日志
python3 mcp_server.py 2>&1 | tee mcp.log
```

### 问题：GPU 显存不足

**解决方案：**
```python
# 立即释放显存
await session.call_tool("release_gpu", {})

# 使用更小的模型
result = await session.call_tool(
    "process_image_to_video",
    {"model_type": "single_original"}  # 使用原版模型
)
```

## 📚 相关文档

- [GPU 管理文档](GPU_MANAGEMENT.md)
- [API 文档](http://localhost:7860/docs)
- [项目 README](README.md)
