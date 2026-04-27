# AI专业写作助手

基于FastAPI和LangGraph的流式输出AI写作助手。

## 功能特性

- 🚀 FastAPI流式API接口
- 💬 支持流式输出，实时显示AI响应
- 💾 使用SQLite持久化会话状态
- 🎨 美观的Web前端界面
- 🔧 支持多线程会话

## 项目结构

```
ai-writing/
├── api.py                 # FastAPI流式接口
├── main.py               # 原始脚本（已保留）
├── run_server.py         # 服务器启动脚本
├── templates/
│   └── index.html       # Web前端页面
├── resources/            # 数据库存储目录
└── pyproject.toml       # 项目依赖
```

## 安装依赖

```bash
uv sync
```

## 运行服务

```bash
uv run python run_server.py
```

服务启动后，访问 http://localhost:8000

## API接口

### 健康检查
```
GET /health
```

### 流式聊天
```
GET /stream/{thread_id}?message=你的消息
```

响应格式：Server-Sent Events (SSE)
- `event: message` - 消息内容
- `event: done` - 完成
- `event: error` - 错误

## 前端功能

- 📝 实时流式输出显示
- 💬 聊天历史记录
- 🎭 优雅的UI设计
- ⌨️ 支持Enter发送消息