"""分析压缩后的问题 JSON —— 完整性校验 + 分类统计 + 抽样。

合并了原 sample_violations.py 的抽样功能。

用法：
    python analyze_problems.py <压缩后的JSON> [--sample CODE]
    python analyze_problems.py 问题_压缩.json
    python analyze_problems.py 问题_压缩.json --sample MD033
"""

import json
import sys
from pathlib import Path


def analyze(data: list[dict]) -> dict:
    """返回分析结果字典"""
    # 完整性检查
    integrity_issues = []
    for d in data:
        if 0 in d["lines"]:
            integrity_issues.append(f"line=0: {d['file']} {d['code']}")
        if len(d["lines"]) != len(set(d["lines"])):
            integrity_issues.append(f"dup lines: {d['file']} {d['code']}")
        if len(d["lines"]) != d["count"]:
            integrity_issues.append(
                f"count mismatch: {d['file']} lines={len(d['lines'])} count={d['count']}"
            )

    # 按规则统计
    by_code: dict[str, dict] = {}
    for d in data:
        code = d["code"]
        if code not in by_code:
            by_code[code] = {"lines": 0, "entries": 0, "files": set()}
        by_code[code]["lines"] += d["count"]
        by_code[code]["entries"] += 1
        by_code[code]["files"].add(d["file"])

    # 来源分类
    md_count = sum(v["lines"] for k, v in by_code.items() if k.startswith("MD"))
    ps_count = sum(v["lines"] for k, v in by_code.items() if k.startswith("PS"))
    py_count = sum(
        v["lines"]
        for k, v in by_code.items()
        if k.startswith(("C", "W", "R", "E"))
    )

    return {
        "integrity_issues": integrity_issues,
        "by_code": by_code,
        "md_count": md_count,
        "ps_count": ps_count,
        "py_count": py_count,
    }


def sample(data: list[dict], code: str):
    """抽样显示指定规则的违规内容"""
    matches = [d for d in data if d["code"] == code]
    print(f"\n=== {code} 抽样 (共 {len(matches)} 条目) ===")
    # 按行数降序，取最严重的前 5 个文件
    worst = sorted(matches, key=lambda x: -x["count"])[:5]
    for d in worst:
        print(f"  {d['count']:>4}行  {d['file']}")
        lines_str = ", ".join(str(ln) for ln in d["lines"][:10])
        if len(d["lines"]) > 10:
            lines_str += f" ... (+{len(d['lines']) - 10})"
        print(f"         行号: {lines_str}")
        print(f"         消息: {d['message'][:100]}")
        print()


def cross_rule_files(data: list[dict]) -> list[tuple[str, set[str]]]:
    """找出违规类型最多的文件"""
    by_file: dict[str, set[str]] = {}
    for d in data:
        by_file.setdefault(d["file"], set()).add(d["code"])
    return sorted(by_file.items(), key=lambda x: -len(x[1]))


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python analyze_problems.py <压缩后的JSON> [--sample CODE]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"错误: 文件不存在 {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # --sample 模式
    if len(sys.argv) >= 4 and sys.argv[2] == "--sample":
        sample(data, sys.argv[3])
        return

    results = analyze(data)

    # 输出完整性
    print("=== 数据完整性 ===")
    if not results["integrity_issues"]:
        print("OK 无完整性问题")
    else:
        for issue in results["integrity_issues"]:
            print(f"WARN {issue}")

    # 输出全类目
    print("\n=== 全问题类目 ===")
    sorted_codes = sorted(
        results["by_code"].items(), key=lambda x: -x[1]["lines"]
    )
    for code, info in sorted_codes:
        print(
            f"  {code}: {info['lines']:>5} 行, "
            f"{info['entries']:>3} 条目, "
            f"{len(info['files']):>3} 文件"
        )

    # 来源分类
    print("\n=== 按来源分类 ===")
    print(f"  markdownlint (MD*):  {results['md_count']} 行")
    print(f"  PSScriptAnalyzer:    {results['ps_count']} 行")
    print(f"  Pylint:              {results['py_count']} 行")

    # 违规类型最多的文件
    print("\n=== 违规类型最多的文件 TOP 10 ===")
    top_files = cross_rule_files(data)[:10]
    for f, codes in top_files:
        print(f"  {len(codes):>2}类  {f}")
        print(f"      {', '.join(sorted(codes))}")


if __name__ == "__main__":
    main()
