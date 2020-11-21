import pandas as pd
import re
import sqlite3
from pathlib import Path
import re

pd.options.display.max_colwidth = 100
pd.set_option('display.width', 160)

data_path = Path('../../nlp_data')
sql_path = Path('../sql')

conn = None
try:
    conn = sqlite3.connect(Path(data_path / 'synoptic_reports.db'))
    cur = conn.cursor()
except Exception as e:
    print('Exception encountered when opening database:', e)

q = "select * from concept"
concept_df = pd.read_sql_query(q,conn)
concept_df.parent_id = concept_df.parent_id.astype("Int64")

# create some transformed columns for matching
concept_df['concept_lower'] = concept_df.concept.str.lower()
concept_df['concept_no_spec_char'] = concept_df.concept_lower.str.replace(r'[-()]', '')
concept_df['concept_no_paren'] = concept_df.concept_lower.str.replace(r'\([^)]*\)', '').str.strip()

# pattern mostly from https://stackoverflow.com/a/62642318
# original 
# pat=re.compile(r'(^[^\n:]+):[ \t]*([\s\S]*?(?=(?:^[^\n:]*:)|\Z))', flags=re.M)
get_sections_pat = re.compile(r'^([A-Z0-9])([:\)])([\S\s]+?(?=^[\n]|^[A-Z]:|\Z))', flags=re.M)
get_subsections_pat = re.compile(r'(^[^\n:]+):[ \t]*([\s\S]*?(?=(?:^[^\n:]*:)|\Z))', flags=re.M)

def get_sections(instr):
    return {m.group(1).strip() : m.group(3).strip() for m in get_sections_pat.finditer(instr)}

def get_subsections(instr):
    newdict = {re.sub('^\W*\s*', '', m.group(1).strip()) : m.group(2).strip()
            for m in get_subsections_pat.finditer(instr)}
    # some times 'section' heading like phrases are lumped with a value, split these out.
    extradict = {}
    for key, value in newdict.items():
        if ('\n' in value):
            extradict[key] = value.split('\n')[0]
            for v in value.split('\n')[1:]:
                extradict[v] = ''
    # combine dictionaries
    return {**newdict, **extradict}

def find_match(search_term):
    st_lower = search_term.lower()
    st_no_spec_char = re.sub('[-()]', '', st_lower)
    st_no_paren = re.sub('\([^)]*\)', '', st_lower).strip()
    
    df = concept_df[(concept_df.concept == search_term) |
                    (concept_df.concept_lower == st_lower) |
                    (concept_df.concept_no_spec_char == st_no_spec_char) |
                    (concept_df.concept_no_paren == st_no_paren)
              ].copy()
    return df

def match_concepts(in_dict, debug=True):
    empty_df = pd.DataFrame(columns=['concept_id',
                                     'concept',
                                     'data_type',
                                     'parent_id'])
    matched_concepts = empty_df.copy()
    mmatch_concepts = empty_df.copy()
    unmatched = {}
    concept_values = empty_df.copy()

    for key, value in in_dict.items():
        key_df = find_match(key)
        if len(key_df) == 1:
            matched_concepts = matched_concepts.append(key_df)
        elif len(key_df) > 1:
            # add to multiple matches
            mmatch_concepts = mmatch_concepts.append(key_df)
        else:
            if debug: print('No match for key:', key)
            unmatched[key] = value

        value_df = find_match(value)
        if len(value_df) == 1:
            matched_concepts = matched_concepts.append(value_df)
        elif len(value_df) > 1:
            # multiple matches for values usually means need to use key to find correct concept.
            # add to multiple matches
            if (len(key_df) == 1):
                new_match = value_df[value_df.parent_id == key_df.concept_id.values[0]]
                if len(new_match) == 1:
                    matched_concepts = matched_concepts.append(new_match)
                else:
                     mmatch_concepts = mmatch_concepts.append(value_df)
            else:
                if debug:
                    print('--------- multiple potential matches found -------------')
                    print(value_df)
                    print('key_df:')
                    print(key_df)
                    print('--------------------------------------------------------')
                mmatch_concepts = mmatch_concepts.append(value_df)
        else:
            # if key has match but value does not have a match, then value should be stored as the concept value (eg '4 mm' and the like)
            if len(key_df) == 1 and value != '':
                key_df['concept_value'] = value
                concept_values = concept_values.append(key_df)
            else:
                if debug: print('No match for value:', value)
                unmatched[key] = value
    matched_concepts.drop_duplicates(inplace=True)
    mmatch_concepts.drop_duplicates(inplace=True)
    return {'matched': matched_concepts,
            'multi_matched': mmatch_concepts,
            'unmatched': unmatched,
            'matched_values': concept_values}