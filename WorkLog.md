### 2020-11-18 15:05:50.176686: clock-out

Had to run `pip install --upgrade pip setuptools wheel`

#### CORHEL-Kamodo 

Kamodo is an open source python package under development at the Community Coordinated Modeling Center (CCMC). Predictive Science Inc. (PSI) has begun adopting Kamodo as part of its visualization toolset for Corona-Heliosphere (CORHEL), created by PSI and also available at the CCMC. By "Kamodofying" CORHEL's run output, all scientifically relevant fields are registered as interpolating functions with defaults, units, and names suitable for LaTeX legibility. This allows CORHEL fields to be manipulated symbolically, with automated unit conversion, quick-look grahics, dashboards and command line accessibility. The CORHEL-Kamodo interface is tailored for the analysis and visualization of both solar and heliospheric model output.

Kamodo is an open source symbolic python framework that seeks to represent physical data as continuous fields. This formulation enables many common analysis and visualization tasks to be framed in terms of function composition familiar to science users.


#### Kamodo basics

In order for discrete model output to be represented as physical continuous fields, each field to is registered as a symbol-interpolating function pair held in a Kamodo object. 

Kamodofying a given model consists of:

1. providing interpolating routines for all scientifically relevant physical fields

2. providing units for each of the above

3. providing default values for arguments to interpolation routines


#### User Derived Variables

Science users may register new (derived) variables by referencing previously defined CORHEL fields in their expressions. Such expression may involve coordinate transformations or make use of plasma physics formulary.
Upon registration of a user expression, users may indicate their prefered units for their derived variables.
For example, CORHEL-Kamodo registers density in units.

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
