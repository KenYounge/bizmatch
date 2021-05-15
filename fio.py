"""
    File I/O
"""

import os
import csv
import subprocess


# LOAD -------------------------------------------------------------------------

def load_lst(fname, force2int=False, default_no_file=False):
    fname = str(fname.strip())
    if not os.path.exists(fname):
        if default_no_file:
            return list()
        else:
            raise IOError
    lst = list()
    with open(fname, mode='r', encoding='utf-8') as f:  # universal newlines support; read-only
        lines = f.readlines()
        for line in lines:
            value = str(line).strip()
            if force2int: value = int(value)
            lst.append(value)
    return lst

def load_set(fname, force2int=False, freeze=False, default_no_file=False):
    fname = str(fname.strip())
    if not os.path.exists(fname):
        if default_no_file:
            return set()
        else:
            raise IOError
    bag = set()
    with open(fname, mode='r', encoding='utf-8') as f:   # universal newlines support; read-only
        lines = f.readlines()
        for line in lines:
            value = str(line).strip()
            if force2int: value = int(value)
            bag.add(value)
    if freeze:
        bag = frozenset(bag)
    return bag

def load_dct(fname, force2int=False, default_no_file=False):
    fname = str(fname.strip())
    if not os.path.exists(fname):
        if default_no_file:
            return dict()
        else:
            raise IOError
    returndict = dict()
    with open(fname, mode='r', encoding='utf-8') as f:   # universal newlines support; read-only
        for r in csv.reader(f, dialect='excel'):
            if force2int:
                if r[0] != "": returndict[r[0]] = int(r[1])
            else:
                if r[0] != "": returndict[r[0]] = r[1]
    return returndict

def load_str(fname, default_no_file=False):
    fname = str(fname.strip())
    if not os.path.exists(fname):
        if default_no_file:
            return ""
        else:
            raise IOError
    with open(fname, 'r') as f:   # read-only
        txt = f.read()
    return txt

def load_csv(fname, quote=None, default_no_file=False):
    fname = str(fname.strip())
    if not os.path.exists(fname):
        if default_no_file:
            return list( list() )
        else:
            raise IOError
    out = list()
    with open(fname, mode='r', encoding='utf-8') as f:   # universal newlines support; read-only
        csv_reader = csv.reader(f, dialect='excel',
                quotechar=quote) if quote else csv.reader(f, dialect='excel')
        for r in csv_reader:
            out.append([value for value in r])
    return out


# READ -------------------------------------------------------------------------

def read_csv(fname, skip_header=False):
    assert os.path.exists(fname)
    lst_generator = (r for r in csv.reader(open(fname, mode='r', encoding='utf-8'), dialect='excel'))
    if skip_header: next(lst_generator)
    return lst_generator


# SAVE -------------------------------------------------------------------------

def save_str(txt, fname):
    fname = str(fname.strip())
    if os.path.exists(fname): os.remove(fname)
    with open(fname, 'w', encoding='utf-8') as f:
            f.write(txt)
    assert os.path.exists(fname)

def save_lst(lst, fname):
    fname = str(fname.strip())
    if lst is None: lst = list()
    if os.path.exists(fname): os.remove(fname)
    with open(fname, 'w', encoding='utf-8') as f:
        for i in range(len(lst)):
            item = str(lst[i])
            if i < (len(lst) - 1): item += "\n"
            f.write(item)

def save_csv(lst, fname):
    fname = str(fname.strip())
    if os.path.exists(fname): os.remove(fname)
    with open(fname, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel')
        writer.writerows(lst)

def save_dct(dct, fname):
    fname = str(fname.strip())
    if os.path.exists(fname): os.remove(fname)
    with open(fname, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel')
        keys = dct.keys()
        for key in keys:
            writer.writerow( (key, dct[key]))

def append_csv(out, fname):
    fname = str(fname.strip())
    with open(fname, 'a', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='excel')
        if type(out) is str:
            writer.writerow(out)
        else:
            writer.writerows(out)

def append_str(txt, fname):
    fname = str(fname.strip())
    if txt:
        with open(fname, 'a', encoding='utf-8') as f:
                f.write(txt)


# DELETE -----------------------------------------------------------------------

def delete_file(fname):
    fname = str(fname.strip())
    if os.path.exists(fname): os.remove(fname)

def delete_files(fpath):
    if not fpath: fpath='.'
    if not fpath.endswith('/'): fpath += '/'
    fnames = list_fnames(fpath)
    for fname in fnames:
        delete_file(fpath + fname)

def delete_files_by_prefix(fpath, prefix):
    if not fpath: fpath='.'
    if not fpath.endswith('/'): fpath += '/'
    fnames = list_fnames(fpath)
    for fname in fnames:
        if str(fname).startswith(prefix):
            delete_file(fpath + fname)


# GOOGLE STORAGE ---------------------------------------------------------------

def gs_copy_file(source_file, dest_file):
    assert source_file, 'No SOURCE file specified'
    assert dest_file,   'No DESTINATION file specified'
    print(subprocess.check_output(['gsutil', 'cp', source_file, dest_file]))


def gs_list_bucket(bucket_name):
    assert bucket_name, 'No Bucket Name specified'
    sims_csv_string = subprocess.check_output(['gsutil', 'ls', 'gs://' + bucket_name])
    sims_csv_list   = sims_csv_string.split('\n')
    return filter(None, sims_csv_list)


# MISC -------------------------------------------------------------------------

def list_fnames(dirpath=''):
    """Walk directory and gather list of filenames"""
    if not dirpath: dirpath='.'
    return next(os.walk(dirpath))[2]

def file_exists(fname):
    return os.path.exists(fname)
