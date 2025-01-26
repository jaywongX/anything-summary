from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import summary
from app.config import settings

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
        from app.celery_app import celery_app
        return celery_app.control.inspect().active()
    except:
        return False

# 注册路由
app.include_router(summary.router, prefix="/api", tags=["summary"]) 