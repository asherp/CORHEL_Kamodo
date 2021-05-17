# ---
# jupyter:
#   jupytext:
#     formats: py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.11.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# Converts runs from h4 -> h5

# %% [markdown]
# Setup: 
#
# * To test this script, we will assume `areyes_at_predsci.com_20210319_1_zb` has been mounted into `/home/data`
# * We assume /dumpster can store h5 files

# %%
# ls /dumpster

# %%
import os

# %%
variables = [
    'br',
    'bt',
    'bp',
    'vr',
    'vt',
    'vp',
    'jr',
    'jt',
    'jp',
#     'p',
    
]


# %%
def has_digit(inputString):
    return any(char.isdigit() for char in inputString)
    
def convert_run(rundir, outdir, variables = variables):
    # converts runs from h4 -> h5 using hdfh5 (psi command line tool)
    _, _, filenames = next(os.walk(rundir))
    files_h4 = []
    for variable in variables:
        print()
        for file_ in filenames:
            if (file_.startswith(variable)) & (file_.endswith('hdf') & (has_digit(file_))):
                print(file_)
#     return filenames

convert_run('/home/data/areyes_at_predsci.com_20210319_1_zb/cme/mhd', '/dumpster/cme/mhd')


# %%
