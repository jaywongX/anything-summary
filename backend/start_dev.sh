#!/bin/bash

# 确保日志目录存在
mkdir -p logs

# 确保上传目录存在
mkdir -p uploads

# 启动 Celery Worker
celery -A app.celery_app worker --loglevel=DEBUG --pool=solo --logfile=logs/celery.log &

# 启动服务，同时将日志输出到文件
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug 2>&1 | tee logs/uvicorn.log 