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

# Notebook for exploring Pathology dataset

### Questions for Toby:
* case_id - year case was evaluated.
* From Cortex dataset AddendAmend is empty? Yes.
* Look at bladder and prostate only. See cortex example. So for some that have other parts, for now only review prostate/bladder portion. Parse what we can from others. For synoptic reports that aren't fully parseable,  flag so pathology can manually review.
* "Construct a comprehensive database of this structured data for use by the CU community" - What data elements desired here?
  * Columns from CAP protocol such as Procedure, Weight, Size, Histologic Type, Histologic Grade, etc?
  * Synoptic report is at the case level
* Where to get previous versions of CAP protocol? Some available at https://www.cap.org/protocols-and-guidelines/cancer-reporting-tools/cancer-protocol-templates, but seems to only go back to ~2012

### Recommendations/Tips from Toby:
* Cases will have anywhere from 0, 1, or 2 synoptic reports.
* Newer stuff in COPATH will probably be easiest to parse and more consistent
* CORTEX wouldn't allow amendments.
* While earliest CAP Synoptic report recommendations were released around 1997, UCH didn't start using them until maybe 2005
* Synoptic report is at the case level; while synoptic report may not have Prostate/Bladder in the specimen section, it may cover details about Prostate/Bladder

```python
import pandas as pd
from pathlib import Path
```

```python
Path.cwd()
```

```python
data_path = Path('../../../Cornish_NLP_Proposal/nlp_data/')
```

```python
data_source = data_path / Path('NLP - pros blad - deid - 2020-07-29.xlsx')
```

```python
sheets = pd.read_excel(data_source, sheet_name=None)
```

```python
sheets.keys()
```

### A few transformations:

* Change column names to lowercase for easier typing
* Removing leading and trailing spaces

```python
copath = sheets['CoPath_363cases']
copath.columns = map(str.lower, copath.columns)
copath = copath.applymap(lambda x: x.strip() if isinstance(x, str) else x)
cortex = sheets['Cortex_10227cases']
cortex.columns = map(str.lower, cortex.columns)
cortex = cortex.applymap(lambda x: x.strip() if isinstance(x, str) else x)
```

```python
copath.to_csv(data_path / 'copath_2020-07-29.csv', index=False)
cortex.to_csv(data_path / 'cortex_2020-07-29.csv', index=False)
```

### Cell to look at updated version for comparison purposes

```python
def updated_data():
    data_source = data_path / Path('NLP - pros blad - deid - 2020-10-29.xlsx')
    sheets = pd.read_excel(data_source, sheet_name=None)
    print(sheets.keys())
    copath = sheets['CoPath_363cases']
    copath.columns = map(str.lower, copath.columns)
    copath = copath.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    cortex = sheets['Cortex_10227cases']
    cortex.columns = map(str.lower, cortex.columns)
    cortex = cortex.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    copath.to_csv(data_path / 'copath_2020-10-29.csv', index=False)
    cortex.to_csv(data_path / 'cortex_2020-10-29.csv', index=False)
updated_data()
```

### Now back to our regular scheduled program

```python
copath
```

```python
copath.parts.value_counts(dropna=False).head(10)
```

```python
copath['parts_length'] = copath['parts'].map(str).apply(len)
copath['addendumcomments_length'] = copath['addendumcomments'].map(str).apply(len)
copath['addendumdiagosis_length'] = copath['addendumdiagosis'].map(str).apply(len)
copath['diagnosticcomment_length'] = copath['diagnosticcomment'].map(str).apply(len)
copath['finaldiagnosis_length'] = copath['finaldiagnosis'].map(str).apply(len)
copath['microscopicdescription_length'] = copath['microscopicdescription'].map(str).apply(len)
```

```python
copath.hist(column=[col for col in copath.columns if '_length' in col], bins=50, figsize=(20, 4), layout=(1,6))
```

```python
for index, val in copath.iloc[0].iteritems():
    print(index, ':')
    print(val, '\n')
```

```python
cortex
```

```python
cortex.parts.value_counts(dropna=False).head(10)
# Prostate may mean resection, biopsy, or others
```

```python
cortex['parts_length'] = cortex['parts'].map(str).apply(len)
# addendamend is only null
cortex['diagnosiscomment_length'] = cortex['diagnosiscomment'].map(str).apply(len)
cortex['finaldiagnosis_length'] = cortex['finaldiagnosis'].map(str).apply(len)
cortex['microscopicdescription_length'] = cortex['microscopicdescription'].map(str).apply(len)
```

```python
cortex.hist(column=[col for col in cortex.columns if '_length' in col], bins=50, figsize=(16, 4), layout=(1,4))
```

```python
# this is an example that is not a report with a Synoptic report - discard this one
for index, val in cortex.iloc[0].iteritems():
    print(index, ':')
    print(val, '\n')
```

```python
for index, val in cortex[cortex.parts == '1: Lymph Node; 2: Lymph Node; 3: Prostate'].iloc[0].iteritems():
    print(index, ':')
    print(val, '\n')
```

```python

```
