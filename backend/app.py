from fastapi import FastAPI, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from services.parser_service import ParserService
from typing import List
import logging
from logging.handlers import RotatingFileHandler
import os

# 创建日志目录
if not os.path.exists('logs'):
    os.mkdir('logs')

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 添加文件处理器
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=1024 * 1024,
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

# 添加控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info('FastAPI app startup')

@app.post("/api/summary")
async def generate_summary(
    files: List[UploadFile] = File(None),
    urls: List[str] = Form(None),
    texts: List[str] = Form(None)
):
    try:
        logger.info("Received summary request")
        parser = ParserService()
        result_text = []

        # 处理URL
        if urls:
            logger.info(f"Processing URLs: {urls}")
            for url in urls:
                if url.strip():
                    text = parser.parse_url(url)
                    result_text.append(f"URL内容: {text}")

        # 处理文本
        if texts:
            logger.info(f"Processing texts count: {len(texts)}")
            for text in texts:
                if text.strip():
                    result_text.append(f"文本内容: {text}")

        # 处理文件
        if files:
            logger.info(f"Processing files count: {len(files)}")
            for file in files:
                logger.info(f"Processing file: {file.filename}, type: {file.content_type}")
                try:
                    file_bytes = await file.read()
                    file_type = file.content_type
                    
                    if file_type == 'application/pdf':
                        text = parser.parse_pdf(file_bytes)
                    elif file_type in ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
                        text = parser.parse_docx(file_bytes)
                    elif file_type == 'text/plain':
                        text = parser.parse_txt(file_bytes)
                    else:
                        text = f"不支持的文件类型: {file_type}"
                    
                    result_text.append(f"文件 {file.filename} 内容: {text}")
                except Exception as e:
                    logger.error(f"Error processing file {file.filename}: {str(e)}")
                    result_text.append(f"处理文件 {file.filename} 失败: {str(e)}")

        response = {
            'success': True,
            'summary': '\n\n'.join(result_text)
        }
        logger.info("Successfully processed request")
        return response

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return {
            'success': False,
            'error': str(e)
        } 