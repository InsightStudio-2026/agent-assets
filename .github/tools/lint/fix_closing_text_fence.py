"""批量修复所有 .md 文件中 ```text 闭合围栏滥用。
将 ```text（无论开围栏还是闭合围栏）替换为 ```。
语义安全：text 是默认语言，去掉不影响渲染；闭合围栏去语言标识修复标题消失 bug。
"""
import os
import re

ROOT = r'c:\Hub\Projects\github\agent-assets'
SKIP_DIRS = {'.git', 'node_modules', '.trash'}

changed_files = 0
total_fixes = 0

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if not fn.endswith('.md'):
            continue
        fpath = os.path.join(dirpath, fn)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            original = f.read()

        # 将独立的 ```text 行替换为 ```
        # 注意：只替换行首的 ```text，不替换行中的内联代码
        fixed = re.sub(r'^(`{3,})text(\s*)$', r'\1\2', original, flags=re.MULTILINE)

        if fixed != original:
            with open(fpath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(fixed)
            count = original.count('\n') - fixed.count('\n')  # shouldn't change
            occurrences = len(re.findall(r'^`{3,}text\s*$', original, re.MULTILINE))
            changed_files += 1
            total_fixes += occurrences
            rel = os.path.relpath(fpath, ROOT)
            print(f'  ✓ {rel} ({occurrences}处)')

print(f'\n修复完成：{changed_files} 个文件，共 {total_fixes} 处')
