# BizMatch - A Utility to Match Business Names

_Copyright (c) 20120 by Kenneth A. Younge._  
  
Access to this code is provided subject to the [MIT License](https://opensource.org/licenses/MIT).    


## Overview

`bizmatch` provides an interactive approach to matching business names between two lists.  

Researchers often have a focal list of company names that they care about, and then they need to find matches (perhaps one-to-one, or perhaps one-to-many) of those companies on another list (what we will call the "alter list"). Part of that match might by automatic (e.g., the match is perfect), but other aspects of the match might be discretionary (i.e., the match is not perfect, the match depends on a point in time when the companies do/don't match, etc.). 

This program provides an iterative approach to the matching process. The user can run `bizmatch` to find **_direct matches_**, AND the user can run `bizmatch` to find **_candidate matches_** to examine in greater detail. After inspection of candidate matches the user can move matches that they find acceptable from the candidate list to the matched list, and/or tweak configuration settings such as synonyms, abbreviations, brand names, special cases, etc. to further refine the matching process. 


**Please note:** The default configuration for `bizmatch` may not be appropriate to your context. The default configuration is appropriate to matching pharmaceutical companies from databases such as EDGAR and the SEC. You will need to reconfigure all of the settings (files starting with a + sign) to meet your own matching problem. Instructions for configuring `bizmatch` appear below.


## Installation

Clone the module from GitHub into the working directory for your Python project.

    git clone https://github.com/KenYounge/bizmatch.git

Install all of bizy's requirements from the requirements.txt file:

    pip install -r bizmatch/requirements.txt

Customize the path to configuration files (optional). If you use PIP to install `bizmatch`, then the configuration files will be located in the library installation path. `bizmatch` will attempt to find and use files in that path, but you can override that decision by changing the following line in the `settings.py` file.

    PATH_CONFIG_FILES  = path.dirname(path.realpath(__file__)) + '/'

Review other settings in the `settings.py` file based on the business domain and the matching sensitivity that you need for your project. 


## Usage

### Input Files

The code matches business names on one "focal" list to one-or-many other business names
on an "alter" list. These lists may (optionally) also specify a date, so as to reject
matches that are not date appropriate. Each of the lists should be setup as follows:


    FOCAL.csv       set the FOCAL list below in the global constant

        purpose:    focal (left) side of match     (must be a unique list)

        format:     [raw_name], [date]             (optional)

    ALTER.csv       set the ALTER list below in the global constant)

        purpose:    alter (right) side of match    (there may be multiples)

        format:     [raw_name], [date]             (optional)


The repository comes with two lists of business names that you can already use for testing:  

  * `_edgar_biznames.csv` :  a focal list of business names from the SEC EDGAR database
  
  * `_sdc_biznames.cav`   : an alter list of business names from the SDC database. 


### Configuration Files for Cleaning Business Names

The code works through a set of word replacements, brandname replacements, known
name changes, name stemming, etc. to perform a better match. Each of those steps 
is driven by a particular configuration file. Using the following configuration 
files is optional. If a file does not exist in current directory, then code will  
run without them by assuming and empty list for that configuration item.
 
#####  +brands.txt

    purpose:    brand names to roll-up if it appears anywhere in name

    format:     one branded term (NO SPACES) per line

    examples:   ibm
                microsoft
                google

#####  +corp.txt

    purpose:    drop corp suffixes related to incorp or organization

    format:     one suffix per line

    examples:   inc
                co
                ltd
                company

#####  +rename.csv

    purpose:    rename companies entirely to handle FKAs
                works BY ENTIRE NAME & names should be precleaned

    format:     [oldname], [newname]

    examples:   Midland Electric, Inc., midwest electric
                southwest power, sunbelt electricity

#####  +replace.csv

    purpose:    harmonize abbreviations, synonyms, mis-spellings, etc.
                works BY PHRASE (not term-by-term or by entire name)
                phrases can include spacing or just be single terms
                this works differently than +rename.csv which is by line

    format:     [phrase-to-change], [phrase-to-become]

    examples:   bio tech, biotech
                hi tech, hitech
                general electric, ge
                intl, international
                transporte, transport
                biotechnology, biotech

#####  +skip.txt

    purpose:    ignore these business names
                build list from manual inspection
                works BY ENTIRE NAME
                name can be raw or cleaned, but best to use cleaned

    format:     one complete biz name per line

    examples:   ken's hi-tech laboratories
                kens hitech labs

#####  +stem.txt

    purpose:    stem certain terms with many alternatives

    format:     one stem per line  (just starting portion of the stem)

    examples:   pharma  (stems pharmaceutical, pharmaceuticals, etc.)
                sci     (stems science, scientific, etc...)
                chem    (stems chemical, chemistry, etc...)


## Temporary Files

The batching process creates intermediate temp files for each batch:

    ~candidates.###    these get rolled up into ~candidates.csv

    ~matched.###       these get rolled up into ~matched.csv

    ~status-###.txt    the current processing status of a batch (no LF)

You can delete temporary files after processing with this wildcard command:   

    rm ~*


## Output Files

On each run of bizmatch.py

    ~candidates.csv
    
        purpose:    alter (right) side of match    (there may be multiples)
    
        format:     [focalname], [altername]
    
        There can be multiple potential candidate matches for each
        focal business name. Candidates are sorted first on focal name
        (alphabetically) and then sorted on alter name by match distance.
        Simply delete invalid lines from the candidates file (leaving
        desired manual matches) and otherwise leave data alone.
    
    
    ~matched.csv
    
        purpose:    The final result of the matching routine.
    
        format:     [focalname], [altername]


## Execution 


#### To run everything in one pass...

Run `run_match.py` to match one list of business names to another list.
  
For example:

    python run_match.py _edgar_biznames.csv _sdc_biznames.csv


#### To run everything in parallel batches...

Run `run_batch.py` to match one list of biz names to another list, 
but to do so by dividing the problem in separate batches.  

For example, to parallelize across 4 cores:

    python run_batches.py _edgar_biznames.csv _sdc_biznames.csv 4 


#### To run a particular batch...

To run the 4th batch (zero-based index of 3) out of 4 batches:

    python run_match.py _edgar_biznames.csv _sdc_biznames.csv 4 3


## To import the module and use it directly... 

See the `example.ipynb` notebook.

You can also import one of the two main modules and call key functions directly.

    import match
    
    # Output is written directly to file
    match.match_lists(fname_focal, fname_alter, num_batches, batch_no)
    
or

    import compare

    # Output is a boolean
    result = compare.compare_biznames(name1, name2, debug=DEBUG)


# Disclaimer

_USE THIS CODE AT YOUR OWN RISK._ I provide no guarantee about it's security, safety, reliability, or any other potential risk or harm.