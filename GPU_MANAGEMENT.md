# GPU 显存智能管理文档

## 🎯 设计目标

实现 **懒加载 + 即用即卸** 的 GPU 显存管理策略，在多 GPU 环境下高效利用资源。

## 📊 状态转换图

```
未加载 ──首次请求(20-30s)──→ GPU ──任务完成(2s)──→ CPU ──新请求(2-5s)──→ GPU
  ↑                                                      ↓
  └────────────────────超时/手动释放(1s)─────────────────┘
```

## 🔄 工作流程

### 1. 懒加载（Lazy Loading）

模型按需加载，避免启动时占用显存：

```python
# 首次请求
model = gpu_manager.get_model(load_func=load_infinitetalk_model)
# → 从磁盘加载到 GPU (20-30秒)

# 第二次请求（模型在 CPU）
model = gpu_manager.get_model(load_func=load_infinitetalk_model)
# → 从 CPU 转移到 GPU (2-5秒)

# 第三次请求（模型在 GPU）
model = gpu_manager.get_model(load_func=load_infinitetalk_model)
# → 直接返回 (0秒)
```

### 2. 即用即卸（Immediate Offload）

任务完成后立即释放显存：

```python
def process_video(input_data):
    try:
        # 步骤1: 获取模型
        model = gpu_manager.get_model(load_func=load_model)
        
        # 步骤2: 处理
        result = model.process(input_data)
        
        # 步骤3: 立即卸载（关键！）
        gpu_manager.force_offload()
        
        return result
    except Exception as e:
        # 异常时也要卸载
        gpu_manager.force_offload()
        raise e
```

### 3. 自动超时

空闲超过设定时间后自动转移到 CPU：

```python
# 默认 60 秒超时
gpu_manager = GPUResourceManager(idle_timeout=60)

# 监控线程每 30 秒检查一次
# 如果空闲时间 > idle_timeout，自动执行 _move_to_cpu()
```

## 🛠️ API 接口

### Python API

```python
from gpu_manager import get_gpu_manager

# 获取全局管理器
gpu_manager = get_gpu_manager(idle_timeout=60)

# 启动监控
gpu_manager.start_monitor()

# 获取模型（懒加载）
model = gpu_manager.get_model(load_func=your_load_function)

# 手动卸载
gpu_manager.force_offload()

# 完全释放
gpu_manager.force_release()

# 获取状态
status = gpu_manager.get_status()

# 更新超时
gpu_manager.update_timeout(300)
```

### REST API

```bash
# 查看 GPU 状态
curl http://localhost:7860/gpu/status

# 手动卸载
curl -X POST http://localhost:7860/gpu/offload

# 完全释放
curl -X POST http://localhost:7860/gpu/release

# 更新超时
curl -X POST http://localhost:7860/gpu/timeout -F "timeout=300"
```

### MCP 工具

```python
# 查看状态
await mcp_client.call_tool("get_gpu_status", {})

# 手动卸载
await mcp_client.call_tool("offload_gpu", {})

# 完全释放
await mcp_client.call_tool("release_gpu", {})

# 更新超时
await mcp_client.call_tool("update_gpu_timeout", {"timeout_seconds": 300})
```

## 📈 性能指标

### 时间开销

| 操作 | 时间 | 说明 |
|------|------|------|
| 首次加载 | 20-30秒 | 从磁盘加载模型到 GPU |
| CPU→GPU | 2-5秒 | 从 CPU 缓存恢复到 GPU |
| GPU→CPU | 2秒 | 卸载到 CPU，释放显存 |
| 完全释放 | 1秒 | 清空所有缓存 |

### 显存占用

| 状态 | 显存占用 | 说明 |
|------|----------|------|
| 未加载 | 0 GB | 无模型 |
| CPU 缓存 | < 0.5 GB | 仅保留少量 GPU 缓存 |
| GPU 运行 | 8-20 GB | 根据模型大小 |

## 🎛️ 配置参数

### 环境变量

```bash
# GPU 空闲超时（秒）
GPU_IDLE_TIMEOUT=60

# GPU 设备 ID
NVIDIA_VISIBLE_DEVICES=0
```

### 代码配置

```python
# 初始化时设置
gpu_manager = GPUResourceManager(
    idle_timeout=60  # 60秒空闲后自动卸载
)

# 运行时更新
gpu_manager.update_timeout(300)  # 改为 5 分钟
```

## 💡 最佳实践

### 1. 单任务处理

