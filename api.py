import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from langchain.messages import HumanMessage
import json

load_dotenv()

model = None

system_prompt = """
专业写作助手提示词（强约束+操作流程版）
你是高标准专业写作助手。深度理解用户写作指令，严格遵守风格、字数、场景限制，内容原创无重复，语句通顺自然，结构清晰，为用户提供定制化优质写作内容。
操作流程严格遵循以下步骤，确保产出精准贴合需求：
1. 第一步：精准拆解需求——先明确用户核心写作目的（如文案、公文、短文等）、具体要求（字数范围、语言风格、结构排版、核心侧重点）及场景适配需求，不遗漏任何约束条件。
2. 第二步：搭建内容框架——根据需求快速梳理核心逻辑，确定内容结构（如开头、主体、结尾，或分点逻辑），确保框架清晰、贴合需求，避免后续内容偏离方向。
3. 第三步：原创内容创作——按照搭建的框架，结合约束要求，撰写原创内容，规避冗余表述、语句不通、逻辑混乱等问题，确保内容无抄袭、无重复，贴合指定风格。
4. 第四步：合规校验——完成初稿后，逐一核对用户所有要求（风格、字数、场景、结构等），修正不符合约束的内容，优化语句流畅度，确保产出完全符合用户指令。
5. 第五步：交付优化——若用户有补充、修改需求，快速响应，精准调整，直至产出满足用户全部要求的优质写作内容。
"""

async def initialize_model():
    """初始化模型，失败时返回None"""
    global model
    try:
        from langchain.chat_models import init_chat_model
        
        api_key = os.getenv("DASHCOPE_API_KEY")
        base_url = os.getenv("DASHCOPE_BASE_URL")
        
        if not api_key:
            print("Warning: DASHCOPE_API_KEY not set")
            return None
            
        model = init_chat_model(
            model="qwen-max",
            model_provider="openai",
            api_key=api_key,
            base_url=base_url,
        )
        print("Model initialized successfully")
        return model
    except Exception as e:
        print(f"Error initializing model: {e}")
        return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化
    await initialize_model()
    yield
    # 关闭时清理
    pass

app = FastAPI(title="AI Writing Assistant API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return FileResponse("templates/index.html")

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "api_key_set": os.getenv("DASHCOPE_API_KEY") is not None
    }

@app.get("/templates/favicon.ico")
async def favicon():
    return FileResponse("templates/favicon.ico")

async def generate_stream(messages, thread_id):
    """生成流式响应"""
    if model is None:
        yield {
            "event": "error",
            "data": json.dumps({"error": "Model not initialized. Please check DASHCOPE_API_KEY."})
        }
        return
    
    try:
        # 添加system prompt作为第一条消息
        system_message = HumanMessage(content=system_prompt)
        all_messages = [system_message] + messages
        
        # 使用模型的流式输出
        full_content = ""
        async for chunk in model.astream(all_messages):
            if hasattr(chunk, 'content') and chunk.content:
                full_content += chunk.content
                try:
                    yield {
                        "event": "message",
                        "data": json.dumps({"event": "message", "content": full_content}, ensure_ascii=False)
                    }
                except Exception:
                    content_no_emoji = ''.join(c for c in full_content if ord(c) <= 0xFFFF)
                    yield {
                        "event": "message",
                        "data": json.dumps({"event": "message", "content": content_no_emoji})
                    }
        
        yield {
            "event": "done",
            "data": json.dumps({"event": "done", "status": "completed"})
        }
            
    except Exception as e:
        print(f"Error in generate_stream: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        yield {
            "event": "error",
            "data": json.dumps({"error": str(e)})
        }

@app.get("/stream/{thread_id}")
async def stream_chat(thread_id: str, message: str):
    messages = [HumanMessage(content=message)]
    
    return EventSourceResponse(
        generate_stream(messages, thread_id),
        media_type="text/event-stream"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
