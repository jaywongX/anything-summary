#!/bin/bash

# 确保日志目录存在
mkdir -p logs

# 确保上传目录存在
mkdir -p uploads

# 激活虚拟环境
source venv/bin/activate

# 停止现有进程
pkill -f celery
pkill -f uvicorn
sudo kill -9 $(sudo lsof -t -i:8000) 2>/dev/null || true

# 清空日志
> logs/app.log
> logs/celery.log
> logs/uvicorn.log

# 清理 PID 文件
rm -f logs/celery.pid

# 启动 Celery Worker
celery -A app.celery_app worker \
    --loglevel=DEBUG \
    -Q default \
    --pool=solo \
    --concurrency=1 \
    --max-tasks-per-child=200 \
    --logfile=logs/celery.log \
    --pidfile=logs/celery.pid \
    --detach

# 检查 Celery Worker 是否成功启动
if ! pgrep -f "celery.*worker" > /dev/null; then
    echo "Error: Celery worker failed to start"
    exit 1
fi

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug 2>&1 | tee logs/uvicorn.log 