# 后端容器化配置
# 使用官方 Python 3.10 镜像作为基础
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 复制 requirements.txt
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 暴露 8000 端口
EXPOSE 8000

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]