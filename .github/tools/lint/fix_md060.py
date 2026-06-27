r"""修复 MD060：表格管道两侧空格。

安全措施：
- 仅在非代码块内的行修复
- 只处理以 | 开头的表格行
- 对齐分隔行 |---| 也一并处理
- 跳过含转义管道符 \| 的行

用法：
    python fix_md060.py [目录路径]
    python fix_md060.py                          # 扫描仓库根目录
    python fix_md060.py docs/specs/              # 扫描指定目录
"""

import re
import sys
from pathlib import Path


def fix_table_pipe_spacing(text: str) -> tuple[str, int]:
    """修复表格管道两侧空格。返回 (fixed_text, changed_lines_count)"""
    lines = text.split("\n")
    result = []
    in_code_block = False
    changed = 0

    for line in lines:
        stripped = line.strip()

        # 追踪代码块边界
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        # 只处理表格行（以 | 开头，以 | 结尾）
        if not stripped.startswith("|") or not stripped.endswith("|"):
            result.append(line)
            continue

        # 跳过含转义管道符的行
        if "\\|" in stripped:
            result.append(line)
            continue

        # 提取缩进
        indent = line[: len(line) - len(line.lstrip())]

        cells = stripped.split("|")
        inner = cells[1:-1]  # cells[0] 和 cells[-1] 是空

        if not inner:
            result.append(line)
            continue

        # 判断是否为分隔行（全部由 -: 和空格组成）
        is_separator = all(
            re.fullmatch(r"[\s\-:]+", c) for c in inner if c.strip()
        )

        fixed_cells = []
        for c in inner:
            trimmed = c.strip()
            if is_separator:
                if trimmed and all(ch in "-:" for ch in trimmed):
                    # 保留对齐冒号，仅补全不足 3 个的短横线
                    has_left = trimmed.startswith(":")
                    has_right = trimmed.endswith(":")
                    dashes = trimmed.strip(":")
                    if len(dashes) < 3:
                        dashes = "---"
                    if has_left and has_right:
                        trimmed = f":{dashes}:"
                    elif has_left:
                        trimmed = f":{dashes}"
                    elif has_right:
                        trimmed = f"{dashes}:"
                    else:
                        trimmed = dashes
                fixed_cells.append(f" {trimmed} ")
            else:
                fixed_cells.append(f" {trimmed} ")

        new_line = indent + "|" + "|".join(fixed_cells) + "|"

        if new_line != line:
            changed += 1

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

        fixed, changed = fix_table_pipe_spacing(orig)
        if changed > 0:
            fp.write_text(fixed, encoding="utf-8")
            rel = fp.relative_to(root) if fp.is_relative_to(root) else fp
            print(f"  FIXED {rel}: {changed} 行")
            total += changed
            files_fixed += 1

    print(f"\n总计: {files_fixed} 文件, {total} 行修复")


if __name__ == "__main__":
    main()
