## 🆕 v1.1.0 新特性 (2025-12-05)

### GPU 智能管理 ⭐
- ✅ **懒加载机制** - 按需加载，启动时不占用显存
- ✅ **即用即卸** - 任务完成立即释放显存（<1GB）
- ✅ **快速恢复** - CPU缓存快速恢复到GPU（2-5秒）
- ✅ **自动超时** - 空闲60秒自动卸载到CPU
- ✅ **多GPU支持** - 自动选择显存占用最少的GPU

### 三模式访问 🚀
1. **UI 界面** - Gradio Web 界面（http://0.0.0.0:7860）
2. **REST API** - HTTP 接口 + Swagger 文档（/docs）
3. **MCP 服务器** - 程序化访问接口

### 新增文件
- `gpu_manager.py` - GPU 资源智能管理器
- `api_server.py` - REST API 服务
- `mcp_server.py` - MCP 服务器
- `start.sh` - 一键启动脚本（自动选择GPU）
- `GPU_MANAGEMENT.md` - GPU 管理文档
- `MCP_GUIDE.md` - MCP 使用指南
- `test_api.sh` - API 测试脚本

### 快速启动

```bash
# 自动选择最空闲的 GPU 并启动
./start.sh

# 访问服务
# UI:  http://0.0.0.0:7860
# API: http://0.0.0.0:7860/docs
```

### GPU 管理 API

```bash
# 查看 GPU 状态
curl http://localhost:7860/gpu/status

# 手动卸载显存
curl -X POST http://localhost:7860/gpu/offload

# 完全释放
curl -X POST http://localhost:7860/gpu/release
```

详见：[GPU_MANAGEMENT.md](GPU_MANAGEMENT.md) | [MCP_GUIDE.md](MCP_GUIDE.md)
