from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import summary
from app.config import settings
from app.core import tasks
from app.celery_app import celery_app
import logging

logger = logging.getLogger(__name__)

app = FastAPI(title="Anything Summary API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    logger.info(f"Registered tasks: {celery_app.tasks.keys()}")

# 注册路由 - 添加前缀
app.include_router(summary.router, prefix="/api")

# 错误处理中间件
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Request failed: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": str(e)
            }
        ) 