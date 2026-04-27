FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY pyproject.toml ./
RUN pip install uv && uv sync

# 复制代码
COPY . .

# Render 默认使用 10000 端口
EXPOSE 10000

# 启动命令
CMD ["uv", "run", "python", "run_server.py"]