"""
RESTful API 服务
提供 HTTP 接口访问
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from flasgger import Swagger
import os
import uuid
from gpu_manager import get_gpu_manager
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Swagger 配置
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs"
}
swagger = Swagger(app, config=swagger_config)

# 初始化 GPU 管理器
gpu_manager = get_gpu_manager(idle_timeout=int(os.getenv('GPU_IDLE_TIMEOUT', 60)))

# 任务存储
tasks = {}


@app.route('/health', methods=['GET'])
def health():
    """
    健康检查
    ---
    tags:
      - System
    responses:
      200:
        description: 服务正常
    """
    return jsonify({"status": "healthy", "service": "InfiniteTalk API"})


@app.route('/gpu/status', methods=['GET'])
def gpu_status():
    """
    获取 GPU 状态
    ---
    tags:
      - GPU Management
    responses:
      200:
        description: GPU 状态信息
        schema:
          properties:
            model_location:
              type: string
            idle_time:
              type: integer
            gpu_memory_allocated_gb:
              type: number
    """
    status = gpu_manager.get_status()
    return jsonify(status)


@app.route('/gpu/offload', methods=['POST'])
def gpu_offload():
    """
    手动卸载 GPU 显存
    ---
    tags:
      - GPU Management
    responses:
      200:
        description: 卸载成功
    """
    gpu_manager.force_offload()
    return jsonify({"status": "offloaded", "message": "模型已卸载到 CPU"})


@app.route('/gpu/release', methods=['POST'])
def gpu_release():
    """
    完全释放 GPU 和 CPU 缓存
    ---
    tags:
      - GPU Management
    responses:
      200:
        description: 释放成功
    """
    gpu_manager.force_release()
    return jsonify({"status": "released", "message": "模型已完全释放"})


@app.route('/gpu/timeout', methods=['POST'])
def update_timeout():
    """
    更新 GPU 空闲超时时间
    ---
    tags:
      - GPU Management
    parameters:
      - name: timeout
        in: formData
        type: integer
        required: true
        description: 超时时间（秒）
    responses:
      200:
        description: 更新成功
    """
    timeout = int(request.form.get('timeout', 60))
    gpu_manager.update_timeout(timeout)
    return jsonify({"status": "updated", "timeout": timeout})


@app.route('/api/process', methods=['POST'])
def process_video():
    """
    处理视频生成请求
    ---
    tags:
      - Video Generation
    parameters:
      - name: mode
        in: formData
        type: string
        required: true
        enum: ['image_to_video', 'video_to_video']
        description: 生成模式
      - name: image
        in: formData
        type: file
        description: 输入图片（图片转视频模式）
      - name: video
        in: formData
        type: file
        description: 输入视频（视频转视频模式）
      - name: audio
        in: formData
        type: file
        required: true
        description: 输入音频
      - name: text
        in: formData
        type: string
        description: 文本提示（可选）
    responses:
      200:
        description: 任务已创建
        schema:
          properties:
            task_id:
              type: string
            status:
              type: string
    """
    try:
        task_id = str(uuid.uuid4())
        mode = request.form.get('mode', 'image_to_video')
        
        # 保存上传的文件
        upload_dir = '/tmp/infinitetalk_uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        files = {}
        if 'image' in request.files:
            image_file = request.files['image']
            image_path = os.path.join(upload_dir, f"{task_id}_image.png")
            image_file.save(image_path)
            files['image'] = image_path
        
        if 'video' in request.files:
            video_file = request.files['video']
            video_path = os.path.join(upload_dir, f"{task_id}_video.mp4")
            video_file.save(video_path)
            files['video'] = video_path
        
        if 'audio' in request.files:
            audio_file = request.files['audio']
            audio_path = os.path.join(upload_dir, f"{task_id}_audio.wav")
            audio_file.save(audio_path)
            files['audio'] = audio_path
        
        text = request.form.get('text', '')
        
        # 创建任务
        tasks[task_id] = {
            'status': 'processing',
            'mode': mode,
            'files': files,
            'text': text,
            'result': None
        }
        
        # 异步处理（这里简化为同步）
        # 实际应该使用 Celery 或 threading
        result = _process_task(task_id, mode, files, text)
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['result'] = result
        
        return jsonify({
            'task_id': task_id,
            'status': 'completed',
            'result': result
        })
        
    except Exception as e:
        logger.error(f"处理失败: {e}")
        return jsonify({'error': str(e)}), 500


def _process_task(task_id, mode, files, text):
    """处理任务的核心逻辑"""
    try:
        # 步骤1: 懒加载模型
        def load_model():
            # 这里应该加载实际的 InfiniteTalk 模型
            # 示例代码
            logger.info("加载 InfiniteTalk 模型...")
            import time
            time.sleep(2)  # 模拟加载
            return {"model": "infinitetalk"}  # 占位符
        
        model = gpu_manager.get_model(load_func=load_model)
        
        # 步骤2: 处理
        logger.info(f"处理任务 {task_id}")
        # 这里添加实际的视频生成逻辑
        result_path = f"/tmp/infinitetalk_results/{task_id}_output.mp4"
        
        # 步骤3: 立即卸载（关键！）
        gpu_manager.force_offload()
        
        return {
            'output_path': result_path,
            'message': '处理完成'
        }
        
    except Exception as e:
        # 异常时也要卸载
        gpu_manager.force_offload()
        raise e


@app.route('/api/status/<task_id>', methods=['GET'])
def task_status(task_id):
    """
    查询任务状态
    ---
    tags:
      - Video Generation
    parameters:
      - name: task_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: 任务状态
      404:
        description: 任务不存在
    """
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(tasks[task_id])


if __name__ == '__main__':
    port = int(os.getenv('PORT', 7860))
    app.run(host='0.0.0.0', port=port, debug=False)
