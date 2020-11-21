---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.5.2
  kernelspec:
    display_name: Python [conda env:nlp]
    language: python
    name: conda-env-nlp-py
---

```python
import sqlite3
import pandas as pd
from pathlib import Path
import re
import pnlp_functions as pnlp
```

```python
df = pd.read_sql_query('''
        select s.*, c.concept from structured_report s
        left join concept c
        on s.concept_id = c.concept_id''', pnlp.conn)
```

```python
df
```

```python
histogram_column = 'concept_id'
pd.concat([df[histogram_column].value_counts().rename('n'),
                 df[histogram_column].value_counts(normalize=True).rename('pct')], axis=1)
```

```python
tmp = df[histogram_column].value_counts()
```

```python
pnlp.concept_df[pnlp.concept_df.parent_id.isin(tmp.index[0:9])]
```

```python
df[(df.concept_id.isin(tmp.index[0:9])) & (df.concept_value.notna())]
```

```python
df[df.concept_id.isin(pnlp.concept_df[pnlp.concept_df.parent_id == 18].concept_id)]
```

```python
df[df.concept_id.isin(pnlp.concept_df[pnlp.concept_df.parent_id == 114].concept_id)]
```

```python

```
