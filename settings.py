"""
    Project Settings
"""

from os import path

CANDID_DIFF        = 3                  # max allowed diff in strings for candidates
CANDID_THRESHOLD   = 0.71               # min ratio between strings for candidates
ALLOW_ONE_2_MANY   = True

ALLOW_DAYS_BEFORE  = 5                  # OK for ALTER to be this # days before focal
ALLOW_DAYS_AFTER   = 5                  # OK for ALTER to be this # days after focal
DATE_FORMAT        = '%Y-%M-%d'         # formatted for US date order

PATH_CONFIG_FILES  = path.dirname(path.realpath(__file__)) + '/'  # Points to installation path from PIP, but you can over-ride to some other project directory

F_BRANDNAMES       = '+brands.txt'
F_CORPSUFFIXES     = '+corp.txt'
F_RENAME           = '+rename.csv'
F_REPLACE          = '+replace.csv'
F_SKIP             = '+skip.txt'
F_STEM             = '+stem.txt'

F_MATCHED          = '~matched.csv'     # Output - matched business names
F_CANDIDATES       = '~candidates.csv'  # Output - candidate names to consider for matching


