from app.celery_app import celery_app
from typing import List, Optional
from app.services.ali_summary_service import AliSummaryService
from app.config import settings
import logging
import asyncio
import os
from app.services.document_parser import DocumentParser
from redis.lock import Lock
from contextlib import contextmanager
import time
import random
import json

# 确保使用正确的日志记录器
logger = logging.getLogger('app.core.tasks')

summary_service = AliSummaryService()
document_parser = DocumentParser()

@contextmanager
def redis_lock(backend, lock_key, timeout=60):
    """Redis 分布式锁"""
    lock = Lock(backend.client, lock_key, timeout=timeout)
    try:
        acquired = lock.acquire(blocking=True, blocking_timeout=5)
        if not acquired:
            raise Exception(f"Could not acquire lock for {lock_key}")
        yield
    finally:
        try:
            lock.release()
        except:
            pass

@celery_app.task(
    bind=True,
    name='app.core.tasks.process_and_summarize',
    queue='default',
    retry_backoff=True,
    retry_backoff_max=600,
    max_retries=3,
    ignore_result=False,
    track_started=True,
    acks_late=True
)
def process_and_summarize(self, task_id: str, file_paths: List[str], text: Optional[str], url: Optional[str]):
    """处理和总结内容的 Celery 任务"""
    results = []
    try:
        logger.info(f"Starting task {task_id}")
        
        # 验证只能提供一种输入
        input_count = sum([
            bool(file_paths),
            bool(text and text.strip()),
            bool(url and url.strip())
        ])
        
        if input_count == 0:
            return store_result(self.backend, task_id, {
                "status": "error",
                "error": "请提供需要处理的内容（文件、文本或URL）"
            })
        
        if input_count > 1:
            return store_result(self.backend, task_id, {
                "status": "error",
                "error": "请只选择一种输入方式（文件、文本或URL）"
            })

        # 处理 URL
        if url:
            logger.info(f"Processing URL: {url}")
            url_content = document_parser.parse_url(url)
            if url_content is None:
                return store_result(self.backend, task_id, {
                    "status": "error",
                    "error": "无法解析URL内容，请检查URL是否有效或直接复制内容"
                })
            results.append(url_content)

        # 处理文件
        if file_paths:
            logger.info(f"Processing {len(file_paths)} files")
            for file_path in file_paths:
                try:
                    content = document_parser.parse_file(file_path)
                    if content:
                        file_name = os.path.basename(file_path)
                        results.append(f"文件 {file_name} 内容:\n{content}")
                        logger.info(f"Successfully processed file {file_name}")
                    else:
                        logger.warning(f"No content extracted from file: {file_path}")
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}")
                    return store_result(self.backend, task_id, {
                        "status": "error",
                        "error": f"处理文件失败: {str(e)}"
                    })

        # 处理文本
        if text:
            logger.info("Processing text input")
            results.append(f"文本内容:\n{text}")

        # 检查是否有内容被处理
        if not results:
            return store_result(self.backend, task_id, {
                "status": "error",
                "error": "没有找到需要处理的内容"
            })

        # 合并所有内容
        combined_text = "\n\n".join(results)
        logger.info(f"Combined text length: {len(combined_text)}")

        # 根据配置决定是否使用大模型
        if settings.USE_LLM:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                summary = loop.run_until_complete(summary_service.summarize(combined_text))
                loop.close()
                result_summary = summary
            except Exception as e:
                logger.error(f"Error summarizing content: {str(e)}")
                return store_result(self.backend, task_id, {
                    "status": "error",
                    "error": f"总结失败: {str(e)}"
                })
        else:
            result_summary = combined_text

        # 存储成功结果
        result = {
            "status": "success",
            "summary": result_summary
        }
        return store_result(self.backend, task_id, result, self.request)

    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}", exc_info=True)
        return store_result(self.backend, task_id, {
            "status": "error",
            "error": str(e)
        })
    finally:
        # 清理文件
        cleanup_files(file_paths)

def store_result(backend, task_id: str, result: dict, request=None) -> dict:
    """存储任务结果到 Redis"""
    try:
        logger.info(f"Storing result for task {task_id}")
        backend.store_result(
            task_id,
            result,
            'SUCCESS',
            request=request
        )
        return result
    except Exception as e:
        logger.error(f"Failed to store result for task {task_id}: {str(e)}")
        raise

def cleanup_files(file_paths: List[str]):
    """清理上传的文件"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Cleaned up file: {file_path}")
        except Exception as e:
            logger.warning(f"Failed to clean up file {file_path}: {e}")