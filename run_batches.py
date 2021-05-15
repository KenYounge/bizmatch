"""
    Batch process the matching of business names between two lists.

    MUST be run from the Command Line - not meant for importing!

    Args:
        argv[1] = file name of focal list
        argv[2] = file name of alter list
        argv[3] = number of batches

"""

assert __name__ == "__main__", 'You must run this program from the command line.'

import subprocess
import time
import fio
from   sys         import argv
from   datetime    import datetime
from   collections import OrderedDict
from   support     import *
from   settings    import *

fname_focal = str(argv[1])
fname_alter = str(argv[2])
num_batches = int(argv[3])

# Start batches running
processes = dict()
banner('MATCH FIRMS (' + ' '.join(argv) + ')', blue=True, clearfirst=True)
for batch_no in range(num_batches):
    cmd = ['python', str(argv[0]), fname_focal, fname_alter, str(num_batches), str(batch_no)]
    process = subprocess.Popen(cmd)
    processes[batch_no] = process

# Pause
time.sleep(90)
print()
start = datetime.now()


# Monitor progress
try:
    while len(processes):

        # Display current status
        print()
        banner(' Status: ' + str(len(processes))
                  + ' running     [Runtime '
                  + str(datetime.now() - start) + ']', green=True)
        for batch_no in range(num_batches):
            fname  = '~status.' + str(batch_no).rjust(3,'0')
            status = str(batch_no).rjust(3,'0') + ': ???'
            try:
                status = fio.load_str(fname)
            except IOError: pass
            if batch_no not in processes: status += ' [DONE]'
            log_info(status)
        print()

        # Sleep
        log_info('Refresh in 15 seconds...')
        time.sleep(15)

        # Remove completed processes
        for batch_no in range(num_batches):
            if batch_no in processes:
                if processes[batch_no].poll() is not None:
                    del processes[batch_no]

except (KeyboardInterrupt, SystemExit):
    print()
    log_warn('EXECUTION HALTED BY USER.')
    print()
except Exception as e:
    log_err(e)

# All batches have completed
log_warn(' Matching complete. [Runtime ' + str(datetime.now() - start) + ']')


# Consolidate results from all batches
log('Consolidating results...')
candidates = []
matched    = []
for batch_no in range(num_batches):
    for row in fio.load_csv('~candidates.' + str(batch_no).rjust(3, '0'), default_no_file=True):
        candidates.append(row)
    for row in fio.load_csv('~matched.' + str(batch_no).rjust(3, '0'), default_no_file=True):
        matched.append(row)


# Make sure they are unique ()
c = OrderedDict()
m = OrderedDict()
candidates = (tuple(entry) for entry in candidates)
matched    = (tuple(entry) for entry in matched)
for entry in candidates:
    c[entry] = None         # use orderdict trick as an ordered set
for entry in matched:
    m[entry] = None         # use orderdict trick as an ordered set
candidates = c.keys()
matched = m.keys()
fio.save_csv(sorted(candidates), F_CANDIDATES)
fio.save_csv(sorted(matched), F_MATCHED)


# Delete temp files
for batch_no in range(num_batches):
    for fbase in ['~candidates.', '~matched.', '~status.']:
        try:
            fname = fbase + str(batch_no).rjust(3,'0')
            if os.path.exists(fname):
                log('Removing ' + fname)
                os.remove(fname)
        except IOError: pass


# Report results
banner('Final results', green=True)
log_info(str(len(matched)).rjust(9) + ' matches')
log_info(str(len(candidates)).rjust(9) + ' candidates')
print()
log_info('Upload files with:  gsutil -m cp ~* gs://tislab  ')
print()


# Done
banner('DONE', blue=True)

