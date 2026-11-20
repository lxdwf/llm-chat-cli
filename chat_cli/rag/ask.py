"""W3-D4 生成：检索 top-k 块，拼进提示词，让聊天模型带引用回答。"""
import os
import sys
from pathlib import Path

from openai import OpenAI

CHAT_CLI_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CHAT_CLI_DIR))

from prompt_loader import load_prompt
from search import search

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)
SYSTEM = load_prompt("rag_answer")


def ask(question: str, k: int = 3):
    """返回 (回答, 检索结果)；检索结果用于核对引用和做错题归因。"""
    hits = search(question, k)
    context = "\n\n".join(f"[{i + 1}] {b}" for i, (_, b) in enumerate(hits))
    resp = client.chat.completions.create(
        model=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"【资料】\n{context}\n\n【问题】{question}"},
        ],
        max_tokens=500,
        temperature=0,
    )
    return resp.choices[0].message.content, hits


if __name__ == "__main__":
    answer, hits = ask("哪些岗位要求 Dify？")
    print(answer)
    print("\n检索到的块：")
    for i, (score, block) in enumerate(hits, 1):
        snippet = block[:100].replace("\n", " / ")
        print(f"[{i}] {score:.3f} | {snippet}")
