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
    name: python38564bitnlpconda558de9a36abb4155bca9bf25b4c81369
---

```python
import pandas as pd
from pathlib import Path
```

```python
Path.cwd()
```

```python
data_source = Path('../../../Cornish_NLP_Proposal/nlp_data/NLP - pros blad - deid - 2020-07-29.xlsx')
```

```python
sheets = pd.read_excel(data_source, sheet_name=None)
```

```python
sheets.keys()
```

```python
copath = sheets['CoPath_363cases']
cortex = sheets['Cortex_10227cases']
```

```python
copath
```

```python
cortex
```

```python
?pd.read_excel
```

```python

```
