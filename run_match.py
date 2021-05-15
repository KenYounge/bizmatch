"""
    Run a complete match (in one batch) of business names between two lists.

    MUST be run from the Command Line - not meant for importing!

    Args:
        argv[1] = file name of focal list
        argv[2] = file name of alter list
        argv[3] = number of batches        (optional)
        argv[4] = index of batch to run    (optional)

"""

assert __name__ == "__main__", 'You must run this program from the command line.'

from   sys import argv
import match

fname_focal = str(argv[1])
fname_alter = str(argv[2])

if len(argv) > 3:
    num_batches = int(argv[3])
    batch_no    = int(argv[4])
else:
    num_batches = 1
    batch_no    = 0

match.match_lists(fname_focal, fname_alter, num_batches, batch_no)

