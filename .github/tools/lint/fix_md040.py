"""修复 MD040：为未标注语言的围栏代码块添加 `text` 语言标识。

安全措施：仅在 OPENING fence（不在代码块内）时才添加语言标记。

用法：
    python fix_md040.py [目录路径]
    python fix_md040.py                          # 扫描仓库根目录
    python fix_md040.py docs/specs/              # 扫描指定目录
"""

import re
import sys
from pathlib import Path


def fix_untagged_fences(text: str) -> tuple[str, int]:
    """将未标注语言的 OPENING 围栏代码块添加 text 标识。

    状态机规则：
    - 纯 ``` / ~~~ + 不在块内 → 开围栏，补 text
    - 纯 ``` / ~~~ + 在块内   → 闭围栏，原样保留
    - 带语言 ```xxx / ~~~xxx + 不在块内 → 开围栏，原样保留
    - 带语言 ```xxx / ~~~xxx + 在块内   → 修复为纯闭围栏（闭合围栏带语言标识是破坏性缺陷）
    """
    lines = text.split("\n")
    result = []
    changed = 0
    in_code_block = False

    for line in lines:
        stripped = line.strip()

        # 纯反引号围栏（无语言标识）
        if re.fullmatch(r"```\s*", stripped) or re.fullmatch(r"~~~\s*", stripped):
            if not in_code_block:
                result.append("```text")
                in_code_block = True
                changed += 1
            else:
                result.append(line)
                in_code_block = False
        # 带语言标识的围栏
        elif re.fullmatch(r"```\w.*", stripped) or re.fullmatch(r"~~~\w.*", stripped):
            if not in_code_block:
                result.append(line)
                in_code_block = True
            else:
                # 闭合围栏带语言标识 → 修复为纯反引号
                result.append("```")
                in_code_block = False
                changed += 1
        else:
            result.append(line)

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

        fixed, changed = fix_untagged_fences(orig)
        if changed > 0:
            fp.write_text(fixed, encoding="utf-8")
            rel = fp.relative_to(root) if fp.is_relative_to(root) else fp
            print(f"  FIXED {rel}: {changed} 块")
            total += changed
            files_fixed += 1

    print(f"\n总计: {files_fixed} 文件, {total} 块修复")


if __name__ == "__main__":
    main()
