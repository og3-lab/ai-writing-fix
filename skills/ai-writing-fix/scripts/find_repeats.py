"""文章の中で、言い回しの重なりが大きい文の組を書き出す。

使い方: python find_repeats.py 原稿.md [しきい値(既定 0.35)]
同じことを2回書いている候補を、重なりの大きい順に並べる。消すかどうかは書き手が決める。
"""
import re
import sys


def sentences(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    out = []
    for para_no, para in enumerate(re.split(r"\n\s*\n", text), 1):
        for s in re.split(r"(?<=[。！？!?])|\n", para):
            if s.lstrip().startswith("#"):
                continue  # 見出しは本文の要約なので比べない
            s = re.sub(r"^[>\-\*\s・|]+", "", s).strip()
            if len(s) >= 12:
                out.append((para_no, s))
    return out


def grams(s, n=3):
    s = re.sub(r"[、。「」『』（）()\s・,.:：|]", "", s)
    return {s[i:i + n] for i in range(len(s) - n + 1)}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    path = sys.argv[1]
    th = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
    with open(path, encoding="utf-8") as f:
        ss = sentences(f.read())
    gs = [grams(s) for _, s in ss]
    pairs = []
    for i in range(len(ss)):
        for j in range(i + 1, len(ss)):
            a, b = gs[i], gs[j]
            if not a or not b:
                continue
            score = len(a & b) / min(len(a), len(b))
            if score >= th:
                pairs.append((score, i, j))
    pairs.sort(reverse=True)
    if not pairs:
        print("重なりの大きい文の組は見つかりませんでした。")
        return
    for score, i, j in pairs:
        print(f"[重なり {score:.2f}] 段落{ss[i][0]}「{ss[i][1]}」")
        print(f"            段落{ss[j][0]}「{ss[j][1]}」")


if __name__ == "__main__":
    main()
