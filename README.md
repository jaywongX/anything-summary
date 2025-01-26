# Anything Summary

Anything Summary 是一个智能文本摘要系统，支持多种格式内容的智能提取和摘要生成。

![项目截图](docs/screenshot.png)

## 功能特性

- 支持多种格式的内容提取和摘要：
  - 网页链接 (URL)
  - PDF文档 (.pdf)
  - Word文档 (.docx)
  - 纯文本文件 (.txt)
  - 音频文件 (.mp3, .wav)
  - 视频文件 (.mp4, .avi)
- 智能文本摘要生成
- 异步任务处理
- RESTful API接口
- 跨域支持

## 快速开始

### 后端部署（WSL Ubuntu）

1. 安装系统依赖

bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv redis-server ffmpeg

2. 创建并激活虚拟环境

bash
cd backend
python3 -m venv venv
source venv/bin/activate

3. 安装Python依赖

bash
pip install -r requirements.txt

4. 创建并配置环境变量文件 `.env`：

bash
# API配置
API_HOST=0.0.0.0
API_PORT=8000

# CORS配置
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# Redis配置
REDIS_HOST=localhost
REDIS_PORT=6379

# 文件上传配置
UPLOAD_DIR=uploads
MAX_FILE_SIZE=104857600  # 100MB

5. 启动服务（需要开三个终端）

bash
# 终端1：Redis服务
sudo service redis-server start

# 终端2：Celery Worker
source venv/bin/activate
celery -A app.celery_app worker --loglevel=info

# 终端3：FastAPI服务
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

### 前端部署（Windows）

1. 安装依赖

bash
cd frontend
npm install

2. 配置 `vite.config.js`，替换为实际的 WSL IP 地址

javascript
const WSL_IP = '172.29.223.73'  // 使用实际的IP地址

3. 启动开发服务器

bash
npm run dev

## 技术栈

### 后端
- Python 3.9+
- FastAPI (Web框架)
- Celery + Redis (异步任务队列)
- PyPDF2 (PDF解析)
- python-docx (Word文档解析)
- FFmpeg (音视频处理)

### 前端
- Vue 3
- Vite
- Vue Router
- Uppy (文件上传)

## 项目结构

```bash
anything-summary/
├── backend/                # 后端代码
│   ├── app/               # 应用程序代码
│   │   ├── __init__.py
│   │   ├── main.py       # FastAPI主程序
│   │   ├── config.py     # 配置文件
│   │   ├── celery_app.py # Celery配置
│   │   ├── api/          # API接口
│   │   │   ├── __init__.py
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── summary.py
│   │   └── core/         # 核心功能
│   │       ├── __init__.py
│   │       ├── file_processor.py
│   │       └── summarizer.py
│   ├── uploads/          # 文件上传目录
│   ├── requirements.txt  # Python依赖
│   └── start.sh         # 启动脚本
│
├── frontend/              # 前端代码
│   ├── public/           # 静态资源
│   ├── src/              # 源代码
│   │   ├── assets/      # 资源文件
│   │   ├── components/  # 组件
│   │   └── views/       # 页面
│   ├── package.json
│   └── vite.config.js
```

## API文档

启动服务后访问：`http://localhost:8000/docs`

## 常见问题

1. Redis连接失败

bash
sudo service redis-server restart

2. 文件上传失败

bash
# 检查uploads目录权限
chmod 777 backend/uploads

3. 端口被占用

bash
# 查看占用进程
sudo lsof -i :8000
# 结束进程
sudo kill -9 <PID>

## 许可证

[MIT License](LICENSE)

## 联系方式

- Email：jaywong001011@gmail.com

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 开发环境

- Python 3.9+
- Node.js 16+
- Redis 6+
- WSL2 (Windows)

## 本地开发

1. 克隆项目
```bash
git clone https://github.com/jaywong001011/anything-summary.git
cd anything-summary
```

2. 配置环境变量
```bash
# 后端
cp backend/.env.example backend/.env

# 前端
cp frontend/.env.example frontend/.env
```

3. 按照上述部署步骤运行项目



