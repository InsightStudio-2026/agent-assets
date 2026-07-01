"""修复表格首尾空列：将 |  | col | col |  | 规范化为 | col | col |。

安全措施：
- 仅在非代码块内的行修复
- 仅处理以 | 开头和结尾的行
- 只有当首尾 cell 都是纯空白（或空）时才移除
- 同一表格内所有行必须一致处理
"""

import sys
from pathlib import Path


def strip_table_edge_empties(text: str) -> tuple[str, int]:
    """移除表格行首尾的空白列。返回 (fixed_text, changed_count)。"""
    lines = text.split("\n")
    result = []
    in_code_block = False
    changed = 0

    # 先收集所有表格行组（连续的行组）
    i = 0
    n = len(lines)

    # 标记每行是否为表格行以及其表组ID
    table_group = [-1] * n  # -1 = not a table row, >=0 = table group index
    group_id = 0

    while i < n:
        stripped = lines[i].strip()
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            i += 1
            continue

        if in_code_block:
            i += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            # 找到表格行组的起始
            start = i
            while i < n:
                s = lines[i].strip()
                # 检查是否遇到代码块
                if s.startswith("```"):
                    break
                if s.startswith("|") and s.endswith("|"):
                    i += 1
                else:
                    break
            # 标记这一组
            for j in range(start, i):
                table_group[j] = group_id
            group_id += 1
        else:
            i += 1

    # 现在处理每个表格组
    group_rows = {}
    for idx, gid in enumerate(table_group):
        if gid >= 0:
            group_rows.setdefault(gid, []).append(idx)

    should_strip = {}  # group_id -> bool

    for gid, row_indices in group_rows.items():
        # 检查该组的所有行是否首尾都是空白列
        all_have_empty_edges = True
        for idx in row_indices:
            line = lines[idx]
            cells = line.split("|")
            if len(cells) < 4:  # 至少需要 '|', cell, cell, '|' → 4 parts
                all_have_empty_edges = False
                break
            # cells[0] 始终是 ''（| 前的内容），cells[-1] 始终是 ''（| 后的内容）
            # 我们需要检查 cells[1]（第一个 content cell）和 cells[-2]（最后一个 content cell）
            first = cells[1].strip()
            last = cells[-2].strip()
            if first != "" or last != "":
                all_have_empty_edges = False
                break
        should_strip[gid] = all_have_empty_edges

    # 重新遍历并修复
    in_code_block = False
    for idx, line in enumerate(lines):
        stripped = line.strip()

        # 追踪代码块
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            continue

        if in_code_block:
            result.append(line)
            continue

        gid = table_group[idx]
        if gid >= 0 and should_strip.get(gid, False):
            indent = line[: len(line) - len(line.lstrip())]
            cells = line.split("|")
            # 移除 cells[1] 和 cells[-2]（首尾空白列）
            inner = cells[2:-2]  # 跳过 cells[0]（空）、cells[1]（空白列）、cells[-2]（空白列）、cells[-1]（空）
            new_line = indent + "|" + "|".join(inner) + "|"
            if new_line != line:
                changed += 1
            result.append(new_line)
        else:
            result.append(line)

    return "\n".join(result), changed


def process_file(filepath: Path) -> int:
    """处理单个文件，返回修改的行数。"""
    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return 0

    fixed, changed = strip_table_edge_empties(content)
    if changed > 0:
        filepath.write_text(fixed, encoding="utf-8")

    return changed


def main():
    """命令行入口"""
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    if not root.is_dir():
        print(f"错误: 目录不存在 {root}")
        sys.exit(1)

    md_files = list(root.rglob("*.md"))
    print(f"扫描 {len(md_files)} 个 .md 文件...")

    total_files = 0
    total_changed = 0
    for fp in sorted(md_files):
        c = process_file(fp)
        if c > 0:
            print(f"  FIXED {fp.relative_to(root)}: {c} 行")
            total_files += 1
            total_changed += c

    print(f"\n总计: {total_files} 文件, {total_changed} 行修复")


if __name__ == "__main__":
    main()
