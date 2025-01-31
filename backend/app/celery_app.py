from celery import Celery
from kombu import Queue
from app.config import settings
import redis
import logging

REDIS_URL = 'redis://localhost:6379'

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s: %(levelname)s/%(processName)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

# 确保所有相关的日志记录器都使用相同的配置
for logger_name in ['app.core.tasks', 'celery', 'celery.task']:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

# 测试 Redis 连接
def test_redis_connection():
    try:
        client = redis.Redis.from_url(REDIS_URL)
        client.ping()
        return True
    except redis.ConnectionError as e:
        print(f"Redis connection error: {e}")
        return False

# 确保 Redis 连接正常
if not test_redis_connection():
    raise Exception("Cannot connect to Redis")

# 创建 Celery 实例
celery_app = Celery(
    'app',
    broker=f'{REDIS_URL}/0',
    backend=f'{REDIS_URL}/0',
    include=['app.core.tasks']
)

# 配置 Celery
celery_app.conf.update(
    result_expires=3600,  # 结果在 Redis 中保存 1 小时
    task_track_started=True,  # 跟踪任务开始状态
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_time_limit=300,
    task_ignore_result=False,
    broker_connection_retry=True,
    broker_connection_retry_on_startup=True,
    broker_connection_max_retries=None,
    broker_connection_timeout=10,
    broker_heartbeat=10,
    broker_pool_limit=None,  # 不限制连接池大小
    result_backend_transport_options={
        'retry_policy': {
            'timeout': 5.0,
            'max_retries': 3,
            'interval_start': 0,
            'interval_step': 0.2,
            'interval_max': 0.5,
        },
        'socket_timeout': 5.0,
        'socket_connect_timeout': 5.0,
        'retry_on_timeout': True
    },
    task_store_errors_even_if_ignored=True,
    task_soft_time_limit=250,
    task_publish_retry=True,
    task_publish_retry_policy={
        'max_retries': 3,
        'interval_start': 0,
        'interval_step': 0.2,
        'interval_max': 0.5,
    },
    task_default_queue='default',
    task_queues=(
        Queue('default', routing_key='default'),
    ),
    task_default_exchange='default',
    task_default_routing_key='default',
    worker_send_task_events=True,
    task_send_sent_event=True,
    worker_max_tasks_per_child=200,  # 每个worker进程处理200个任务后重启
    worker_prefetch_multiplier=1,  # 每个worker一次只处理一个任务
    worker_lost_wait=30,
    worker_state_db='worker_state',
    broker_heartbeat_checkrate=2,
    event_queue_ttl=10,
    event_queue_expires=10,
    worker_concurrency=1,  # 限制worker并发数为1
    task_acks_late=True,  # 任务完成后再确认
    task_reject_on_worker_lost=True,  # worker丢失时拒绝任务
    redis_backend_use_ssl=False,
    redis_socket_keepalive=True,
    redis_retry_on_timeout=True,
    redis_socket_connect_timeout=30,
    redis_max_connections=None,  # 不限制 Redis 最大连接数
)

# 显式注册任务路由
celery_app.conf.task_routes = {
    'app.core.tasks.process_and_summarize': {'queue': 'default'}
}

# 自动发现任务
celery_app.autodiscover_tasks(['app.core'])

def check_redis_connection():
    """检查 Redis 连接并打印详细信息"""
    try:
        client = redis.Redis.from_url(REDIS_URL)
        info = client.info()
        print(f"Redis version: {info['redis_version']}")
        print(f"Connected clients: {info['connected_clients']}")
        print(f"Used memory: {info['used_memory_human']}")
        return True
    except Exception as e:
        print(f"Redis connection error: {e}")
        return False

# 在启动时检查
if not check_redis_connection():
    raise Exception("Cannot connect to Redis") 