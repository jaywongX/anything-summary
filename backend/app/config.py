from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 基础配置
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Anything Summary"
    
    # CORS配置
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    
    # Celery配置
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # 文件上传配置
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # ModelScope配置
    MODELSCOPE_TOKEN: str = ""
    
    # 是否使用大模型
    USE_LLM: bool = False
    
    # 阿里云API配置
    ALI_API_KEY: str = ""

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = 'utf-8'
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name == 'USE_LLM':
                return raw_val.lower() in ('true', '1', 't', 'y', 'yes')
            return raw_val

settings = Settings() 