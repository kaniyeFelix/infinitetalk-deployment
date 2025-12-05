#!/bin/bash
# InfiniteTalk 一键启动脚本
# 自动选择显存占用最少的 GPU

set -e

echo "========================================="
echo "  InfiniteTalk Docker 启动脚本"
echo "========================================="

# 检查 nvidia-docker
if ! command -v nvidia-smi &> /dev/null; then
    echo "❌ 错误: 未检测到 nvidia-smi"
    echo "请确保已安装 NVIDIA 驱动"
    exit 1
fi

if ! docker info | grep -q "Runtimes.*nvidia"; then
    echo "⚠️  警告: nvidia-docker 可能未正确配置"
    echo "尝试继续..."
fi

# 自动选择显存占用最少的 GPU
echo ""
echo "🔍 检测可用 GPU..."
nvidia-smi --query-gpu=index,name,memory.used,memory.total --format=csv,noheader

GPU_ID=$(nvidia-smi --query-gpu=index,memory.used --format=csv,noheader,nounits | \
         sort -t',' -k2 -n | head -1 | cut -d',' -f1)

GPU_NAME=$(nvidia-smi --query-gpu=name --format=csv,noheader -i $GPU_ID)
GPU_MEM_USED=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits -i $GPU_ID)
GPU_MEM_TOTAL=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits -i $GPU_ID)

echo ""
echo "✅ 已选择 GPU $GPU_ID: $GPU_NAME"
echo "   显存使用: ${GPU_MEM_USED}MB / ${GPU_MEM_TOTAL}MB"

# 设置环境变量
export NVIDIA_VISIBLE_DEVICES=$GPU_ID

# 加载 .env 文件（如果存在）
if [ -f .env ]; then
    echo ""
    echo "📝 加载环境变量..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo ""
    echo "⚠️  未找到 .env 文件，使用默认配置"
    echo "   提示: 复制 .env.example 为 .env 并修改配置"
fi

# 设置默认值
PORT=${PORT:-7860}
GPU_IDLE_TIMEOUT=${GPU_IDLE_TIMEOUT:-60}

echo ""
echo "📋 配置信息:"
echo "   GPU ID: $GPU_ID"
echo "   服务端口: $PORT"
echo "   GPU 空闲超时: ${GPU_IDLE_TIMEOUT}秒"

# 停止旧容器（如果存在）
if docker ps -a | grep -q infinitetalk; then
    echo ""
    echo "🛑 停止旧容器..."
    docker stop infinitetalk 2>/dev/null || true
    docker rm infinitetalk 2>/dev/null || true
fi

# 启动容器
echo ""
echo "🚀 启动 InfiniteTalk 容器..."

docker run -d \
  --name infinitetalk \
  --gpus "device=$GPU_ID" \
  --restart unless-stopped \
  -p 0.0.0.0:${PORT}:7860 \
  -v $(pwd)/models:/app/models \
  -e GPU_IDLE_TIMEOUT=${GPU_IDLE_TIMEOUT} \
  -e NVIDIA_VISIBLE_DEVICES=${GPU_ID} \
  infinitetalk:latest

# 等待容器启动
echo ""
echo "⏳ 等待服务启动..."
sleep 5

# 检查容器状态
if docker ps | grep -q infinitetalk; then
    echo ""
    echo "========================================="
    echo "  ✅ InfiniteTalk 启动成功！"
    echo "========================================="
    echo ""
    echo "📍 访问地址:"
    echo "   UI 界面:  http://0.0.0.0:${PORT}"
    echo "   API 文档: http://0.0.0.0:${PORT}/docs"
    echo ""
    echo "🔧 管理命令:"
    echo "   查看日志: docker logs -f infinitetalk"
    echo "   停止服务: docker stop infinitetalk"
    echo "   重启服务: docker restart infinitetalk"
    echo ""
    echo "💡 GPU 管理:"
    echo "   查看状态: curl http://localhost:${PORT}/gpu/status"
    echo "   手动卸载: curl -X POST http://localhost:${PORT}/gpu/offload"
    echo "   完全释放: curl -X POST http://localhost:${PORT}/gpu/release"
    echo ""
else
    echo ""
    echo "❌ 容器启动失败"
    echo "查看日志: docker logs infinitetalk"
    exit 1
fi
