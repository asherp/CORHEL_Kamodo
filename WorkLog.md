
### 2021-06-01 12:18:46.049112: clock-in

### 2021-05-24 16:54:42.090389: clock-out

* need 4d plotting from kamodo

### 2021-05-24 16:53:33.671538: clock-in

### 2021-05-20 16:56:24.693099: clock-out

* got numpy array back from interpolated slice
* `NotImplementedError: No way to handle out_shape (259, 195), with arg shapes:((1,), (1,), (195,), (259,))
`

### 2021-05-20 15:31:10.366153: clock-in

### 2021-05-20 12:27:56.193794: clock-out

* tring to pull interpolated results from dask. something weird with h5. Try netcdf?

### 2021-05-20 10:20:11.468816: clock-in

### 2021-05-20 10:00:57.995083: clock-out


### 2021-05-20 09:27:07.345793: clock-in

### 2021-05-19 17:54:22.783798: clock-out

* kamodofying parallel dask slicer - bug in kamodofy

### 2021-05-19 16:06:00.071139: clock-in

### 2021-05-18 19:34:35.609858: clock-out: T-1h 


### 2021-05-18 18:24:59.282613: clock-in

### 2021-05-18 18:02:28.766370: clock-out


### 2021-05-18 17:14:04.431893: clock-in

### 2021-05-18 14:16:45.684997: clock-out

* creating documentation site
* adding docker entrypoint
* mathjax difficulties - not sure why kamodo equations are not rendering. here's another mathjax plugin https://squidfunk.github.io/mkdocs-material/reference/mathjax/

### 2021-05-18 12:20:41.321167: clock-in

### 2021-05-17 17:54:39.359043: clock-out

* added run_conversion tool

### 2021-05-17 16:30:55.291775: clock-in

### 2021-05-17 14:06:36.434041: clock-out

* adding run conversion script

### 2021-05-17 13:32:04.149842: clock-in

### 2021-04-22 13:07:09.455782: clock-out

* looking at more numpy parallel libraries
pnumpy
* https://quansight.github.io/pnumpy/stable/index.html
* I'm not able to see a significant speed improvement with my tests. 
* This issue mentions how pnumpy would fit into numpy natively in contrast to dask. https://github.com/numpy/numpy/issues/18028

Clearlinux
* looked at clearlinux/numpy-mp for parallel numpy https://github.com/clearlinux/dockerfiles/tree/master/numpy-mp
* numpy-mp Explainer article here https://clearlinux.org/blogs-news/improving-python-numpy-performance-kubernetes-using-clear-linux-os


Legate
* creating legate conda environment. legate.numpy removed their dockerfiles
* created issue on their github
* installing legate.numpy into new conda environment

```console
conda env create -n legate -f conda/legate_numpy_dev.yml
conda activate legate
python setup.py --with-core /Users/asherp/miniconda3/envs/legate
```
* last step would not complete



### 2021-04-22 11:27:19.518453: clock-in

### 2021-04-12 18:48:58.311015: clock-out

* looking at legate core https://github.com/nv-legate/legate.numpy

### 2021-04-12 18:34:46.165005: clock-in

### 2021-04-09 13:06:37.904612: clock-out

* added notebook for running mapfl in predsi/psiweb

### 2021-04-09 11:32:03.214247: clock-in

### 2021-04-06 13:22:34.865792: clock-out

* got point interpolation working on dask cluster
`docker-compose up --scale worker=6`

### 2021-04-06 12:18:06.677667: clock-in

### 2021-04-05 12:06:32.220139: clock-out


### 2021-04-05 11:55:34.655431: clock-in

### 2021-04-02 15:06:54.383176: clock-out

* got spacetime domain across multiple workers

### 2021-04-02 11:25:16.243787: clock-in

### 2021-04-01 19:07:44.677278: clock-out

* bind mounts vs volumes https://4sysops.com/archives/introduction-to-docker-bind-mounts-and-volumes/

bind mounts are the same as -v /my/host/path:/container/path

Got dask to share data

`docker-compose up --scale worker=6`

`pip install git+https://github.com/fujiisoup/xr-scipy.git`

* tried this
```from xrscipy.interpolate import RegularGridInterpolator as xaRegularGridInterpolator```

