```python
%load_ext autoreload
%autoreload 2
```

```python
from corhel.psihdf import rdhdf
```

<!-- #region -->

# Slice Interpolation


## 3D interpolation

The core challenge is to link each field signature with a fast interpolator.
For single timestep 3d interpolation, scipy's `RegularGridInterpolator` will suffice. This is the original interpolator CORHEL-Kamodo was built on.
<!-- #endregion -->

```python
from corhel import CORHEL_Kamodo
```

```python
cor = CORHEL_Kamodo('/home/data/areyes_at_predsci.com_20210319_1_zb', mhd_path='cme/mhd', cartesian=True)
```

```python
cor.b_r(r=1.0).shape
```

## 4D interpolation

Time-dependent interpolation, there are too many files to load into memory at once. To accomplish this, we need to leverage parallel readers. There are several tools available for this task, each with their own trade-offs and infrastructure requirements.

### Dask

Dask runs parallel tasks on multiple processes either on the same machine or multiple machines. With dask, we start a client connected to a Master node which talks to the various worker processes.

```python
from dask.distributed import Client
client = Client('tcp://scheduler:8786')
client
```

The above client includes a dashboard that allows us to monitor the work done by the workers.


### Xarray


We'll use xarray to leverage dask on our runs. Read [here](https://xarray.pydata.org/en/v0.10.1/dask.html) for more on how xarray and dask work together. The solution for concatonating across files is taken from [this stackoverflow comment](https://stackoverflow.com/a/64542348/2793333).

```python
from corhel import convert_run
```

```python
help(convert_run)
```

```python
import xarray as xr
```

```python
run_orig = '/home/data/areyes_at_predsci.com_20210319_1_zb/cme/mhd'
```

```python
rundir = '/dumpster/areyes_at_predsci.com_20210319_1_zb/cme/mhd'
```

```python
runfiles = convert_run(run_orig, rundir)
```

```python
br = xr.open_mfdataset('{}/br*.nc'.format(rundir),
                  combine = 'nested',
                  concat_dim='time', parallel=True)
br
```

```python
ds = br.interp(time=1.5, r=1.5)
```

```python
ds.compute()
```

Dask auotmatically parallelizes the xarray, which is now ready for slicing:

```python
ds = br.interp(time=2.5, phi=3.0)
ds
```

### Kamodofying slicer

The process of loading and registering parallelized interpolators may be managed by subclassing `Kamodo`.

```python
Client?
```

```python
from kamodo import Kamodo, kamodofy
from dask.distributed import Client
import xarray as xr

def da_to_np(da):
    return da.__xarray_dataarray_variable__.data

class Corhel(Kamodo):
    def __init__(self, rundir, variable_names=['br'], scheduler=None, **kamodo_kwargs):
        """params
        rundir = <run directory of mhd files>
        scheduler = <address of dask scheduler>
        kamodo_kwargs: {dict} additional function variables to register
        """
        self._scheduler = scheduler
        self._client = Client(self._scheduler)
        self._rundir = rundir
        self._data = {}
        
        self.get_variables(variable_names)
        
        super(Corhel, self).__init__(**kamodo_kwargs)
        self.register_interpolators()
    
    def get_variables(self, variable_names):
        for varname in variable_names:
            self._data[varname] = xr.open_mfdataset(
                '{}/{}*.nc'.format(self._rundir, varname),
                combine = 'nested',
                concat_dim='time',
                parallel=True)

    
    def register_interpolators(self):
        for varname, variable in self._data.items():
            @kamodofy(data={})
            def func(t=variable.time, r=variable.r, theta=variable.theta, phi=variable.phi):
                result = variable.interp(r=r, theta=theta, phi=phi, time=t).compute()
                return da_to_np(result)
            
            self[varname] = func
                 

```

```python
rundir = '/dumpster/areyes_at_predsci.com_20210319_1_zb/cme/mhd'
```

```python
cor = Corhel(rundir, ['br'], 'tcp://scheduler:8786', f='x')
cor
```

```python
da = cor.br(t=1.5, r=1.5)
```

```python
cor.plot(br=dict(t=1.5, r=1.5))
```

```python

```
