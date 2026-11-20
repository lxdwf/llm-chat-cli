"""W3-D3 检索：把问题向量化，用余弦相似度取 top-k 文本块。"""
import json
import math
from pathlib import Path

from embed import embed

HERE = Path(__file__).parent
data = json.loads((HERE / "index.json").read_text(encoding="utf-8"))


def cosine(a, b):
    """余弦相似度：点积除以两个模长，只看方向，不看长度。"""
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb)


def search(question: str, k: int = 3):
    """返回 [(相似度, 文本块), ...]，按相似度从高到低。"""
    qv = embed([question])[0]
    scored = [(cosine(qv, v), i) for i, v in enumerate(data["vectors"])]
    scored.sort(reverse=True)
    return [(s, data["blocks"][i]) for s, i in scored[:k]]


if __name__ == "__main__":
    for score, block in search("哪些岗位要求 Dify？"):
        print(f"{score:.3f} | {block[:80].replace(chr(10), ' / ')}")
