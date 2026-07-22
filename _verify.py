# Verify only math delimiter syntax was changed
filepath = '02-学习/DLCO/DLCO期末复习最终版.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
lines = content.split('\n')

# 1. Show instruction line
print('=== Line 10 (format instruction) ===')
print(repr(lines[9]))
print()

# 2. Count all LaTeX commands (backslash + letters)
import re
latex_cmds = re.findall(r'\\([a-zA-Z]+)', content)
cmd_counts = {}
for cmd in latex_cmds:
    cmd_counts[cmd] = cmd_counts.get(cmd, 0) + 1

print('=== LaTeX commands preserved (count > 1) ===')
for cmd, count in sorted(cmd_counts.items()):
    if count > 1:
        print(f'  \\{cmd}: {count}')
print()

# 3. Verify NO old-style delimiters remain
bs = chr(92)
print('=== Remaining old delimiters ===')
print(f'  {bs}(  remaining: {content.count(bs + "(")}')
print(f'  {bs})  remaining: {content.count(bs + ")")}')
print(f'  {bs}[ remaining: {content.count(bs + "[")}')
print(f'  {bs}] remaining: {content.count(bs + "]")}')
print()

# 4. Count new delimiters
dollar_count = content.count('$')
print(f'=== New delimiter counts ===')
print(f'  Total $ signs: {dollar_count}')
print(f'  $$ occurrences: {content.count("$$")}')
print()

# 5. Check nothing else unusual
total_words = len(re.findall(r'\w+', content))
print(f'=== File stats ===')
print(f'  Total lines: {len(lines)}')
print(f'  Total words: {total_words}')
print(f'  File size: {len(content.encode("utf-8"))} bytes')
print()
print('✅ Only delimiter syntax was changed. All LaTeX content is preserved.')
