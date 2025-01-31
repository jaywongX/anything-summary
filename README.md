# Anything Summary

一站式智能内容总结工具，支持多模态混合输入。

One-stop intelligent content summary tool, supporting multi-modal mixed input.

## 功能特点 / Features

- 多种输入方式 / Multiple input methods
  - 文本输入 / Text input
  - 网页链接 / Web URL
  - 文件上传 / File upload
- 支持多种文件格式 / Multiple file formats support
  - 文档：PDF、Word、TXT / Documents: PDF, Word, TXT
  - 图片：JPG、PNG、GIF（支持OCR） / Images: JPG, PNG, GIF (with OCR)
  - 音频：MP3、WAV / Audio: MP3, WAV
  - 视频：MP4、AVI / Video: MP4, AVI
  - 压缩包：ZIP、RAR、7Z / Archives: ZIP, RAR, 7Z
- 多语言支持 / Multi-language Support
  - 中文 / Chinese
  - 英文 / English

## 部署和启动 / Deployment and Launch

### 环境要求 / Requirements

#### 前端 / Frontend
- Node.js >= 16
- npm >= 8
- Vue 3
- 必需的依赖包 / Required dependencies:
  - vue-i18n@9 (多语言支持 / i18n support)
  - @uppy/core, @uppy/dashboard (文件上传 / file upload)
  - vue-router@4 (路由 / routing)

#### 后端 / Backend
- Python >= 3.8
- 必需的 Python 包已列在 requirements.txt / Required Python packages are listed in requirements.txt

### 前端部署 / Frontend Deployment
bash
进入前端目录 / Enter frontend directory
cd frontend
安装依赖 / Install dependencies
npm install
开发环境启动 / Start development server
npm run dev
生产环境构建 / Build for production
npm run build

### 后端部署 / Backend Deployment
bash
# 进入后端目录 / Enter backend directory
cd backend
# 创建并激活虚拟环境 / Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或者在 Windows 下 / Or on Windows
# .\venv\Scripts\activate

# 安装依赖 / Install dependencies
pip install -r requirements.txt

# 安装 Redis (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install redis-server

# 启动 Redis 服务 / Start Redis service
sudo service redis-server start

# 启动 Celery Worker / Start Celery Worker (新终端 / New terminal)
celery -A app.celery_app worker --loglevel=info

# 启动开发服务器 / Start development server (新终端 / New terminal)
sh start_dev.sh
# 或者在 Windows 环境下 / Or on Windows
# python app.py

### 配置说明 / Configuration

1. 前端配置 / Frontend Configuration
   - 在 `.env` 文件中配置 API 地址 / Configure API URL in `.env` file
   - 默认语言设置在 `src/i18n/index.ts` / Default language settings in `src/i18n/index.ts`
   - 支持的文件类型配置在 `src/views/SummaryPage.vue` / Supported file types in `src/views/SummaryPage.vue`

2. 后端配置 / Backend Configuration
   - 配置文件位于 `config.py` / Configuration file in `config.py`
   - 可配置项包括：服务端口、数据库连接、文件上传限制等 / Configurable items include: service port, database connection, file upload limits, etc.

### 常见问题 / Common Issues

1. ModuleNotFoundError: No module named 'celery' / celery 模块未找到:
```bash
# 确保在虚拟环境中安装 celery
pip install celery redis
```

2. Redis 连接问题 / Redis connection issues:
```bash
# 检查 Redis 服务状态 / Check Redis service status
sudo service redis-server status

# 重启 Redis 服务 / Restart Redis service
sudo service redis-server restart
```

3. 依赖安装问题 / Dependency installation issues:
bash
清除 npm 缓存后重新安装 / Clear npm cache and reinstall
npm clean-cache --force
npm install

4. 跨域问题 / CORS issues:
   - 检查 vite.config.ts 中的代理配置 / Check proxy configuration in vite.config.ts
   - 确保后端已正确配置 CORS / Ensure backend CORS is properly configured

5. 文件上传问题 / File upload issues:
   - 检查文件大小是否超过限制（默认 100MB） / Check if file size exceeds limit (default 100MB)
   - 确认文件类型是否在支持列表中 / Verify file type is in supported list

### 开发指南 / Development Guide

1. 添加新的语言支持 / Add new language support:
   - 在 `src/locales` 目录下创建新的语言文件 / Create new language file in `src/locales`
   - 在 `src/i18n/index.ts` 中注册新语言 / Register new language in `src/i18n/index.ts`

2. 修改或添加翻译 / Modify or add translations:
   - 编辑 `src/locales` 目录下的语言文件 / Edit language files in `src/locales`
   - 遵循已有的键值结构 / Follow existing key-value structure

## 贡献 / Contributing

欢迎提交 Pull Request 或 Issue。

Pull requests and issues are welcome.

## 许可证 / License

[MIT License](LICENSE)