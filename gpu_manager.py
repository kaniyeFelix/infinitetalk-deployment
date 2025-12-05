"""
GPU 资源智能管理器
实现懒加载 + 即用即卸逻辑
"""
import torch
import gc
import time
import threading
import logging
from typing import Callable, Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GPUResourceManager:
    """GPU 资源管理器 - 懒加载 + 即用即卸"""
    
    def __init__(self, idle_timeout: int = 60):
        """
        Args:
            idle_timeout: 空闲超时时间（秒），超时后自动转移到 CPU
        """
        self.model = None  # GPU 上的模型
        self.model_on_cpu = None  # CPU 缓存
        self.lock = threading.Lock()
        self.idle_timeout = idle_timeout
        self.last_use_time = time.time()
        self.running = False
        self.monitor_thread = None
        self.model_location = "未加载"  # 未加载/GPU/CPU
        self.load_func = None
        
    def start_monitor(self):
        """启动监控线程"""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info(f"GPU 监控已启动，空闲超时: {self.idle_timeout}秒")
    
    def stop_monitor(self):
        """停止监控线程"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
    
    def _monitor_loop(self):
        """监控循环 - 自动卸载空闲模型"""
        while self.running:
            time.sleep(30)  # 每30秒检查一次
            
            with self.lock:
                if self.model is not None:
                    idle_time = time.time() - self.last_use_time
                    
                    if idle_time > self.idle_timeout:
                        logger.info(f"模型空闲 {idle_time:.0f}秒，自动卸载到 CPU")
                        self._move_to_cpu()
    
    def get_model(self, load_func: Callable):
        """
        懒加载获取模型
        
        状态转换：
        1. 未加载 → GPU (首次，20-30秒)
        2. CPU → GPU (快速恢复，2-5秒)
        3. GPU → 直接返回 (0秒)
        
        Args:
            load_func: 模型加载函数
            
        Returns:
            模型实例（在 GPU 上）
        """
        with self.lock:
            self.last_use_time = time.time()
            self.load_func = load_func
            
            # 情况1: 已在 GPU 上
            if self.model is not None:
                logger.info("模型已在 GPU 上，直接使用")
                return self.model
            
            # 情况2: 在 CPU 上，快速转移
            if self.model_on_cpu is not None:
                logger.info("从 CPU 恢复模型到 GPU (2-5秒)")
                start = time.time()
                self.model = self.model_on_cpu.to('cuda')
                self.model_on_cpu = None
                self.model_location = "GPU"
                logger.info(f"恢复完成，耗时 {time.time()-start:.1f}秒")
                return self.model
            
            # 情况3: 未加载，从磁盘加载
            logger.info("首次加载模型到 GPU (20-30秒)")
            start = time.time()
            self.model = load_func()
            self.model_location = "GPU"
            logger.info(f"加载完成，耗时 {time.time()-start:.1f}秒")
            return self.model
    
    def force_offload(self):
        """
        即用即卸：任务完成后立即调用
        将模型从 GPU 转移到 CPU，释放显存
        """
        with self.lock:
            if self.model is not None:
                logger.info("任务完成，卸载模型到 CPU (2秒)")
                start = time.time()
                self.model_on_cpu = self.model.to('cpu')
                self.model = None
                self.model_location = "CPU"
                
                # 清理 GPU 缓存
                torch.cuda.empty_cache()
                gc.collect()
                
                logger.info(f"卸载完成，耗时 {time.time()-start:.1f}秒")
                self._log_gpu_memory()
    
    def force_release(self):
        """
        完全释放：清空 GPU 和 CPU 缓存
        """
        with self.lock:
            logger.info("完全释放模型")
            self.model = None
            self.model_on_cpu = None
            self.model_location = "未加载"
            
            torch.cuda.empty_cache()
            gc.collect()
            
            logger.info("释放完成")
            self._log_gpu_memory()
    
    def _move_to_cpu(self):
        """内部方法：将模型从 GPU 移到 CPU"""
        if self.model is not None:
            self.model_on_cpu = self.model.to('cpu')
            self.model = None
            self.model_location = "CPU"
            
            torch.cuda.empty_cache()
            gc.collect()
            
            self._log_gpu_memory()
    
    def _log_gpu_memory(self):
        """记录 GPU 显存使用"""
        if torch.cuda.is_available():
            allocated = torch.cuda.memory_allocated() / 1024**3
            reserved = torch.cuda.memory_reserved() / 1024**3
            logger.info(f"GPU 显存: 已分配 {allocated:.2f}GB, 已保留 {reserved:.2f}GB")
    
    def get_status(self) -> Dict[str, Any]:
        """获取当前状态"""
        with self.lock:
            idle_time = time.time() - self.last_use_time
            
            status = {
                "model_location": self.model_location,
                "idle_time": int(idle_time),
                "idle_timeout": self.idle_timeout,
                "gpu_available": torch.cuda.is_available()
            }
            
            if torch.cuda.is_available():
                status["gpu_memory_allocated_gb"] = torch.cuda.memory_allocated() / 1024**3
                status["gpu_memory_reserved_gb"] = torch.cuda.memory_reserved() / 1024**3
                status["gpu_name"] = torch.cuda.get_device_name(0)
            
            return status
    
    def update_timeout(self, new_timeout: int):
        """更新空闲超时时间"""
        with self.lock:
            self.idle_timeout = new_timeout
            logger.info(f"空闲超时已更新为 {new_timeout}秒")


# 全局单例
_gpu_manager = None

def get_gpu_manager(idle_timeout: int = 60) -> GPUResourceManager:
    """获取全局 GPU 管理器单例"""
    global _gpu_manager
    if _gpu_manager is None:
        _gpu_manager = GPUResourceManager(idle_timeout=idle_timeout)
        _gpu_manager.start_monitor()
    return _gpu_manager
