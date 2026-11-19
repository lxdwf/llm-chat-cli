"""W3-D2 对照组：坏切块 corpus_bad

和 build_corpus.py 唯一的差别：不分类型、不认标题、不认表格行，
把每个来源的原文压成一条流水，按固定 200 字硬切。

保留【来源：X】来源头 —— 这样 D6 的 E1 才是单变量对照：
  E1-②（本文件）只变「切块方式」，来源头不动
  E1-③（四源切法 + 去掉来源头）只变「来源头」，切块方式不动
两处都改，D6 就无法归因到底是哪个起的作用。
"""
import re
from pathlib import Path

BASE = Path(r"D:/app/obsidian/个人档案/E学习计划/AI学习计划")
OUT = Path(__file__).parent / "corpus_bad"

BLOCK_SEP = "\n\n@@BLOCK@@\n\n"
SIZE = 200                       # 固定 200 字，不设 overlap

SOURCES = [
    ("岗位库",   BASE / "13_AI应用Agent岗位信息库_100家.md"),
    ("技能清单", BASE / "06_IT求职方向_岗位锁定与技能清单.md"),
    ("市场调研", BASE / "07_IT求职市场调研_2026秋.md"),
    ("职业规划", BASE / "12_职业规划报告_计算机2027届.md"),
]


def hard_cut(path, size=SIZE):
    """剥 frontmatter → 抹平所有换行和标题符号 → 按固定字数硬切"""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"-{3,}", "—", text)
    text = re.sub(r"\s+", " ", text).strip()        # 抹平换行：没有行边界 = 不能按行切
    return [text[i:i + size] for i in range(0, len(text), size)
            if len(text[i:i + size]) >= 80]         # 同样过滤噪声尾块


def build():
    OUT.mkdir(exist_ok=True)
    all_blocks = []
    for name, path in SOURCES:
        blocks = [f"【来源：{name}】\n{b}" for b in hard_cut(path)]
        print(f"{name}: {len(blocks)} 块")
        all_blocks += blocks
        for i in range(0, len(blocks), 25):
            (OUT / f"{name}_part{i // 25 + 1}.md").write_text(
                BLOCK_SEP.join(blocks[i:i + 25]), encoding="utf-8", newline="\n")

    lens = [len(b) for b in all_blocks]
    print(f"合计 {len(all_blocks)} 块｜最短 {min(lens)}｜中位 {sum(lens) // len(lens)}｜最长 {max(lens)}")


if __name__ == "__main__":
    build()
