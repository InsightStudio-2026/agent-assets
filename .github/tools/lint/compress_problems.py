"""压缩 VS Code Problems JSON —— 去重、合行、删噪。

将 markdownlint 列级错误合并为行级条目，按 (file, code) 分组。
输出紧凑 JSON，保留定位与修复所需的最小信息。

用法：
    python compress_problems.py <输入.json> [输出.json]
    默认输出: 问题_压缩.json
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def norm_code(entry: dict) -> str:
    """归一化 code：markdownlint 用嵌套对象 {value, target}，提取 value"""
    code = entry.get("code", "")
    if isinstance(code, dict):
        return code.get("value", str(code))
    return str(code)


def norm_resource(entry: dict) -> str:
    """统一资源路径格式，去掉 /c:/ 前缀中多余的斜杠"""
    return entry.get("resource", "").lstrip("/")


def compress(input_path: Path, output_path: Path) -> dict:
    """执行压缩，返回统计字典"""
    with open(input_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    total_in = len(raw)

    # 步骤 1: 归一化 + 去噪
    cleaned = []
    for e in raw:
        cleaned.append({
            "resource": norm_resource(e),
            "code": norm_code(e),
            "message": e.get("message", ""),
            "line": e.get("startLineNumber", 0),
        })

    # 步骤 2: 精确去重
    seen = set()
    deduped = []
    for e in cleaned:
        key = (e["resource"], e["code"], e["message"], e["line"])
        if key not in seen:
            seen.add(key)
            deduped.append(e)

    # 步骤 3: 按 (resource, code) 分组
    groups: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for e in deduped:
        groups[(e["resource"], e["code"])].append(e)

    # 步骤 4: 合并输出
    output = []
    for (resource, code), items in sorted(groups.items()):
        items.sort(key=lambda x: x["line"])
        lines = sorted(set(it["line"] for it in items))
        msg_sample = items[0]["message"]
        output.append({
            "file": resource,
            "code": code,
            "message": msg_sample,
            "lines": lines,
            "count": len(lines),
        })

    # 步骤 5: 统计
    by_rule: dict[str, int] = defaultdict(int)
    for o in output:
        by_rule[o["code"]] += o["count"]

    # 写入
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    return {
        "total_in": total_in,
        "deduped": len(deduped),
        "merged": len(output),
        "by_rule": dict(sorted(by_rule.items(), key=lambda x: -x[1])),
    }


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python compress_problems.py <输入.json> [输出.json]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("问题_压缩.json")

    if not input_path.exists():
        print(f"错误: 文件不存在 {input_path}")
        sys.exit(1)

    stats = compress(input_path, output_path)

    orig_kb = input_path.stat().st_size / 1024
    out_kb = output_path.stat().st_size / 1024
    ratio = orig_kb / out_kb if out_kb > 0 else 0

    print(f"输入条目: {stats['total_in']}")
    print(f"去重后:   {stats['deduped']} (去除 {stats['total_in'] - stats['deduped']} 条)")
    print(f"合并后:   {stats['merged']} 条目")
    print(f"原始: {orig_kb:.0f} KB → 压缩: {out_kb:.1f} KB (压缩比 {ratio:.1f}:1)")

    print("\n规则分布 (Top 10):")
    for code, cnt in list(stats["by_rule"].items())[:10]:
        print(f"  {code}: {cnt}")

    print(f"\n写入 {output_path}")


if __name__ == "__main__":
    main()
