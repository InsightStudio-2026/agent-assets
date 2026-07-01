"""演示 ```text 闭合围栏 bug 导致标题消失的渲染差异。
纯正则实现，无外部依赖，可自证修复有效性。
"""
import re

# 模拟 bug 版本（database.instructions.md 修复前）
BEFORE = """## 3. 单层手动重跑（FAIL 时定位）

```powershell
$py = ".\\backend\\venv\\Scripts\\python.exe"
& $py scripts/run_migrations.py --verify
```text

## 4. Baseline 刷新（仅当 drift 合法变窄时）

```powershell
$py = ".\\backend\\venv\\Scripts\\python.exe"
& $py scripts/check_schema_drift.py --target postgres --write-baseline
```text

## 5. Schema 变更 SOP（强制顺序）
"""

# 模拟修复版本
AFTER = BEFORE.replace('```text', '```')

def extract_headings(md_text, _label):
    """从 Markdown 中提取 ## 标题，模拟渲染器行为。
    关键：闭合围栏带语言标识会导致后续标题被"吞入"代码块。
    简化模拟：统计 ``` 配对——若闭合围栏非纯 ```，配对失败，
    后续内容全被视为代码块内部，标题被吞。
    """
    lines = md_text.split('\n')
    headings = []
    in_fence = False
    fence_errors = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # 检查围栏行
        fence_match = re.match(r'^(`{3,})(\S*)\s*$', stripped)
        if fence_match:
            _ = fence_match.group(1)
            lang = fence_match.group(2) if fence_match.group(2) else None
            if not in_fence:
                # 开围栏
                in_fence = True
            else:
                # 闭合围栏检测：lang 非空 → 非法闭合（被视为新开代码块）
                if lang:
                    fence_errors.append(
                        f"Line {i+1}: 闭合围栏带语言标识 '{lang}'——"
                        f"渲染器将其视为新代码块开头，后续内容全部被吞！"
                    )
                    # in_fence 保持 True（"新代码块"持续）
                else:
                    in_fence = False
            continue

        # 检测标题（仅当不在代码块内）
        if not in_fence:
            h2_match = re.match(r'^##\s+(.+)', stripped)
            if h2_match:
                headings.append((i+1, h2_match.group(1)))

    return headings, fence_errors

print("=" * 60)
print("【修复前】闭合围栏 ```text —— 标题被吞")
print("=" * 60)
headings_before, errors_before = extract_headings(BEFORE, "before")
for err in errors_before:
    print(f"  ❌ {err}")
print(f"\n  检测到的 ## 标题: {len(headings_before)} 个")
for ln, h in headings_before:
    print(f"    L{ln}: {h}")
if len(headings_before) < 3:
    print(f"  ⚠️ 应有 3 个标题 (## 3 / ## 4 / ## 5)，实际只检测到 {len(headings_before)} 个！")

print()
print("=" * 60)
print("【修复后】闭合围栏 ``` —— 标题正常")
print("=" * 60)
headings_after, errors_after = extract_headings(AFTER, "after")
for err in errors_after:
    print(f"  ❌ {err}")
print(f"\n  检测到的 ## 标题: {len(headings_after)} 个")
for ln, h in headings_after:
    print(f"    L{ln}: {h}")
if len(headings_after) == 3:
    print("  ✅ 3 个标题全部正确识别！")

print()
print("=" * 60)
print("结论：```text 作为闭合围栏会导致后续所有标题消失。")
print("修复为 ``` (纯反引号) 后标题恢复正常渲染。")
print("=" * 60)
