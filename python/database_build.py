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
cdf = cdf.drop_duplicates()

cdf[['concept', 'data_type']].to_sql('concept', con=conn, index=False, if_exists='append')

table_df = pd.read_sql_query('select * from concept',conn)

# need to find concept_id of parent concept and update appropriate rows

for row in cdf[cdf.parent.notna()]:
    if pd.isna(row.parent):
        print(row.concept)
    else:
        # need to find id of parent
        print(row.parent)

