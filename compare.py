"""
    Compare two business names.
"""

import fio
import Levenshtein
from support    import *
from   settings import *

# LOAD CONFIG FILES ----------------------------------------------------------------------------------------------------

if PATH_CONFIG_FILES: assert str(PATH_CONFIG_FILES).endswith('/')

if not os.path.exists(PATH_CONFIG_FILES + F_BRANDNAMES):    log_warn(PATH_CONFIG_FILES + F_BRANDNAMES + ' does not exit.')
if not os.path.exists(PATH_CONFIG_FILES + F_CORPSUFFIXES):  log_warn(PATH_CONFIG_FILES + F_CORPSUFFIXES + ' does not exit.')
if not os.path.exists(PATH_CONFIG_FILES + F_RENAME):        log_warn(PATH_CONFIG_FILES + F_RENAME + ' does not exit.')
if not os.path.exists(PATH_CONFIG_FILES + F_REPLACE):       log_warn(PATH_CONFIG_FILES + F_REPLACE + ' does not exit.')
if not os.path.exists(PATH_CONFIG_FILES + F_SKIP):          log_warn(PATH_CONFIG_FILES + F_SKIP + ' does not exit.')
if not os.path.exists(PATH_CONFIG_FILES + F_STEM):          log_warn(PATH_CONFIG_FILES + F_STEM + ' does not exit.')

BRANDNAMES  = fio.load_set(PATH_CONFIG_FILES + F_BRANDNAMES,   default_no_file=True, freeze=True)
CORPSUFFIX  = fio.load_set(PATH_CONFIG_FILES + F_CORPSUFFIXES, default_no_file=True)
RENAMES     = fio.load_csv(PATH_CONFIG_FILES + F_RENAME,       default_no_file=True)
REPLACE     = fio.load_csv(PATH_CONFIG_FILES + F_REPLACE,      default_no_file=True)
SKIP        = fio.load_set(PATH_CONFIG_FILES + F_SKIP,         default_no_file=True, freeze=True)
STEM        = fio.load_set(PATH_CONFIG_FILES + F_STEM,         default_no_file=True, freeze=True)


# MAIN COMPARISON FUNCTION ---------------------------------------------------------------------------------------------

def compare_biznames(bizname1, bizname2, fuzzy_diff=0, fuzzy_ratio=0.9, debug=False):
    """
        Compare two business names

        Args:
                bizname1:               first business name
                bizname2:               second business name
                fuzzy_diff:             when doing a fuzzy match, max allowed difference in length of names
                fuzzy_ratio:            when doing a fuzzy match, max levenstein difference ratio allowed between names
                debug:                  print out debugging info if comparison isn't working as expected
    """

    f1_clean = clean_name(bizname1)
    if debug: print(bizname1, f1_clean)

    f2_clean = clean_name(bizname2)
    if debug: print(bizname2, f2_clean)

    # disallow if no strings
    if not f1_clean or not f2_clean: return False

    # always require at least the same first character in the name to be the same
    if f1_clean[0] != f2_clean[0]:
        if debug: print('Failed first char test')
        return False

    # check diff in string lengths
    len_diff = abs(len(f1_clean) - len(f2_clean))
    if len_diff > fuzzy_diff:
        if debug: print('Failed first char test', 'len_diff', len_diff)
        return False

    # check num of different unique chars
    f_chars = {c for c in f1_clean}
    a_chars = {c for c in f2_clean}
    common = f_chars.intersection(a_chars)
    n_diff = abs(max(len(f_chars), len(a_chars)) - len(common))
    if debug: print('n_diff', n_diff)

    if n_diff <= fuzzy_diff:

        # calc dist now (late) to save runtime
        dist = calc_distance(f1_clean, f2_clean)

        # EXACT MATCH
        if dist == 0:
            return True

        # GOOD ENOUGH MATCH?
        else:

            # calc % of name that is similar
            ratio = 1 - (float(dist) /
                         min(len(f1_clean), len(f2_clean)))

            if debug: print('ratio', ratio)

            # CANDIDATE
            if ratio > fuzzy_ratio:
                return True

    return False

# CLEANING FUNCTIONS ---------------------------------------------------------------------------------------------------

def clean_name(name, rename_dct=None):

    # fast exit
    if not name: return ''

    # single spacing and lower
    name = ' '.join(name.split()).lower()
    if not name: return ''

    # skips
    if name in SKIP: return ''

    # replacements (pass # 1)
    for (old, new) in REPLACE:
        old = " " + old + " "
        new = " " + new + " "
        name = str(" " + name + " ")
        name = name.replace(old, new)
    name = name.strip()
    if name in SKIP: return ''
    if not name: return ''

    # punctuation
    name = remove_punct(name)
    if name in SKIP: return ''
    if not name: return ''

    # brandnames  (1st try)
    name = get_brandname(name)
    if name in SKIP: return ''
    if not name: return ''

    # stem
    terms = name.split()
    for i in range(len(terms)):
        term = terms[i]
        for stem in STEM:
            if term.startswith(stem):
                terms[i] = stem

    name = ' '.join(terms)
    if name in SKIP: return ''
    if not name: return ''

    # suffixes
    terms = name.split()
    for _ in range(4):
        if terms:
            if terms[-1] in CORPSUFFIX:
                terms = terms[:-1]
    if not terms: return ''
    name = ' '.join(terms)
    if name in SKIP: return ''
    if not name: return ''

    # synonyms (pass # 2)
    for (old, new) in REPLACE:
        old = " " + old + " "
        new = " " + new + " "
        name = str(" " + name + " ")
        name = name.replace(old, new)
    name = name.strip()
    if name in SKIP: return ''
    if not name: return ''

    # brandnames (2nd try)
    name = get_brandname(name)
    if name in SKIP: return ''
    if not name: return ''

    # SPECIAL CASES
    if name == "none":     return ''
    if name in STEM:      return ''
    if name[:4] == "the ": name = name[4:]

    # final cleaning to remove any extra spaces that might have arisen
    name = ' '.join(name.split())

    # rename company if this appears in the renaming dict
    if rename_dct and name in rename_dct: name = rename_dct[name]

    # RETURN
    return name

def get_brandname(name):
    s = " " + name + " "
    for brand in BRANDNAMES:
        if s.find(" " + brand + " ") >= 0:
            return brand
    return name

def remove_punct(s):

    # Change to a SPACE
    for char in ["_", "-", "(", ")", "{", "}", "[", "]", "<", ">", "|", "\\",
                 ",", ":", ";", "~", '"', "/", "&"]:
        s = s.replace(char, ' ')

    # Remove
    for char in ["!", "@", "#", "$", "%", "^", "*", "+", "=", "`", "'", ".", "?"]:
        s = s.replace(char,"")

    # Compress Spacing
    s = ' '.join(s.split())

    return s

def calc_distance(name1, name2):

    assert name1, 'No name1'
    assert name2, 'No name2'

    # exact match
    if name1 == name2:
        return 0

    # calc levenshtein
    else:
        return Levenshtein.distance(name1, name2)

def is_number(s):
    try:    float(s)
    except: return False
    else:   return True
