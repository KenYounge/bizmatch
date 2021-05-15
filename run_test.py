"""
    BizNames: Test if running
"""

import match
import compare
from   datetime  import datetime
from   support   import *

DEBUG = False

def test1():
    banner('TEST: Compare two names', blue=True)
    name1 = 'ALBANY MOLECULAR RESEARCH INC'
    name2 = 'ALBANY MOLECULAR RESRCH INC'
    result = compare.compare_biznames(name1, name2, debug=DEBUG)
    print('Test if: ', name1,  ' == ', name2)
    print(result)

def test2():
    banner('TEST: Compare two names', blue=True)
    name1 = 'ALBANY MOLECULAR RESEARCH INC'
    name2 = 'ALBANY MOLECULAR RH INC'
    result = compare.compare_biznames(name1, name2, debug=DEBUG)
    print('Test if: ', name1,  ' == ', name2)
    print(result)

def test3():
    banner('TEST: Compare two names and date', blue=True)
    name1  = 'ALBANY MOLECULAR RESEARCH INC'
    name2  = 'ALBANY MOLECULAR RESRCH INC'
    date1  = datetime.strptime('1999-12-31', '%Y-%M-%d')
    date2  = datetime.strptime('1999-12-31', '%Y-%M-%d')
    clean1 = compare.clean_name(name1)
    clean2 = compare.clean_name(name2)
    matched, candidates = match._match_names(clean1, name1, date1, clean2, name2, date2)
    if matched: print('MATCH FOUND:', matched[0], ' == ', matched[1])
    if candidates: print('CANDIDATE MATCH FOUND:', candidates[0], candidates[1])

def test4():
    banner('TEST: Match a name to entire alter list', blue=True)

    rename_dct = match._load_rename_dict()
    a_lst      = match._load_bizname_list('_sdc_biznames.csv', rename_dct)

    name1  = 'Hola Home Furnishings'
    clean1 = match.clean_name(name1, rename_dct)
    date1  = None

    print('Matching names...')
    matched, candidates = match._match_alters(clean1, name1, date1, a_lst, rename_dct)
    if matched:
        for focal, alter in matched:
            print('MATCH FOUND:', focal, ' == ', alter)
    else: print('No Matches')

    if candidates:
        for focal, alter in candidates:
            print('CANDIDATE MATCH FOUND:', focal, ' == ', alter)

if __name__ == "__main__":
    print()
    test1()
    test2()
    test3()
    test4()
    print()
    print()

