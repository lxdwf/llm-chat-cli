import re, statistics
from pathlib import Path

BASE = Path(r"D:/app/obsidian/个人档案/E学习计划/AI学习计划")
OUT = Path(__file__).parent / "corpus"

BLOCK_SEP = "\n\n@@BLOCK@@\n\n"      # ④ 块分隔哨兵：语料里绝不出现的字符串，写和读共用这一个常量

SOURCES = [                                                 # ① 加一个来源 = 加一行
    ("岗位库",   BASE / "13_AI应用Agent岗位信息库_100家.md",     "table_row"),
    ("技能清单", BASE / "06_IT求职方向_岗位锁定与技能清单.md",   "md_section"),
    ("市场调研", BASE / "07_IT求职市场调研_2026秋.md",           "md_section"),
    ("职业规划", BASE / "12_职业规划报告_计算机2027届.md",       "md_section"),
]

def chunk_table(path):
    """表格：一行一块，且把列名写进块里（表头注入）"""
    rows = [l for l in path.read_text(encoding="utf-8").splitlines()
            if l.startswith("| ") and l.count("|") >= 7]
    blocks = []
    for r in rows:
        c = [x.strip() for x in r.strip().strip("|").split("|")]
        if len(c) < 6 or "---" in r or not c[0].isdigit():   # 只留真数据行
            continue
        blocks.append(f"公司：{c[1]}\n岗位：{c[2]}\n城市：{c[3]}\n"
                      f"学历薪资：{c[4]}\n核心要求：{c[5]}")
    return blocks

def chunk_md(path, min_len=80):
    """长文：按 ## / ### 标题切，标题留在块首（标题注入）"""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)   # ⑤ 剥掉 YAML frontmatter（它自带 --- 和噪声）
    parts = re.split(r"\n(?=#{2,3} )", text)
    return [p.strip() for p in parts if len(p.strip()) >= min_len]


def clean(block: str) -> str:
    """把块内容里的 --- （水平线、表格分隔行）换成破折号，避免和分隔符撞车"""
    return re.sub(r"-{3,}", "—", block)

def build():
    OUT.mkdir(exist_ok=True)
    all_blocks = []
    for name, path, kind in SOURCES:
        raw = chunk_table(path) if kind == "table_row" else chunk_md(path)
        blocks = [f"【来源：{name}】\n{clean(b)}" for b in raw]   # ② 来源头注入
        print(f"{name}: {len(blocks)} 块")
        all_blocks += blocks
        for i in range(0, len(blocks), 25):                    # ③ 配额：≤50 个文档
            (OUT / f"{name}_part{i // 25 + 1}.md").write_text(
                BLOCK_SEP.join(blocks[i:i + 25]), encoding="utf-8", newline="\n")
    lens = [len(b) for b in all_blocks]
    print(f"合计 {len(all_blocks)} 块｜最短 {min(lens)}｜中位 "
          f"{statistics.median(lens):.0f}｜最长 {max(lens)}")

if __name__ == "__main__":
    build()