* [pyinterp](https://pangeo-pyinterp.readthedocs.io/en/latest/index.html): lots of interpolation libraries all rolled into one!
Unfortunately may need to build this by hand
```console
ImportError: /opt/conda/lib/python3.7/site-packages/zmq/backend/cython/../../../../.././libstdc++.so.6: version `GLIBCXX_3.4.26' not found (required by /opt/conda/lib/python3.7/site-packages/pyinterp/core.cpython-37m-x86_64-linux-gnu.so)
```

### 2021-04-01 17:16:20.276714: clock-in

### 2021-04-01 15:36:47.899504: clock-out: T-6m 

* dask docker workers

### 2021-04-01 15:10:43.953746: clock-in

### 2021-04-01 14:41:03.800861: clock-out


### 2021-04-01 14:38:28.214160: clock-in

### 2021-04-01 11:10:41.303586: clock-out


### 2021-04-01 10:43:48.197848: clock-in

### 2021-03-31 18:23:38.650528: clock-out

* moving data into dask/xarray

### 2021-03-31 18:05:34.105090: clock-in

### 2021-03-31 18:00:42.707843: clock-out


### 2021-03-31 17:17:30.928038: clock-in

### 2021-03-31 17:11:45.417110: clock-out


### 2021-03-31 16:21:24.973897: clock-in

### 2021-03-31 15:35:50.095302: clock-out


### 2021-03-31 15:10:31.021326: clock-in

* updating base kamodo container version

### 2021-03-05 12:43:27.494944: clock-out: T-25m 

* setting up simple interpolator

### 2021-03-05 12:13:52.346694: clock-in

### 2021-02-09 21:05:25.324321: clock-out


### 2021-02-09 21:05:09.608622: clock-in

### 2021-02-09 17:49:34.460096: clock-out

* added figure rescaling functions

### 2021-02-09 17:20:29.394866: clock-in

### 2021-02-04 14:40:06.962311: clock-out

* fixed current sheet generation

### 2021-02-04 14:16:11.750235: clock-in

### 2021-02-04 13:45:43.378325: clock-out: T-13m 


### 2021-02-04 13:22:39.118876: clock-in

### 2021-02-04 13:07:32.209841: clock-out


### 2021-02-04 13:04:55.056341: clock-in

### 2021-02-04 11:28:50.218218: clock-out


### 2021-02-04 11:22:21.871343: clock-in

### 2021-02-04 10:55:47.419293: clock-out

* build docker image, default results are too large
* building image `docker build -f corhel.Dockerfile -t apembroke/corhel_kamodo .`
* fixed bug in spherical causing plots to look weird

### 2021-02-04 09:04:07.040524: clock-in

### 2021-02-03 09:37:19.621823: clock-out

* `conda install -c conda-forge idna`
* `TypeError: Unable to serialise object of type <class 'generator'>`

### 2021-02-03 08:55:29.193263: clock-in

### 2021-01-13 17:32:14.017309: clock-out


### 2021-01-13 17:29:38.632651: clock-in

### 2021-01-13 13:01:14.636426: clock-out

* setting up docker container
* Mount the run into the container working directory

```console
cd /Users/asherp/git/psi/report_generator/test/runs/July2017/corhel_run_heating_model_2/ut201707140030-custom/ilabel2_bg/cor
docker run -it --mount type=bind,source="$(pwd)",destination=/local,consistency=cached -p 8888:8888 asherp/corhel_kamodo
```

### 2021-01-13 11:57:30.973046: clock-in

### 2020-12-08 13:47:12.066175: clock-out

* AGU poster

### 2020-12-08 10:26:49.310591: clock-in

### 2020-11-24 14:42:52.703798: clock-out


### 2020-11-24 12:39:59.785131: clock-in

### 2020-11-23 20:08:05.869753: clock-out

* submitted poster

### 2020-11-23 20:07:53.906199: clock-in: T-4h 

### 2020-11-23 14:10:53.019667: clock-out


### 2020-11-23 11:23:46.240031: clock-in: T-10m 

### 2020-11-22 22:55:56.257898: clock-out: T-32h 

* registered for AGU

### 2020-11-21 14:19:31.935128: clock-in

### 2020-11-20 18:54:58.901432: clock-out

* got field line traces to render
* I don't know how I was able to merge psiweb dev into master without including the `mhdweb` folder!


### 2020-11-20 16:14:26.213620: clock-in

### 2020-11-20 14:07:55.353961: clock-out


### 2020-11-20 11:26:20.426302: clock-in

### 2020-11-20 11:18:49.853476: clock-out

* yt has ability to load spherical data https://yt-project.org/docs/dev/examining/spherical_data.html#loading-spherical-data

### 2020-11-20 11:09:49.785987: clock-in

### 2020-11-20 10:53:50.407847: clock-out

* looking at volume rendering with yt

### 2020-11-20 10:39:11.493366: clock-in

### 2020-11-19 20:03:32.754114: clock-out

* working on field lines

### 2020-11-19 18:45:17.572343: clock-in

### 2020-11-19 15:35:05.406133: clock-out


### 2020-11-19 13:35:29.860167: clock-in

### 2020-11-18 21:05:27.360667: clock-out

`@gridify` - had to insert sparse and copy keywords

```python
# manually generate the appropriate function signature
grid_wrapper_def = r"""def wrapped({signature}):
    coordinates = np.meshgrid({arg_str}, indexing = 'xy', sparse = False, copy = False)
    points = np.column_stack([c.ravel() for c in coordinates])
    return np.squeeze({fname}(points).reshape(coordinates[0].shape, order = 'A'))
    """
```

```python
def to_agu(corhel):
	'''prints latex for rendering in agu poster'''
    print(corhel.to_latex().replace('\\begin{equation}','').replace('\\end{equation}',' \\\\ '))
```


The CORHEL-Kamodo object will be rendered as a list of equations when initialized in a Jupyter notebook. The right-hand side are black-box "lambda" functions pointing to grid interpolators.

```console
\operatorname{r^{r1}_{r0}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{t^{r1}_{r0}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{p^{r1}_{r0}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{e^{r1}_{r0}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{r^{r0}_{r1}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{t^{r0}_{r1}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{p^{r0}_{r1}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{e^{r0}_{r1}}{\left(\phi,\theta \right)} = \lambda{\left(\phi,\theta \right)} \\ \operatorname{b_{\theta}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{b_{\phi}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{b_{r}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{j_{\theta}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{j_{\phi}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ p{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \rho{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ t{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{v_{r}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{v_{\theta}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{v_{\phi}}{\left(\phi,\theta,r \right)} = \lambda{\left(\phi,\theta,r \right)} \\ \operatorname{b^{c}_{r}}{\left(c \right)} = \lambda{\left(c \right)}
```


### 2020-11-18 19:30:56.358031: clock-in

### 2020-11-18 15:05:50.176686: clock-out

Had to run `pip install --upgrade pip setuptools wheel`


### 2020-11-18 13:16:01.060176: clock-in

### 2020-11-18 11:19:24.838656: clock-out


### 2020-11-18 11:05:55.101934: clock-in

* added contouring

### 2020-05-28 15:40:45.037364: clock-out

* looking at flux rope designer notes
* components are in different spaces!

### 2020-05-28 13:33:19.162010: clock-in

### 2020-05-28 13:00:42.064893: clock-out

* trying python-forge to obtain signatures
* Starting new CORHEL-Kamodo notebook demonstrating usage in r,theta, phi space
* Contouring

### 2020-05-28 09:54:59.456157: clock-in

* testing
* can register a hidden kamodo object storing cartesian version `_cartesian`, then use closure
* looking at closures
* cant compose with generator expressions

### 2020-05-27 14:38:53.892886: clock-in

### 2020-05-27 11:38:08.358790: clock-out

* loaded mas variables

### 2020-05-27 10:48:11.020544: clock-in

### 2020-05-26 20:53:49.816195: clock-out

* loading imas file

### 2020-05-26 19:21:04.821497: clock-in

### 2020-05-26 17:01:06.337252: clock-out


### 2020-05-26 16:07:30.001474: clock-in

### 2020-05-26 15:52:42.885896: clock-out


### 2020-05-26 15:49:31.996366: clock-in

### 2020-05-26 15:38:22.439733: clock-out

* got theta as a 2d contour

### 2020-05-26 15:19:58.409924: clock-in

### 2020-05-26 15:06:20.073633: clock-out

* trying to get contour function working

### 2020-05-26 12:36:41.095479: clock-in

### 2020-05-26 12:14:14.128707: clock-out


### 2020-05-26 11:45:37.281187: clock-in

### 2020-05-26 11:40:47.227546: clock-out


### 2020-05-26 11:30:08.123871: clock-in

### 2020-05-22 15:57:50.687781: clock-out

* hanlded different arg shapes for interpolator

### 2020-05-22 15:36:57.250514: clock-in

### 2020-05-22 12:47:13.576222: clock-out


### 2020-05-22 11:26:23.350529: clock-in

### 2020-05-21 18:04:05.556221: clock-out

* contours are interfering with 3d surface plot
* trying to match contours with surface plot

### 2020-05-21 16:59:19.694888: clock-in

### 2020-05-21 15:18:08.851965: clock-out

* developing 3d contours
* attending xsede notebook webinar

### 2020-05-21 13:28:05.178440: clock-in

### 2020-05-21 13:15:54.059450: clock-out


### 2020-05-21 13:12:02.294538: clock-in

### 2020-05-21 12:53:43.139976: clock-out

* got first 3d plots to work
* should try sparse meshgrid

### 2020-05-21 11:26:27.770624: clock-in

### 2020-05-20 18:45:15.613156: clock-out


### 2020-05-20 17:25:06.681873: clock-in

### 2020-05-20 16:01:51.860061: clock-out: T-15m 


### 2020-05-20 15:14:00.077893: clock-in

### 2020-05-20 14:34:42.024411: clock-out


### 2020-05-20 13:16:04.923519: clock-in

### 2020-05-20 10:40:07.349380: clock-out

* trying to generate parametric surface

### 2020-05-20 08:53:47.705869: clock-in

* kamodofied cartesian/spherical coordinates
* created initial corhel reader
