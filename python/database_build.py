import sqlite3
import pandas as pd
from pathlib import Path

data_path = Path('../../nlp_data')
sql_path = Path('../sql')
conn = None

print('Current working directory:', Path.cwd())

try:
    conn = sqlite3.connect(Path(data_path / 'synoptic_reports.db'))
except Exception as e:
    print('Exception encountered when opening database:', e)

with open(Path(sql_path / 'database_build.sql')) as sqlfile:
    conn.executescript(sqlfile.read())

q = "select * from sqlite_master where type='table'"
table_df = pd.read_sql_query(q,conn)
table_df

bladder_setup = pd.read_csv(Path(sql_path / 'bladder_concepts.csv'), low_memory=False)
bladder_setup.head()

prostate_setup = pd.read_csv(Path(sql_path / 'prostate_concepts.csv'), low_memory=False)
prostate_setup.head()

cdf = pd.concat([bladder_setup, prostate_setup])
cdf = cdf.drop_duplicates().reset_index(drop=True)
cdf['parent_id'] = pd.NA

# need to find concept_id of parent concept and update appropriate rows
for row in cdf[cdf.parent.notna()].itertuples():
    if pd.notna(row.parent):
        if len(cdf[cdf.concept == row.parent]) != 1:
            print(row.concept, '->', row.parent)
            print(cdf[cdf.concept == row.parent])
        else:
            cdf.at[row.Index, 'parent_id'] = cdf[cdf.concept == row.parent].index[0]

cdf.parent_id = cdf.parent_id.astype('Int64')
cdf = cdf.reset_index().rename(columns={'index': 'concept_id'})
cdf[['concept_id', 'concept', 'data_type', 'parent_id']].to_sql(
    'concept', con=conn, index=False, if_exists='replace')

# data looks good in table, but pandas treats parent_id column as float to to presence of NULL values
table_df = pd.read_sql_query('select * from concept',conn)
table_df.parent_id = table_df.parent_id.astype('Int64')


# Now load the report data
data_source = Path(data_path / 'NLP - pros blad - deid - 2020-07-29.xlsx')
sheets = pd.read_excel(data_source, sheet_name=None)
### A few transformations:
# Change column names to lowercase for easier typing
# Removing leading and trailing spaces
# Standardized column names
copath = sheets['CoPath_363cases']
copath.columns = map(str.lower, copath.columns)
copath = copath.applymap(lambda x: x.strip() if isinstance(x, str) else x)
cortex = sheets['Cortex_10227cases']
cortex.columns = map(str.lower, cortex.columns)
cortex.rename(columns={'diagnosiscomment': 'diagnosticcomment'}, inplace=True)
cortex = cortex.applymap(lambda x: x.strip() if isinstance(x, str) else x)

rpts = pd.concat([copath, cortex])
rpts = rpts.drop_duplicates().reset_index(drop=True)
rpts[['case_id', 'parts', 'diagnosticcomment', 'finaldiagnosis', 'microscopicdescription']].to_sql(
    'original_report', con=conn, index=False, if_exists='replace')
table_df = pd.read_sql_query('select * from original_report',conn)
table_df.head()