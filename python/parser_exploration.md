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
get_sections_pat = re.compile(r'^([A-Z0-9])([:\)])([\S\s]+?(?=^[\n]|^[A-Z]:|\Z))', flags=re.M)
get_subsections_pat = re.compile(r'(^[^\n:]+):[ \t]*([\s\S]*?(?=(?:^[^\n:]*:)|\Z))', flags=re.M)

def get_sections(instr):
    return {m.group(1).strip() : m.group(3).strip() for m in get_sections_pat.finditer(instr)}

def get_subsections(instr):
    return {re.sub('^\W*\s*', '', m.group(1).strip()) : m.group(2).strip()
            for m in get_subsections_pat.finditer(instr)}
```

```python
parts = get_sections(table_df.parts[0])
parts
```

```python
finaldiagnosis = get_sections(table_df.finaldiagnosis[0])
finaldiagnosis
```

```python
subsection = get_subsections(finaldiagnosis['E'])
subsection
```

```python
subsection.keys()
```

```python
subsection['URINARY BLADDER']
```

```python
table_df.microscopicdescription[0]
```

```python
md = get_subsections(table_df.microscopicdescription[0])
md
```

```python
md.keys()
```

```python
# do any of the keys match concepts?
q = "select * from concept"
concept_df = pd.read_sql_query(q,conn)
concept_df
```

```python
len(md)
```

```python
# if value is empty string, then this is a section?
matched_concepts = None
mmatch_concepts = None
unmatched = {}
concept_values = None

for key, value in md.items():
    key_df = concept_df[concept_df.concept == key].copy()
    if len(key_df) == 1:
        if matched_concepts is None:
            matched_concepts = key_df
        else:
            matched_concepts = matched_concepts.append(key_df)
    elif len(key_df) > 1:
        # add to multiple matches
        if mmatch_concepts is None:
            mmatch_concepts = key_df
        else:
            mmatch_concepts = mmatch_concepts.append(key_df)
    else:
        print('No match for key:', key)
        unmatched[key] = value
    
    value_df = concept_df[concept_df.concept == value]
    if len(value_df) == 1:
        if matched_concepts is None:
            matched_concepts = value_df
        else:
            matched_concepts = matched_concepts.append(value_df)
    elif len(value_df) > 1:
        # multiple matches for values usually means need to use key to find correct concept.
        # add to multiple matches
        if mmatch_concepts is None:
            mmatch_concepts = value_df
        else:
            mmatch_concepts = mmatch_concepts.append(value_df)
    else:
        # if key has match but value does not have a match, then value should be stored as the concept value (eg '4 mm' and the like)
        if len(key_df) == 1 and value != '':
            key_df['concept_value'] = value
            if concept_values is None:
                concept_values = key_df
            else:
                concept_values = concept_values.append(key_df)
        else:
            print('No match for value:', value)
            unmatched[key] = value
matched_concepts.drop_duplicates(inplace=True)
mmatch_concepts.drop_duplicates(inplace=True)
```

```python
print(len(matched_concepts))
matched_concepts
```

```python
mmatch_concepts
```

```python
unmatched
```

```python
concept_values
```

```python

```
