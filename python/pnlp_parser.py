import sqlite3
import pandas as pd
from pathlib import Path
import re
import pnlp_functions as pnlp

pd.options.display.max_colwidth = 100
pd.set_option('display.width', 160)

q = """
    select * from original_report
    where 
        case_id like 'COP-202%'
        or case_id like 'COP-2019%'
    limit 1000
    """
table_df = pd.read_sql_query(q,pnlp.conn)

table_df

pnlp.conn.executescript('''
delete from structured_report;
delete from unmatched_concepts;
''')

for index, row in table_df.iterrows():
    print('Now parsing', row.case_id)
    if row.microscopicdescription:
        parsed = pnlp.get_subsections(row.microscopicdescription)
        ret = pnlp.match_concepts(parsed, debug = False)

        if len(ret['matched']) > 0:
            # create dataframe for storing as structured_report in db
            ret['matched']['case_id'] = row.case_id
            ret['matched']['concept_value'] = None
            todb = ret['matched'][['case_id', 'concept_id', 'concept_value']]
            # now add concepts that have associated values
            if len(ret['matched_values']) > 0:
                ret['matched_values']['case_id'] = row.case_id
                todb = todb.append(ret['matched_values'][['case_id', 'concept_id', 'concept_value']])
            # write to db
            try:
                todb.drop_duplicates().to_sql('structured_report', con=pnlp.conn, index=False, if_exists='append')
            except sqlite3.IntegrityError as e:
                print('    WARN: All or part of', row.case_id, 'has already been saved as a structured_report.')

        if len(ret['unmatched']) > 0:
            # create dataframe for storing unmatched items in db
            unmatched_concepts = [x.strip(' :') for x in [k + ': ' + v for k, v in ret['unmatched'].items()]]
            umdf = pd.DataFrame(columns = ('case_id', 'concept_candidate'))
            umdf['concept_candidate'] = unmatched_concepts
            umdf['case_id'] = row.case_id
            # write to db
            try:
                umdf.drop_duplicates().to_sql('unmatched_concepts', con=pnlp.conn, index=False, if_exists='append')
            except sqlite3.IntegrityError as e:
                print('    WARN: All or part of', row.case_id, 'has already been saved as unmatched_concepts.')
        
        if len(ret['unmatched']) == 0 and len(ret['matched']) == 0:
            print('    ', row.case_id, 'has no matching concepts')

    else:
        print('    ', row.case_id, 'has no microsopicdescription')
