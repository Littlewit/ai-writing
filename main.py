import os
import sqlite3
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain.messages import HumanMessage

# 加载环境变量
load_dotenv()

# 初始化聊天模型
model = init_chat_model(
    model="qwen-max",
    model_provider="openai",
    api_key=os.getenv("DASHCOPE_API_KEY"),
    base_url=os.getenv("DASHCOPE_BASE_URL"),
)

# 连接sqlite数据库
# 如果数据库不存在，会自动创建一个
connection = sqlite3.connect("resources/agent.db", check_same_thread=False)
# 初始化checkpointer
checkpointer = SqliteSaver(connection)
# 自动建表
checkpointer.setup()

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


# 创建智能体
agent = create_agent(
    model=model,
    checkpointer=checkpointer,
    system_prompt=system_prompt
)

modal_messages = HumanMessage("你好")
# 执行智能体，包含checkpointer配置
# response = agent.invoke(
#     modal_messages,
#     config={
#         "configurable": {
#             "thread_id": "test_thread_1"
#         }
#     }
# )
# 提取并打印最后一条消息的内容
# if 'messages' in response and len(response['messages']) > 0:
#     last_message = response['messages'][-1]
#     print(last_message.content)
# if __name__ == "__main__":
#     main()
