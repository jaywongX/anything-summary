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
    """
    处理和总结内容的 Celery 任务
    """
    try:
        # 设置任务状态为开始
        self.update_state(state='STARTED')
        
        logger.info(f"Starting task {task_id}")
        logger.info(f"Task parameters: files={file_paths}, text_length={len(text) if text else 0}, url={url}")
        
        use_llm = settings.USE_LLM
        logger.info(f"USE_LLM={use_llm}")
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = []
        
        # 验证输入
        if not any([file_paths, text, url]):
            logger.warning("No input provided")
            return {
                "status": "error",
                "error": "请提供至少一项需要处理的内容（文件、文本或URL）"
            }

        # 处理文件
        if file_paths:
            logger.info(f"Processing {len(file_paths)} files")
            for file_path in file_paths:
                try:
                    logger.info(f"Processing file: {file_path}")
                    content = document_parser.parse_file(file_path)
                    if content:
                        file_name = os.path.basename(file_path)
                        results.append(f"文件 {file_name} 内容:\n{content}")
                        logger.info(f"Successfully processed file {file_name}, content length: {len(content)}")
                    else:
                        logger.warning(f"No content extracted from file: {file_path}")
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}", exc_info=True)
                    return {
                        "status": "error",
                        "error": f"处理文件失败: {str(e)}"
                    }

        # 处理文本
        if text:
            logger.info("Processing text input")
            results.append(f"文本内容:\n{text}")

        # 处理URL
        if url:
            logger.info(f"Processing URL: {url}")
            try:
                url_content = document_parser.parse_url(url)
                if url_content:
                    results.append(f"URL内容:\n{url_content}")
                    logger.info(f"Successfully processed URL, content length: {len(url_content)}")
            except Exception as e:
                logger.error(f"Error processing URL: {str(e)}", exc_info=True)
                return {
                    "status": "error",
                    "error": f"处理URL失败: {str(e)}"
                }

        if not results:
            logger.warning("No content was processed")
            return {
                "status": "error",
                "error": "没有找到需要处理的内容"
            }

        # 合并所有内容
        combined_text = "\n\n".join(results)
        logger.info(f"Combined text length: {len(combined_text)}")

        # 根据USE_LLM决定是否使用大模型
        if use_llm:
            logger.info("Using LLM for summarization")
            try:
                summary = loop.run_until_complete(summary_service.summarize(combined_text))
                logger.info(f"Summary length: {len(summary)}")
                result_summary = summary
            except Exception as e:
                logger.error(f"Error summarizing content: {str(e)}", exc_info=True)
                return {
                    "status": "error",
                    "error": f"总结失败: {str(e)}"
                }
        else:
            logger.info("LLM is disabled, returning original content")
            result_summary = combined_text

        # 准备结果
        result = {
            "status": "success",
            "summary": result_summary
        }
        
        # 确保结果被存储到 Redis
        logger.info(f"[STORE] Starting to store result for task {task_id}")
        try:
            self.backend.store_result(
                task_id,
                result,
                'SUCCESS',
                request=self.request
            )
            logger.info(f"[STORE] Successfully stored result for task {task_id}")
        except Exception as e2:
            logger.error(f"[STORE] Storage methods failed for task {task_id}. Errors: {e}, {e2}", exc_info=True)
            raise
        
        logger.info(f"Task {task_id} completed with result: {result}")
        
        # 清理文件
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):  # 添加存在检查
                    os.remove(file_path)
                    logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logger.warning(f"Failed to clean up file {file_path}: {e}")
        
        logger.info(f"Task {task_id} finished")
        return result
        
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}", exc_info=True)
        error_result = {
            "status": "error",
            "error": str(e)
        }
        # 存储错误结果
        try:
            self.backend.store_result(
                task_id,
                error_result,
                'FAILURE',
                request=self.request
            )
            logger.info(f"Task {task_id} error result stored in Redis")
        except Exception as store_error:
            logger.error(f"Failed to store error result: {store_error}", exc_info=True)
            
        raise self.retry(exc=e, countdown=5)
    finally:
        try:
            loop.close()
        except:
            pass
        logger.info(f"Task {task_id} finished") 