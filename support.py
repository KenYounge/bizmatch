"""
    Supporting Functions
"""

import os
import logging
import traceback
import json


# CONSTANTS ------------------------------------------------------------------------------------------------------------

PROGBAR_WIDTH          = 50
CONSOLE_WIDTH          = 80
LOGFILE_WIDTH          = 120
MENU_BAR_WIDTH         = 40
INDENT_DEBUG           = '        '
INDENT_ERR_DETAIL      = '              '


# COLOR FORMATS --------------------------------------------------------------------------------------------------------

TXT_NORMAL             = '\033[0m'
TXT_BOLD               = '\033[1m'
TXT_FAINT              = '\033[2m'
TXT_ITALIC             = '\033[3m'
TXT_UNDERLINE          = '\033[4m'
TXT_BLACK              = '\033[90m'
TXT_RED                = '\033[91m'
TXT_GREEN              = '\033[92m'
TXT_YELLOW             = '\033[93m'
TXT_BLUE               = '\033[94m'
TXT_MAGENTA            = '\033[95m'
TXT_CYAN               = '\033[96m'
TXT_WHITE              = '\033[97m'
HI_WHITE               = '\033[1m\033[9%sm\033[4%sm' % (0, 7)
HI_BLACK               = '\033[1m\033[9%sm\033[4%sm' % (7, 0)
HI_RED                 = '\033[1m\033[9%sm\033[4%sm' % (7, 1)
HI_GREEN               = '\033[1m\033[9%sm\033[4%sm' % (7, 2)
HI_YELLOW              = '\033[1m\033[9%sm\033[4%sm' % (7, 3)
HI_BLUE                = '\033[1m\033[9%sm\033[4%sm' % (7, 4)
HI_MAGENTA             = '\033[1m\033[9%sm\033[4%sm' % (7, 5)
HI_CYAN                = '\033[1m\033[9%sm\033[4%sm' % (7, 6)


# USER INTERFACE -------------------------------------------------------------------------------------------------------

def banner(msg='', red=False, black=False, magenta=False, green=False,
           cyan=False, yellow=False, blue=False, white=False, clearfirst=False):
    if red:         b = HI_RED
    elif black:     b = HI_BLACK
    elif magenta:   b = HI_MAGENTA
    elif green:     b = HI_GREEN
    elif cyan:      b = HI_CYAN
    elif yellow:    b = HI_YELLOW
    elif blue:      b = HI_BLUE
    elif white:     b = HI_WHITE
    else:           b = TXT_UNDERLINE
    if clearfirst:
        os.system('clear')
    log(msg, bcolor=b)

def track_status(txt, fname='~status'):
    with open(fname, "w+") as f:
        f.write(txt)

def log_warn(msg):
    log(msg, warn_txt=True)

def log_info(msg):
    log(msg, info_txt=True)

def log_err(e=None, trace=True):
    try:
        # Log Error (if given)
        if e:
            e = str(e).strip().upper()
            tracebk = ''
            if trace: tracebk = traceback.format_exc()
            log(e, err_txt=True, tracebk=tracebk)

        # No Error, so log traceback
        else:
            e = ''
            tracebk = traceback.format_exc()
            log(e, err_txt=True, tracebk=tracebk)

    except Exception as e: print('CRITICAL TRACKER ERROR: ' + str(e))

def log(msg, warn_txt=False, info_txt=False, err_txt=False, ljust=False, fcolor=TXT_BLUE, bcolor='', lf=True, tracebk=''):

    # PREP
    try:
        if type(msg) is not str and type(msg) is not Exception:
            try:
                msg = json.dumps(msg)                    # convert obj to string
            except:
                try: msg = str(msg)
                except: msg = 'Cannot log - invalid msg'
        if str(msg).startswith('\n'): msg = msg[1:]      # remove newline prefix
        if warn_txt: msg = str(msg).replace('\n', ';  ')       # flatten to one line
    except Exception as e:
        try: msg += '; Error logging msg: ' + str(e)
        except:
            try: msg = 'Unable to log msg: ' + str(e)
            except: msg = 'COMPLETE LOGGING MELTDOWN!'

    # to LOGFILE
    try:
        if err_txt:
            logging.info(str('====================>>> ERROR:  ' + msg + '  '
                             ).ljust(LOGFILE_WIDTH, '*'))
            if tracebk:
                lines = str(tracebk).strip().split('\n')
                out   = []
                if lines:
                    for line in lines[1:-1]:
                        line = str(line).strip()
                        if str(line).startswith('File '):
                            out.append(line)
                        else:
                            if out: out[-1] = out[-1] + ':  ' + line
                            else:   out.append(line)
                    if out:
                        for line in out:
                            logging.info(INDENT_ERR_DETAIL + line)

        elif warn_txt:    logging.debug('-------------------->>> ' +
                                        str(msg).replace('\n', '; '))
        elif bcolor:  logging.info(str(msg).ljust(CONSOLE_WIDTH, '.'))
        else:         logging.info(msg)

    except Exception as e:
        try:
            print('LOG TO LOGFILE ERROR: ' + str(e))
            print('ORIGINAL ERROR TEXT:  ' + str(msg))
            traceback.print_exc()
        except: pass

    # to CONSOLE
    try:

        # Errors
        if err_txt:
            print()
            print(HI_RED + str('ERROR: ' + msg).ljust(CONSOLE_WIDTH)+TXT_NORMAL)
            if tracebk:
                lines = str(tracebk).strip().split('\n')
                out   = []

                if lines:
                    try:

                        for line in lines[1:-1]:
                            line = str(line).strip()
                            if str(line).startswith('File '):
                                out.append(line)
                            else:
                                if out: out[-1] = out[-1] + ':  ' + line
                                else:   out.append(line)
                        if out:
                            for line in out:
                                print(TXT_RED + line + TXT_NORMAL)
                    except Exception as e: print('TRACEBACK ERROR:', str(e))
            print()

       # Non-Errors
        else:

            if bcolor:   msg = str(bcolor) + msg.ljust(CONSOLE_WIDTH)
            if warn_txt:     msg = TXT_RED + TXT_BOLD + msg
            if info_txt: msg = '    ' + TXT_WHITE + msg
            if ljust:    msg = str(msg).ljust(CONSOLE_WIDTH-24)
            if lf:
                print(fcolor  + msg + TXT_NORMAL)
            else:
                print(fcolor  + msg + TXT_NORMAL, end='', flush=True)

    except Exception as e:
        try:
            print('CONSOLE ERROR:', str(e))
            print('ORIGINAL TEXT:', str(msg))
            traceback.print_exc()
        except: pass


# MISC OTHER -----------------------------------------------------------------------------------------------------------

def break_points(lst, batch_no, num_batches):
    assert batch_no < num_batches
    assert num_batches < len(lst)
    batch_size = int(len(lst)/num_batches) + 1
    idx_start  = batch_no * batch_size
    idx_stop   = (batch_no + 1) * batch_size
    if idx_stop > len(lst): idx_stop = len(lst)  # possibly cut short final batch
    return idx_start, idx_stop

# Print iterations progress when match.py is called from the command line
def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total:
        print()