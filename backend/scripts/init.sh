#!/bin/bash

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 创建必要的目录
mkdir -p uploads

# 设置权限
chmod 777 uploads
chmod +x start.sh 