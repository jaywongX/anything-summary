from app.celery_app import celery_app
from typing import List, Optional
from app.services.ali_summary_service import AliSummaryService
import logging
import asyncio
import os

logger = logging.getLogger(__name__)
summary_service = AliSummaryService()

@celery_app.task(bind=True)
def process_and_summarize(self, task_id: str, file_paths: List[str], text: Optional[str], url: Optional[str]):
    """
    处理和总结内容的 Celery 任务
    """
    try:
        logger.info(f"Starting task {self.request.id} with params: files={file_paths}, text_length={len(text) if text else 0}, url={url}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        results = []
        
        # 处理文件
        if file_paths:
            logger.info(f"Processing {len(file_paths)} files")
            for file_path in file_paths:
                try:
                    logger.info(f"Processing file: {file_path}")
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        logger.info(f"File content length: {len(content)}")
                        summary = loop.run_until_complete(summary_service.summarize(content))
                        results.append(f"文件 {file_path} 摘要:\n{summary}")
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {str(e)}", exc_info=True)
                    results.append(f"处理文件 {file_path} 失败: {str(e)}")

        # 处理文本
        if text and text.strip():
            logger.info(f"Processing text with length: {len(text)}")
            try:
                summary = loop.run_until_complete(summary_service.summarize(text))
                results.append(f"文本摘要:\n{summary}")
            except Exception as e:
                logger.error(f"Error processing text: {str(e)}", exc_info=True)
                results.append(f"处理文本失败: {str(e)}")

        # 处理URL
        if url and url.strip():
            logger.info(f"Processing URL: {url}")
            try:
                summary = loop.run_until_complete(summary_service.summarize_url(url))
                results.append(f"URL摘要:\n{summary}")
            except Exception as e:
                logger.error(f"Error processing URL: {str(e)}", exc_info=True)
                results.append(f"处理URL失败: {str(e)}")

        if not results:
            logger.warning("No content was processed")
            results.append("没有找到需要处理的内容")

        summary_text = "\n\n".join(results)
        logger.info(f"Task {self.request.id} completed successfully with summary length: {len(summary_text)}")
        return {
            "status": "success",
            "summary": summary_text
        }
    except Exception as e:
        logger.error(f"Task {self.request.id} failed: {str(e)}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }
    finally:
        try:
            loop.close()
        except:
            pass
        # 清理临时文件
        for file_path in file_paths:
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logger.error(f"Error cleaning up file {file_path}: {str(e)}") 