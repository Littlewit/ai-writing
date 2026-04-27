import os
import sqlite3
from dotenv import load_dotenv

load_dotenv()

print("Starting test...")

try:
    from langchain.chat_models import init_chat_model
    print("[OK] LangChain imported")

    model = init_chat_model(
        model="qwen-max",
        model_provider="openai",
        api_key=os.getenv("DASHCOPE_API_KEY"),
        base_url=os.getenv("DASHCOPE_BASE_URL"),
    )
    print("[OK] Model initialized")

    from langgraph.checkpoint.sqlite import SqliteSaver
    print("[OK] Checkpoint module imported")

    connection = sqlite3.connect("resources/agent.db", check_same_thread=False)
    print("[OK] Database connected")

    checkpointer = SqliteSaver(connection)
    checkpointer.setup()
    print("[OK] Checkpointer setup complete")

    from langchain.agents import create_agent
    print("[OK] Agent module imported")

    system_prompt = """
    专业写作助手提示词（强约束+操作流程版）
    你是高标准专业写作助手。深度理解用户写作指令，严格遵守风格、字数、场景限制，内容原创无重复，语句通顺自然，结构清晰，为用户提供定制化优质写作内容。
    """

    agent = create_agent(
        model=model,
        checkpointer=checkpointer,
        system_prompt=system_prompt
    )
    print("[OK] Agent created successfully")

    print("\nAll tests passed!")

except Exception as e:
    print(f"\n[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()