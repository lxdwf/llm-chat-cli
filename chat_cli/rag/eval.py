"""W3-D4 评测：对 13 道题逐题调用 ask()，打印检索结果和回答。

先手工判分，不要急着写自动判分；判分标准还会随实验变化。
"""
import json
from pathlib import Path

from ask import ask

HERE = Path(__file__).parent
testset = json.loads((HERE / "testset.json").read_text(encoding="utf-8"))


def main():
    for n, item in enumerate(testset, 1):
        k = 5 if item["type"] in {"multi", "cross"} else 3
        answer, hits = ask(item["q"], k)

        print(f"\n{'=' * 60}")
        print(f"第 {n} 题 [{item['type']}] {item['q']}")
        print(f"检索 top-{k}：")
        for rank, (score, block) in enumerate(hits, 1):
            snippet = block[:100].replace("\n", " / ") if block else ""
            print(f"  {rank}. {score:.3f} | {snippet}")
        print(f"回答：{answer}")


if __name__ == "__main__":
    main()
