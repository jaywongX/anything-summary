from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from app.core.tasks import process_and_summarize  # 只导入任务，不重新定义
from app.celery_app import celery_app  # 添加这行导入
from app.config import settings
import aiofiles
import os
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/summary")
async def create_summary(
    files: List[UploadFile] = File(default=[]),
    urls: str = Form(default=""),
    texts: str = Form(default="")
):
    try:
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
        
        # 启动异步任务
        task = process_and_summarize.apply_async(
            kwargs={
                "task_id": task_id,
                "file_paths": saved_files,
                "text": texts,
                "url": urls
            },
            task_id=task_id  # 确保使用相同的task_id
        )
        logger.info(f"Created celery task with ID: {task.id}")
        
        return {
            "task_id": task_id,
            "status": "processing",
            "success": True
        }
    except Exception as e:
        logger.error(f"Error creating summary task: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": str(e)
        }

@router.get("/summary/{task_id}")
async def get_summary_status(task_id: str):
    """获取任务状态"""
    try:
        task = celery_app.AsyncResult(task_id)
        status = task.status
        logger.info(f"Checking task {task_id} status: {status}")
        
        if status == 'SUCCESS':
            result = task.result
            logger.info(f"Task result: {result}")
            if isinstance(result, dict) and result.get("status") == "success":
                return {
                    "status": "completed",
                    "result": result
                }
            else:
                return {
                    "status": "error",
                    "error": result.get("error", "处理失败") if isinstance(result, dict) else str(result)
                }
        elif status == 'PENDING':
            return {"status": "processing"}
        elif status == 'FAILURE':
            return {
                "status": "error",
                "error": str(task.result)
            }
        else:
            return {"status": "processing"}
        
    except Exception as e:
        logger.error(f"Error checking task status: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        } 