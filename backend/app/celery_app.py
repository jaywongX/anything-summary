from celery import Celery
from app.config import settings
import base64

# 创建 Celery 实例
celery_app = Celery(
    'app',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# 配置 Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,
    result_expires=3600,
    task_ignore_result=False,
    broker_connection_retry_on_startup=True,
    imports=['app.core.tasks'],  # 明确导入任务模块
)

# 自动发现任务
celery_app.autodiscover_tasks(['app.core'])

@celery_app.task(bind=True, name="process_summary")
def process_summary(self, file_content_b64, file_type, file_name):
    """处理文件内容的 Celery 任务"""
    try:
        from services.parser_service import ParserService
        
        # 解码文件内容
        file_content = base64.b64decode(file_content_b64)
        
        parser = ParserService()
        
        if file_type == 'text/plain':
            text = parser.parse_txt(file_content)
        elif file_type == 'application/pdf':
            text = parser.parse_pdf(file_content)
        elif file_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            text = parser.parse_docx(file_content)
        else:
            text = f"不支持的文件类型: {file_type}"
        
        return {
            'success': True,
            'text': f"文件 {file_name} 内容: {text}"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"处理文件 {file_name} 失败: {str(e)}"
        } 