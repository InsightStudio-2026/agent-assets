"""诊断所有 .md 文件中 ```text 被误用为闭合围栏的情况"""
import os
import re

root = r'c:\Hub\Projects\github\agent-assets'
issues = []

for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ('.git', 'node_modules', '.trash')]
    for fn in filenames:
        if not fn.endswith('.md'):
            continue
        fpath = os.path.join(dirpath, fn)
        with open(fpath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            stripped = line.rstrip('\n\r')
            # 匹配 ```text（可能有尾随空格）作为闭合围栏：
            # 条件是上一行非空且非围栏自身
            if re.match(r'^`{3,}text\s*$', stripped):
                prev_is_blank = (i == 0) or (lines[i-1].strip() == '')
                prev_is_fence = (i > 0) and re.match(r'^`{3,}', lines[i-1].strip())
                if not prev_is_blank and not prev_is_fence:
                    issues.append(f'{fpath}:{i+1}: CLOSING ```text (前一行有内容，不是开围栏)')

if issues:
    print(f'发现 {len(issues)} 处闭合围栏滥用：')
    for iss in issues:
        print(f'  {iss}')
else:
    print('未发现闭合围栏滥用。')
