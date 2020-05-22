from kamodo import Kamodo, kamodofy, gridify
import psihdf
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import os
import matplotlib.pyplot as plt

class Spherical(Kamodo):
    def __init__(self,
        x = np.linspace(-1, 1, 100),
        y = np.linspace(-1, 1, 100),
        z = np.array([1])):
        super(Spherical, self).__init__()

        # @gridify(x = x, y = y, z = z)
        def r(xvec):
            x, y, z = xvec.T
            return (x**2 + y**2 + z**2)**.5

        # @gridify(x = x, y = y, z = z)
        def theta(xvec):
            x, y, z = xvec.T
            return np.arcsin(z/(x**2 + y**2 + z**2)**.5)

        # @gridify(x = x, y = y)
        def phi(xvec):
            x, y, z = xvec.T
            return np.arctan2(y,x)

        @kamodofy(equation = '$\\vec{r}(\\vec{x}) = r(\\vec{x}), \\theta(\\vec{x}), \\phi(\\vec{x})$')
        def rvec(xvec):
            return np.vstack((r(xvec).ravel(), theta(xvec).ravel(), phi(xvec).ravel())).T

        self['r'] = 'sqrt(x**2 + y**2 + z**2)'
        self['theta'] = 'pi/2 - asin(z/r)'
        self['phi'] = 'pi - atan2(y,x)'
        self['rvec'] = rvec

class Cartesian(Kamodo):
    def __init__(self, 
                 r = np.array([1]), 
                 theta = np.linspace(0, np.pi, 180),
                 phi = np.linspace(0, 2*np.pi, 360)):
        super(Cartesian, self).__init__()
        
        @gridify(r = r, theta = theta, phi = phi)
        def x(rvec):
            r, theta, phi = rvec.T
            return r*np.sin(theta)*np.cos(phi)
        
        @gridify(r = r, theta = theta, phi = phi)
        def y(rvec):
            r, theta, phi = rvec.T
            return r*np.sin(theta)*np.sin(phi)
        
        @gridify(r = r, theta = theta)
        def z(rvec):
            r, theta = rvec.T
            return r*np.cos(theta)
        
        self['z'] = 'r*sin(pi/2 - theta)'
        self['x(r,theta, phi)'] = 'r*sin(theta)*cos(pi - phi)'
        self['y(r,theta, phi)'] = 'r*sin(theta)*sin(pi - phi)'
        self['xvec'] = lambda x, y, z: np.hstack((x.ravel(), y.ravel(), z.ravel()))

def get_contours(x_i,y_j,m_ij,c_vals):
    cs = plt.contour(x_i,y_j,m_ij, c_vals)
    paths = []
    t_vals = []
    for i,c_val in enumerate(c_vals):
        c = cs.collections[i]
        for p in c.get_paths():
            segment = np.vstack((p.vertices, np.ones(2)*np.nan))
            paths.append(segment)
            t_vals.append(np.ones(len(segment))*c_val)
    vertices = np.vstack(paths)
    t_vals = np.hstack(t_vals)
    theta_, phi_ = vertices.T
    return t_vals, theta_, phi_


