FROM python:3.9

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    ffmpeg \
    redis-server \
    tesseract-ocr \
    tesseract-ocr-chi-sim \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY app/ app/
COPY .env .
COPY start.sh .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 创建上传目录
RUN mkdir -p uploads

# 设置权限
RUN chmod +x start.sh

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["./start.sh"] 