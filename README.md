# AI专业写作助手
基于LangGraph的专业AI写作助手，支持流式输出。

## 功能特性
- ✨ 流式输出 - 实时显示AI生成内容
- 🤖 AI Agent - 专业的5步写作流程
- 💾 多轮对话 - 支持上下文记忆
- 🎨 现代UI - 简洁美观的前端界面

## 快速开始

### 本地运行
```bash
# 安装依赖
uv sync

# 复制环境变量配置
cp .env.example .env
# 编辑.env，填入你的API Key

# 启动服务
uv run python run_server.py
```

访问 http://localhost:8000

## 部署指南

### Render（推荐）
1. Fork此仓库到你的GitHub
2. 访问 [Render](https://render.com)
3. 创建新的Web Service
4. 连接你的GitHub仓库
5. 配置环境变量：
   - `DASHCOPE_API_KEY`: 你的API密钥
   - `DASHCOPE_BASE_URL`: https://dashscope.aliyuncs.com/compatible-mode/v1
6. 点击Deploy

Render会自动检测`render.yaml`配置文件进行部署。

### 推送代码到GitHub

**SSH方式**（推荐）：
```bash
# 初始化Git
cd /path/to/project
git init
git add .
git commit -m "Initial commit"

# 生成SSH密钥（如果还没有）
# ssh-keygen -t ed25519 -C "your_email@example.com"
# 然后复制 ~/.ssh/id_ed25519.pub 内容到GitHub Settings > SSH and GPG keys

# 添加SSH远程仓库
git remote add origin git@github.com:你的用户名/ai-writing.git
git push -u origin main
```

**HTTPS方式**：
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的用户名/ai-writing.git
git push -u origin main
```

### Railway
1. Fork此仓库到你的GitHub
2. 访问 [Railway](https://railway.app)
3. 创建新项目，选择"Deploy from GitHub"
4. 选择仓库
5. 添加环境变量（同上）
6. 部署

### Docker本地运行
```bash
# 构建镜像
docker build -t ai-writing .

# 运行容器
docker run -p 8000:8000 \
  -e DASHCOPE_API_KEY=your_key \
  -e DASHCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1 \
  ai-writing
```

## 技术栈

- **后端**: FastAPI + LangChain + LangGraph
- **数据库**: SQLite (AsyncSqliteSaver)
- **AI模型**: 通义千问 (qwen-max)
- **前端**: Vanilla HTML/CSS/JS + SSE

## 项目结构
```
├── api.py              # FastAPI应用
├── run_server.py      # 服务器启动脚本
├── main.py            # 主程序入口
├── pyproject.toml     # 项目配置
├── Dockerfile          # Docker配置
├── render.yaml         # Render部署配置
├── templates/
│   ├── index.html     # 前端页面
│   └── favicon.ico   # 网站图标
├── resources/         # 数据库存储
└── .env               # 环境变量（不提交）
```

## 注意事项

- 免费版Render服务会在闲置后休眠，首次访问可能有延迟
- 确保API Key安全，不要提交到GitHub
- 生产环境建议使用付费套餐

## License
MIT