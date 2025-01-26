#!/bin/bash

# 创建必要的目录
mkdir -p uploads

# 启动Redis（如果没有使用外部Redis）
redis-server &

# 启动Celery Worker
celery -A app.celery_app worker --loglevel=info &

# 启动FastAPI应用
uvicorn app.main:app --host ${API_HOST:-0.0.0.0} --port ${API_PORT:-8000} --reload 