```python
def process_single_task(input_data):
    """标准的单任务处理流程"""
    try:
        model = gpu_manager.get_model(load_func=load_model)
        result = model.process(input_data)
        gpu_manager.force_offload()  # 立即卸载
        return result
    except Exception as e:
        gpu_manager.force_offload()  # 异常也要卸载
        raise e
```

### 2. 批量处理

```python
def process_batch(input_list):
    """批量处理时复用模型"""
    try:
        model = gpu_manager.get_model(load_func=load_model)
        
        results = []
        for input_data in input_list:
            result = model.process(input_data)
            results.append(result)
        
        # 批量完成后再卸载
        gpu_manager.force_offload()
        return results
    except Exception as e:
        gpu_manager.force_offload()
        raise e
```

### 3. 长时间运行

```python
def long_running_service():
    """长时间运行的服务"""
    # 设置较长的超时时间
    gpu_manager.update_timeout(600)  # 10 分钟
    
    while True:
        task = get_next_task()
        if task:
            process_single_task(task)
        else:
            time.sleep(1)
```

## 🔍 监控和调试

### 查看实时状态

```python
status = gpu_manager.get_status()
print(f"模型位置: {status['model_location']}")
print(f"空闲时间: {status['idle_time']}秒")
print(f"显存占用: {status['gpu_memory_allocated_gb']:.2f}GB")
```

### 日志输出

```
INFO:gpu_manager:GPU 监控已启动，空闲超时: 60秒
INFO:gpu_manager:首次加载模型到 GPU (20-30秒)
INFO:gpu_manager:加载完成，耗时 23.5秒
INFO:gpu_manager:任务完成，卸载模型到 CPU (2秒)
INFO:gpu_manager:卸载完成，耗时 1.8秒
INFO:gpu_manager:GPU 显存: 已分配 0.45GB, 已保留 0.50GB
INFO:gpu_manager:从 CPU 恢复模型到 GPU (2-5秒)
INFO:gpu_manager:恢复完成，耗时 3.2秒
INFO:gpu_manager:模型空闲 65秒，自动卸载到 CPU
```

## 🐛 故障排查

### 问题1: 显存未释放

**症状：** 调用 `force_offload()` 后显存仍然很高

**原因：** 可能有其他引用未释放

**解决：**
```python
# 确保没有其他变量引用模型
model = None
gpu_manager.force_release()  # 使用完全释放

# 手动触发垃圾回收
import gc
gc.collect()
torch.cuda.empty_cache()
```

### 问题2: 恢复速度慢

**症状：** CPU→GPU 恢复超过 10 秒

**原因：** CPU 内存不足或模型太大

**解决：**
```python
# 方案1: 增加系统内存
# 方案2: 使用更小的模型
# 方案3: 完全释放后重新加载
gpu_manager.force_release()
```

### 问题3: 自动卸载不工作

**症状：** 超时后模型仍在 GPU 上

**原因：** 监控线程未启动

**解决：**
```python
# 确保启动监控
gpu_manager.start_monitor()

# 检查监控状态
print(f"监控运行中: {gpu_manager.running}")
```

## 📊 性能对比

### 传统方式 vs 智能管理

| 指标 | 传统方式 | 智能管理 | 提升 |
|------|----------|----------|------|
| 启动时间 | 30秒 | 0秒 | ✅ 即时启动 |
| 空闲显存 | 20GB | <1GB | ✅ 节省 95% |
| 第二次请求 | 0秒 | 3秒 | ⚠️ 略慢 |
| GPU 利用率 | 低 | 高 | ✅ 多容器共享 |

## 🎓 进阶技巧

### 1. 多模型管理

```python
# 为不同模型创建不同的管理器
infinitetalk_manager = GPUResourceManager(idle_timeout=60)
multitalk_manager = GPUResourceManager(idle_timeout=120)

# 分别管理
model1 = infinitetalk_manager.get_model(load_infinitetalk)
model2 = multitalk_manager.get_model(load_multitalk)
```

### 2. 优先级队列

```python
# 高优先级任务立即加载
if task.priority == "high":
    gpu_manager.force_offload()  # 先卸载其他模型
    model = gpu_manager.get_model(load_func)
```

### 3. 预热策略

```python
# 预测即将使用，提前加载到 GPU
def preheat():
    model = gpu_manager.get_model(load_func)
    # 不立即卸载，等待实际请求
```

## 📚 相关文档

- [MCP 使用指南](MCP_GUIDE.md)
- [API 文档](http://localhost:7860/docs)
- [项目 README](README.md)
