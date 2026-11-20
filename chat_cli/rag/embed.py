import json, os, requests
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).parent.parent.parent / ".env"
load_dotenv(ENV_PATH)  # 加载 .env 中的变量到系统环境变量

URL = "https://api.siliconflow.cn/v1/embeddings"
KEY = os.environ["SILICONFLOW_API_KEY"]
HERE = Path(__file__).parent

def embed(texts: list[str]) -> list[list[float]]:
    r = requests.post(
        URL,
        headers={"Authorization": f"Bearer {KEY}"},
        json={"model": "BAAI/bge-m3", "input": texts},
        timeout=120,
    )
    r.raise_for_status()
    return [d["embedding"] for d in r.json()["data"]]

def load_blocks() -> list[str]:
    blocks = []
    for f in sorted((HERE / "corpus").glob("*.md")):
        blocks += [b.strip() for b in f.read_text(encoding="utf-8").split("\n\n@@BLOCK@@\n\n") if b.strip()]
    return blocks

if __name__ == "__main__":
    blocks = load_blocks()
    vectors = []
    for i in range(0, len(blocks), 10):
        vectors += embed(blocks[i:i + 10])
        print(f"已向量化 {len(vectors)}/{len(blocks)}")
    (HERE / "index.json").write_text(
        json.dumps({"blocks": blocks, "vectors": vectors}, ensure_ascii=False),
        encoding="utf-8",
    )
    print("维度：", len(vectors[0]), "｜索引已存 index.json")