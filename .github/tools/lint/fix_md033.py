"""修复 MD033：将模板占位符 `<Token>` 转为行内代码 `<Token>`。

三遍策略（顺序关键）：
  遍 1：合并 `a`<tag>`b` → `a<tag>b`（占位符夹在 code span 之间）
  遍 2：包裹独立 <tag> → `<tag>`
  遍 3：后处理合并 `a``<tag>``b` → `a<tag>b`（遍 2 可能产生的碎片）

安全措施：跳过代码块内内容。

用法：
    python fix_md033.py [目录路径]
    python fix_md033.py                          # 扫描仓库根目录
    python fix_md033.py docs/specs/              # 扫描指定目录
"""

import re
import sys
from pathlib import Path

# 遍 1：合并 `text`<tag>`text` → `text<tag>text`
MERGE_SPAN_TAG_SPAN = re.compile(
    r"`([^`]*)`<([a-zA-Z][a-zA-Z0-9_@:.\-/]*)>`([^`]*)`"
)

# 遍 2：包裹独立 <tag> → `<tag>`
# 排除前导字符：反引号、单词字符、路径分隔符 /
WRAP_TAG = re.compile(
    r"(?<![`\w/])<([a-zA-Z][a-zA-Z0-9_@:.\-/]*)>(?![`\w/])"
)

# 遍 3：后处理 — 合并 `a``<T>``b` → `a<T>b`
POST_MERGE = re.compile(
    r"`([^`]*)``<([^>]*)>``([^`]*)`"
)


def fix_placeholder_tags(text: str) -> tuple[str, int]:
    """修复文本中的模板占位符。返回 (fixed_text, change_count)"""
    lines = text.split("\n")
    result = []
    changed = 0
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        new_line = line

        # 遍 1：合并 `a`<tag>`b` → `a<tag>b`
        new_line, n1 = MERGE_SPAN_TAG_SPAN.subn(r"`\1<\2>\3`", new_line)
        changed += n1

        # 遍 2：包裹独立 <tag> → `<tag>`
        new_line, n2 = WRAP_TAG.subn(r"`<\1>`", new_line)
        changed += n2

        # 遍 3：后处理合并 `a``<T>``b` → `a<T>b`
        new_line, n3 = POST_MERGE.subn(r"`\1<\2>\3`", new_line)
        changed += n3

        result.append(new_line)

    return "\n".join(result), changed


def main():
    """命令行入口"""
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"错误: 目录不存在 {root}")
        sys.exit(1)

    md_files = [f for f in root.rglob("*.md") if ".git" not in f.parts]
    print(f"扫描 {len(md_files)} 个 .md 文件...")

    total = 0
    files_fixed = 0
    for fp in md_files:
        try:
            orig = fp.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"  SKIP {fp}: {e}")
            continue

        fixed, changed = fix_placeholder_tags(orig)
        if changed > 0:
            fp.write_text(fixed, encoding="utf-8")
            rel = fp.relative_to(root) if fp.is_relative_to(root) else fp
            print(f"  FIXED {rel}: {changed} 处")
            total += changed
            files_fixed += 1

    print(f"\n总计: {files_fixed} 文件, {total} 处修复")


if __name__ == "__main__":
    main()
