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
# ## About
#
# Converts runs from h4 -> h5
#
# Setup: 
#
# * To test this script, we will assume `areyes_at_predsci.com_20210319_1_zb` has been mounted into `/home/data`
# * We assume /dumpster can store h5 files
#
# using hdfh4:
# ```console
# hdfh5 hdf4_filename [hdf5_filename]
# ```

# %%
import os

# %% [markdown]
# These are the variables we will convert. We'll look for files matching `<var><number>.hdf`

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
from psihdf import rdhdf
import xarray as xr


# %%
def convert_file(dirname, fname, outdir, overwrite=False):
    outname = fname.split('.hdf')[0] + '.nc'
    outfile = '{outdir}/{outname}'.format(**locals())
    infile = '{dirname}/{fname}'.format(**locals())
    if overwrite:
        phi, theta, r, variable = rdhdf(infile)
        da = xr.DataArray(variable, [('phi', phi), ('theta', theta), ('r', r)])
        da.to_netcdf(outfile)
    else:
        if os.path.exists(outfile):
            return '{outfile} already exists'.format(**locals())
        else:
            phi, theta, r, variable = rdhdf(infile)
            da = xr.DataArray(variable, [('phi', phi), ('theta', theta), ('r', r)])
            da.to_netcdf(outfile)
    return outfile

def has_digit(inputString):
    return any(char.isdigit() for char in inputString)

# %% active="ipynb"
# convert_file('/home/data/areyes_at_predsci.com_20210319_1_zb/cme/mhd',
#              'br001.hdf',
#              '/dumpster/cme/mhd')


# %%
def convert_run(rundir, outdir, variables=variables, verbose=False, overwrite=False):
    """converts runs from h4 -> h5 using hdfh5 (psi command line tool)"""
    dirpath, dirnames, filenames = next(os.walk(rundir))
    os.makedirs(outdir, exist_ok=True)
    for variable in variables:
        for file_ in filenames:
            if (file_.startswith(variable)) & (file_.endswith('hdf') & (has_digit(file_))):
                output = convert_file(dirpath, file_, outdir, overwrite=overwrite)
                if verbose:
                    print(output)
    dirpath, dirnames, filenames = next(os.walk(outdir))
    return ['{}/{}'.format(dirpath, _) for _ in filenames]


# %% active="ipynb"
# outfiles = convert_run('/home/data/areyes_at_predsci.com_20210319_1_zb/cme/mhd',
#                        '/dumpster/cme/mhd',
#                        verbose=False, overwrite=False)

