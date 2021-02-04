* fixed bug in spherical

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
