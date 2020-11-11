---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.2
  kernelspec:
    display_name: 'Python 3.8.5 64-bit (''nlp'': conda)'
    language: python
    name: python38564bitnlpconda558de9a36abb4155bca9bf25b4c81369
---

```python
import sqlite3
import pandas as pd
from pathlib import Path
import re
```

```python
pd.options.display.max_colwidth = 100
data_path = Path('../../nlp_data')
sql_path = Path('../sql')
```

```python
try:
    conn = sqlite3.connect(Path(data_path / 'synoptic_reports.db'))
    cur = conn.cursor()
except Exception as e:
    print('Exception encountered when opening database:', e)
```

```python
q = """select * from original_report
where case_id = 'COP-2020-50'
limit 10"""
table_df = pd.read_sql_query(q,conn)
new_df = table_df.copy()
table_df
```

```python
table_df.parts
```

```python
new_df['parts'] = table_df.parts.str.split('\n')
```

```python
parts = {}
for r in new_df.parts[0]:
    m = re.match('([A-Z])[:)](.*)', r)
    if m:
        parts[re.sub(r'\W+', '', m.group(1))] = m.group(2).strip()
```

```python
parts
```

```python
table_df.finaldiagnosis[0]
```

```python
# pattern mostly from https://stackoverflow.com/a/62642318
# original 
# pat=re.compile(r'(^[^\n:]+):[ \t]*([\s\S]*?(?=(?:^[^\n:]*:)|\Z))', flags=re.M)
pat=re.compile(r'^([A-Z0-9])([:\)])([\S\s]+?(?=^[\n]|^[A-Z]:|\Z))', flags=re.M)

def get_sections(instr):
    return {m.group(1).strip() : m.group(3).strip() for m in pat.finditer(instr)}
```

```python
get_sections(table_df.parts[0])
```

```python
get_sections(table_df.finaldiagnosis[0])
```

```python

```
