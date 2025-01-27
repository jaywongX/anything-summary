from fastapi import FastAPI, UploadFile, Form, File, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import summary
from app.config import settings
from typing import List, Optional
from services.parser_service import ParserService
from app.core.logging_config import setup_logging
from app.celery_app import celery_app, process_summary
import base64

# 设置日志
logger = setup_logging()

app = FastAPI(title="Anything Summary API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加健康检查端点
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "redis": "running" if check_redis() else "not running",
            "celery": "running" if check_celery() else "not running"
        }
    }

def check_redis():
    try:
        from redis import Redis
        redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
        return redis.ping()
    except:
        return False

def check_celery():
    try:
        return celery_app.control.inspect().active()
    except:
        return False

# 注册路由
app.include_router(summary.router, prefix="/api", tags=["summary"])

@app.post("/api/summary")
async def generate_summary(
    files: List[UploadFile] = File(default=[]),
):
    try:
        logger.info("Received summary request")
        
        # 检查是否收到文件
        if not files:
            logger.warning("No files received")
            return JSONResponse(
                status_code=400,
                content={
                    'success': False,
                    'error': "请上传至少一个文件"
                }
            )
            
        logger.info(f"Received {len(files)} files")
        tasks = []
        
        # 为每个文件创建异步任务
        for file in files:
            logger.info(f"Processing file: {file.filename}, type: {file.content_type}")
            try:
                contents = await file.read()
                # 将文件内容转换为base64以便序列化
                content_b64 = base64.b64encode(contents).decode('utf-8')
                
                # 创建异步任务
                task = process_summary.apply_async(args=[content_b64, file.content_type, file.filename])
                tasks.append(task)
                
            except Exception as e:
                logger.error(f"Error processing file {file.filename}: {str(e)}", exc_info=True)
                return JSONResponse(
                    status_code=500,
                    content={
                        'success': False,
                        'error': f"处理文件失败: {str(e)}"
                    }
                )

        # 等待所有任务完成
        results = []
        for task in tasks:
            try:
                result = task.get(timeout=30)  # 30秒超时
                if result['success']:
                    results.append(result['text'])
                else:
                    results.append(result['error'])
            except Exception as e:
                logger.error(f"Task failed: {str(e)}")
                results.append(f"任务处理失败: {str(e)}")

        if not results:
            logger.warning("No content processed")
            return JSONResponse(
                status_code=400,
                content={
                    'success': False,
                    'error': "没有找到可处理的内容"
                }
            )

        response = {
            'success': True,
            'summary': '\n\n'.join(results)
        }
        logger.info("Successfully processed request")
        return JSONResponse(content=response)

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                'success': False,
                'error': str(e)
            }
        ) 