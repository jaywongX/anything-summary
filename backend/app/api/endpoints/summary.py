from fastapi import APIRouter, UploadFile, File, Form
from typing import List, Optional
from app.core.file_processor import FileProcessor
from app.core.summarizer import Summarizer
from app.celery_app import celery_app
from app.config import settings
import aiofiles
import os

router = APIRouter()
file_processor = FileProcessor(settings.UPLOAD_DIR)
summarizer = Summarizer()

@router.post("/summary")
async def create_summary(
    files: Optional[List[UploadFile]] = File(None),
    text: Optional[str] = Form(None),
    url: Optional[str] = Form(None)
):
    try:
        # 创建任务ID
        task_id = celery_app.new_task_id()
        
        # 保存文件
        saved_files = []
        if files:
            for file in files:
                file_path = os.path.join(settings.UPLOAD_DIR, f"{task_id}_{file.filename}")
                async with aiofiles.open(file_path, 'wb') as f:
                    content = await file.read()
                    await f.write(content)
                saved_files.append(file_path)
        
        # 启动异步任务
        task = process_and_summarize.delay(
            task_id=task_id,
            file_paths=saved_files,
            text=text,
            url=url
        )
        
        return {"task_id": task_id}
        
    except Exception as e:
        return {"error": str(e)}

@router.get("/summary/{task_id}")
async def get_summary(task_id: str):
    task = celery_app.AsyncResult(task_id)
    if task.ready():
        return {"status": "completed", "result": task.result}
    return {"status": "processing"}

# Celery任务
@celery_app.task(name="app.core.tasks.process_and_summarize")
def process_and_summarize(task_id: str, file_paths: List[str], text: Optional[str], url: Optional[str]):
    try:
        summary = "这是一个测试摘要"  # 临时实现
        return {"status": "success", "summary": summary}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        # 清理临时文件
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception:
                pass 