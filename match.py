"""
    Match company names on a focal list, to company names (1-to-1 or 1-to-many) on an alter list
"""

from datetime   import datetime
from compare    import *
from support    import *
from settings   import *

# MAIN MATCHING FUNCTION -----------------------------------------------------------------------------------------------

def match_lists(fname_focal, fname_alter, num_batches=1, batch_no=0):
    """
    Match business names between two lists.

    Args:
        fname_focal:    filename of the focal list of business names (given one of these)
        fname_alter:    filename of the alter list of business names (try to fine one or more of these)
        num_batches:    number of batches (if running in parallel)
        batch_no:       index of the batch to run right here, right now (if running in parallel)

    Return:
        matched pairs and candidate (but not yet matched) pairs are saved to disk
    """

    banner('Match business names from ' + fname_focal + ' to ' + fname_alter)

    # Prep
    count           = 0
    all_matched     = []
    all_candids     = []
    rename_dct      = _load_rename_dict()
    f_lst           = _load_bizname_list(fname_focal, rename_dct)
    a_lst           = _load_bizname_list(fname_alter, rename_dct)
    i_start, i_stop = break_points(f_lst, batch_no, num_batches)

    fio.delete_files_by_prefix('.', '~')   # Delete temp files

    try:

        # LOOP FOCALS
        for f_clean, f_raw, f_date in f_lst[i_start:i_stop]:

            matched, candids = _match_alters(f_clean, f_raw, f_date, a_lst, rename_dct)

            if matched: all_matched.extend(matched)
            if candids: all_candids.extend(candids)

            # STATUS
            track_status(
                    str(batch_no).rjust(3, '0') + ': ' +
                    str(len(all_matched)) + ' matched / ' +
                    str(len(all_candids)).rjust(2) + ' candidates' +
                    '  [' +
                    str(' ' + str("%.1f" % round(
                            (float(count) / (i_stop - i_start)) * 100, 1)
                                  ).rjust(4, ' ') + '%' +
                        ']'),
                    '~status.' + str(batch_no).rjust(3, '0'))
            count += 1
            printProgressBar(count, len(f_lst[i_start:i_stop]), prefix='Progress:', suffix='Complete', length=50)

    except Exception as e:
        log_err(e)

    # Save results (the successful matches and the candidate potentials)
    fio.save_csv(all_matched, '~matched.'    + str(batch_no).rjust(3, '0'))
    fio.save_csv(all_candids, '~candidates.' + str(batch_no).rjust(3, '0'))

# SUPPORTING FUNCTIONS -------------------------------------------------------------------------------------------------

def _match_alters(f_clean, f_raw, f_date, a_lst, rename_dct):

    matched = list()
    candids = list()

    assert rename_dct   # NOTE >> not being used yet - but require it now for future compatability

    for a_clean, a_raw, a_date in a_lst:

        m, c = _match_names(f_clean, f_raw, f_date, a_clean, a_raw, a_date)
        if m: matched.append(m)
        if c: candids.append(c)

        if not ALLOW_ONE_2_MANY and m: break

    return matched, candids

def _match_names(f_clean, f_raw, f_date, a_clean, a_raw, a_date, days_before=ALLOW_DAYS_BEFORE, days_after=ALLOW_DAYS_AFTER, candidate_diff=CANDID_DIFF, candidate_threshold=CANDID_THRESHOLD):


    matched = None
    candid  = None

    if f_clean and f_raw and a_clean and a_raw:

        # require same first char
        if f_clean[0] == a_clean[0]:

            # precalc date check
            dates_ok = True
            if f_date and a_date:
                days = (a_date - f_date).days
                if days >  days_after:  dates_ok = False
                if days < -days_before: dates_ok = False

            # check dates
            if dates_ok:

                # check diff in string lengths
                if abs(len(f_clean)-len(a_clean)) <= candidate_diff:

                    f_chars = {c for c in f_clean}
                    a_chars = {c for c in a_clean}
                    common  = f_chars.intersection(a_chars)
                    n_diff  = abs(max(len(f_chars),len(a_chars)) - len(common))

                    # check num of different unique chars
                    if n_diff <= candidate_diff:

                        # calc dist now (late) to save runtime
                        dist = calc_distance(f_clean, a_clean)

                        # EXACT MATCH
                        if dist == 0:
                            matched = (f_raw, a_raw)

                        # Potential Candidate?
                        else:

                            # calc % of name that is similar
                            ratio = 1 - (float(dist) /
                                           min(len(f_clean),len(a_clean)))

                            # CANDIDATE
                            if ratio > candidate_threshold:
                                candid = (f_raw, a_raw)

    # return
    return matched, candid

def _load_bizname_list(fname, rename_dct):
    log('Loading ' + fname + ' ...')

    f_lst = fio.load_csv(fname)
    if len(f_lst[0]) == 1: f_lst = [ (n, None) for n in f_lst]  # Add if missing
        
    f_out = []
    for raw_name, d in f_lst:
        if d: 
            f_out.append( (clean_name(raw_name, rename_dct), raw_name, datetime.strptime(d, DATE_FORMAT)) )
        else:
            f_out.append( (clean_name(raw_name, rename_dct), raw_name, None) )
    return f_out

def _load_rename_dict():
    log('Loading rename list...')
    rename_dct = dict()
    for oldname, newname in RENAMES:
        rename_dct[oldname] = newname
        rename_dct[clean_name(oldname)] = newname
    return rename_dct
