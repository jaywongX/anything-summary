from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List, Optional
from app.core.tasks import process_and_summarize
from app.celery_app import celery_app
from app.config import settings
import aiofiles
import os
import uuid
import logging
from celery.result import AsyncResult

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/summary")
async def create_summary(
    files: List[UploadFile] = File(None),
    text: str = Form(None),
    url: str = Form(None)
):
    try:
        logger.info(f"Received request - files: {bool(files)}, text: {bool(text)}, url: {bool(url)}")
        task_id = str(uuid.uuid4())
        logger.info(f"Creating new task with ID: {task_id}")
        
        # 保存文件
        saved_files = []
        if files:
            for file in files:
                file_path = os.path.join(settings.UPLOAD_DIR, f"{task_id}_{file.filename}")
                async with aiofiles.open(file_path, 'wb') as f:
                    content = await file.read()
                    await f.write(content)
                saved_files.append(file_path)
                logger.info(f"Saved file: {file_path}")
        
        # 创建任务
        try:
            task = process_and_summarize.delay(
                task_id=task_id,
                file_paths=saved_files,
                text=text,
                url=url
            )
            logger.info(f"Created celery task with ID: {task_id}")
        except Exception as e:
            logger.error(f"Failed to create celery task: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to create task: {str(e)}"
            )
        
        return {
            "task_id": task_id,
            "status": "processing"
        }
    except Exception as e:
        logger.error(f"Error in create_summary: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/summary/{task_id}")
async def get_summary_status(task_id: str):
    """获取任务状态"""
    try:
        task_result = AsyncResult(task_id, app=celery_app)
        logger.debug(f"Task {task_id} state: {task_result.state}")
        
        # 尝试从 Redis 直接获取结果
        try:
            result = celery_app.backend.get_task_meta(task_id)
            logger.debug(f"Redis result for task {task_id}: {result}")
            
            if result and result.get('status') == 'SUCCESS':
                task_result = result.get('result', {})
                if isinstance(task_result, dict) and task_result.get('status') == 'success':
                    return {
                        "status": "success",
                        "result": {
                            "summary": task_result.get('summary', '')
                        }
                    }
        except Exception as e:
            logger.warning(f"Error getting result from Redis: {e}")
        
        # 检查任务状态
        if task_result.state == 'SUCCESS':
            result = task_result.get()
            if isinstance(result, dict) and result.get('status') == 'success':
                return {
                    "status": "success",
                    "result": {
                        "summary": result.get('summary', '')
                    }
                }
            else:
                return {
                    "status": "error",
                    "error": result.get('error', 'Unknown error')
                }
        elif task_result.state == 'FAILURE':
            error = str(task_result.result)
            logger.error(f"Task {task_id} failed: {error}")
            return {
                "status": "error",
                "error": error
            }
        elif task_result.state == 'PENDING':
            # 检查任务是否真的存在
            if not celery_app.backend.get_task_meta(task_id):
                return {
                    "status": "error",
                    "error": "Task not found"
                }
        
        return {"status": "processing"}
            
    except Exception as e:
        logger.error(f"Error checking task status: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }

@router.get("/celery/status")
async def get_celery_status():
    """检查 Celery 状态"""
    try:
        # 检查 Redis 连接
        redis_ok = celery_app.backend.client.ping()
        
        # 检查 Worker
        workers = celery_app.control.inspect().active()
        
        if not workers:
            return {
                "status": "error",
                "message": "No Celery workers are running"
            }
            
        return {
            "status": "ok",
            "redis_connected": redis_ok,
            "workers": list(workers.keys())
        }
    except Exception as e:
        logger.error(f"Error checking Celery status: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/health/redis")
async def check_redis_health():
    """检查 Redis 健康状态"""
    try:
        # 检查 Redis 连接
        redis_client = celery_app.backend.client
        redis_info = redis_client.info()
        
        return {
            "status": "ok",
            "redis_version": redis_info.get('redis_version'),
            "connected_clients": redis_info.get('connected_clients'),
            "used_memory_human": redis_info.get('used_memory_human'),
            "total_connections_received": redis_info.get('total_connections_received')
        }
    except Exception as e:
        logger.error(f"Redis health check failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "message": str(e)
        } 