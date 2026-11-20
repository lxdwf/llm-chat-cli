import json, math
from pathlib import Path
from embed import embed

HERE = Path(__file__).parent
data = json.loads((HERE / "index.json").read_text(encoding="utf-8"))

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot #/ (na * nb)                     # ← 少了分母，长块会被排前面

def search(question: str, k: int = 3):
    qv = embed([question])[0]
    scored = [(cosine(qv, v), i) for i, v in enumerate(data["vectors"])]
    scored.sort(reverse=True)
    return [(s, data["blocks"][i]) for s, i in scored[:k]]

if __name__ == "__main__":
    for score, block in search("哪些岗位要求 Dify？"):
        print(f"{score:.3f} | {block[:80].replace(chr(10), ' / ')}")
    #for score, block in search("工作地点在哪"):
    #    print(f"{score:.3f} | {block[:80].replace(chr(10), ' / ')}")
    #for score, block in search("对学历要求高不高"):
     #   print(f"{score:.3f} | {block[:80].replace(chr(10), ' / ')}")
