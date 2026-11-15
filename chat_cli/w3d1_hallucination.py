"""W2-D6 · Prompt A/B 对比

同一段 JD，只换 system 提示词，看输出质量差多少。
BAD  = 一句话指令
GOOD = prompts/jd_parse.md 五段模板
"""
from prompt_loader import load_prompt
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],   # 缺配置立刻 KeyError
    base_url="https://api.deepseek.com",
)

QUESTIONS = [
    "卓望公司的 AI 应用开发岗在哪些城市？",          # 资料内有
    "联通湖北这个岗要求英语几级？",                  # 资料内有
    "字节跳动的 AI 应用岗薪资多少？",                # 资料内没有 ← 关键题
]


# 要对比的两份提示词，装在字典里：key 是标签，value 是提示词正文
PROMPTS = {
    "BARE": "你是求职顾问，回答简短。请以 JSON 格式返回结果，包含 answer 字段存储回答内容。",                 # 一句话，没有角色/上下文/字段名
    "STUFFED" : """你是求职顾问。只能依据下面资料回答，资料里没有就说"资料未提及"。
            资料：
         1. 卓望公司 AI应用开发（27届校招）：北京/广州/昆明/西安，本科+，要求 Python或Java/Go一门；大模型API/Prompt；Dify/LangChain/向量库/RAG优先。
         2. 联通湖北省分公司 AI Agent开发工程师：武汉，校招本科，Python+RESTful/JSON；Dify/FastGPT/LangChain低代码；英语四级。
         3. 美亚柏科 AI开发工程师(Agent)：广州，校招本科，Python；LangChain/AutoGPT；RAG/工具调用原理。""",          
}


def ask(system_prompt: str,question: str):
    """发一次请求。成功返回 dict，失败返回 None"""
    resp = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {"role": "system", "content":system_prompt},
            {"role": "user", "content": question},
        ],
        response_format={"type": "json_object"},          # 强制输出 JSON
        extra_body={"thinking": {"type": "disabled"}},    # 关思考，排除干扰
        max_tokens=800,
    )
    text = resp.choices[0].message.content
    if not text or not text.strip():
        return None
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

if __name__ == "__main__":
    for prompt_name, prompt_text in PROMPTS.items():
        print(f"\n===== 测试提示词：{prompt_name} =====")
        for q in QUESTIONS:
            result = ask(prompt_text, q)
            print(f"问题：{q}")
            print(f"回答：{result}")


