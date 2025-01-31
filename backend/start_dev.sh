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

# 停止 Redis
sudo service redis-server stop

# 清理 Redis 数据
sudo rm -rf /var/lib/redis/dump.rdb
sudo rm -rf /var/lib/redis/appendonly.aof

# 配置 Redis
sudo tee /etc/redis/redis.conf << EOF
bind 127.0.0.1
port 6379
daemonize yes
pidfile /var/run/redis/redis-server.pid
logfile /var/log/redis/redis-server.log
dir /var/lib/redis
appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
maxmemory 256mb
maxmemory-policy allkeys-lru
EOF

# 启动 Redis
sudo service redis-server start

# 等待 Redis 完全启动
sleep 2

# 检查 Redis 状态
for i in {1..5}; do
    if redis-cli ping | grep -q 'PONG'; then
        echo "Redis is running"
        break
    fi
    if [ $i -eq 5 ]; then
        echo "Error: Redis failed to start"
        exit 1
    fi
    echo "Waiting for Redis to start... ($i/5)"
    sleep 1
done

# 清理 Redis 数据
redis-cli flushall

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

# 等待 Celery Worker 完全启动
sleep 2

# 检查 Celery Worker 是否成功启动
if ! pgrep -f "celery.*worker" > /dev/null; then
    echo "Error: Celery worker failed to start"
    exit 1
fi

# 启动服务
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --log-level debug 2>&1 | tee logs/uvicorn.log 