class CORHEL_Kamodo(Kamodo):
    def __init__(self,
            rundir,
            mapfl_r1_r0_path = 'cor/mapfl_r1_r0/mapfl.in', 
            verbosity = 0,
            grid = True,
            missing_value = np.nan):

        
        self.verbosity = verbosity
        self._rundir = rundir
        self._mapfl_r1_r0_path = mapfl_r1_r0_path
        self._map_data = {}
        self._missing_value = missing_value
        self.load_mapfl_in()
        self.load_mapping()
    
        super(CORHEL_Kamodo, self).__init__() 
        
        self.register_mapping(grid)

        
        # register spherical coordinates
        # use rhs underscores to avoid triggering composition 
        self['r'] = 'sqrt(x_**2 + y_**2 + z_**2)'
        self['theta'] = 'pi/2 - asin(z_/r)'
        self['phi'] = 'pi - atan2(y_,x_)'

        # register Cartesian coordinates
        # make sure lhs ordering is r, theta, phi
        self['x(r_, theta_, phi_)'] = 'r_*sin(theta_)*cos(pi - phi_)'
        self['y(r_, theta_, phi_)'] = 'r_*sin(theta_)*sin(pi - phi_)'
        self['z'] = 'r_*sin(pi/2 - theta_)'

        # register cartesian parameters
        self['e_r0__r1_'] = 'e_r0__r1(phi, theta)'
        self['p_r0__r1_'] = 'p_r0__r1(phi, theta)'
        self['t_r0__r1_'] = 't_r0__r1(phi, theta)'
        self['r_r0__r1_'] = 'r_r0__r1(phi, theta)'
        
    def load_mapfl_in(self):
        mapfl_in_path = '{}/{}'.format(self._rundir, self._mapfl_r1_r0_path)
        
        self._mapdir = os.path.dirname(os.path.realpath(mapfl_in_path))
        
        with open(mapfl_in_path) as f:
            f.readline()
            self._mapfl_in = dict()
            for l in f.readlines():
                try:
                    var_, val_ = l.split('=')
                    val_ = val_.strip()
                    if val_ == '.true.':
                        val_ = True
                    elif val_ == '.false.':
                        val_ = False
                    elif val_[0] == "'":
                        val_ = val_.strip("'")
                    else:
                        val_ = float(val_)
                except:
                    continue
                var_ = var_.replace('%', '_')
                self._mapfl_in[var_] = val_
                
    def read_mapping(self, varname):
        fname = '{}/{}'.format(self._mapdir, self._mapfl_in[varname])
        return psihdf.rdhdf(fname)
    
    
    def load_mapping(self):
        map_params = 'rtpekql'
        self._map_data = {}
        for direction in 'fb':
            for param in map_params:
                param_key = param + direction + 'file'
                try:
                    phi, theta, r, mapvar = self.read_mapping(param_key)
                    self._map_data[param_key] = dict(phi = phi, theta = theta, mapvar = mapvar)
                except Exception as m:
                    if self.verbosity > 2:
                        print(m)
                
    def get_interpolator(self, axes, variable, grid = True):
        rgi = RegularGridInterpolator(
            axes.values(), 
            variable,
            bounds_error = False,
            fill_value = self._missing_value)

        if grid:
            def interpolator(rvec):
                """Interpolator as a function of axes"""
                return rgi(rvec)
            return gridify(interpolator, phi_i = axes['phi'], theta_j = axes['theta'])
        else:
            phi_ij, theta_ij = np.meshgrid(axes['phi'], axes['theta'], indexing = 'ij')
            def interpolator(phi_ij = phi_ij, theta_ij = theta_ij):
                """Interpolator as a function of axes"""
                if len(phi_ij.shape) > 1:
                    points = np.column_stack((phi_ij.ravel(), theta_ij.ravel()))
                    if self.verbosity > 0:
                        print('multi-dimensional input to interpolator')
                        print(phi_ij.shape, theta_ij.shape, points.shape)
                        print((phi_ij.min(), phi_ij.max()),(theta_ij.min(), theta_ij.max()))
                    return (rgi(points)).reshape(phi_ij.shape)
                else:
                    if self.verbosity > 0:
                        print('1-d input to interpolator')
                    points = np.vstack((phi_ij,theta_ij)).T
                    return rgi(points)

            return interpolator

    def register_mapping(self, grid):
        for key, mapdict in self._map_data.items():
            map_key = key.split('file')[0]
            if map_key[-1] == 'f':
                map_suffix = '_r0__r1'
            else:
                map_suffix = '_r1__r0'
            axes = {k: mapdict[k] for k in ['phi','theta']}
            self[key[0] + map_suffix] = self.get_interpolator(axes, mapdict['mapvar'], grid)
        