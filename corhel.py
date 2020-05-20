from kamodo import Kamodo, kamodofy, gridify
import psihdf
from scipy.interpolate import RegularGridInterpolator
import os

class Spherical(Kamodo):
    def __init__(self):
        super(Spherical, self).__init__()
        self['r'] = '(x**2 + y**2 + z**2)**(1/2)'
        self['theta'] = 'z/r'
        self['phi'] = 'atan2(y,x)'

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
            return r*np.cos(theta)
        
        self['x(r,theta,phi)'] = x
        self['y(r,theta,phi)'] = y
        self['z(r,theta)'] = z



def get_interpolator(axes, variable):
    rgi = RegularGridInterpolator(axes.values(), variable)
    @gridify(**axes)
    def interpolator(points):
        """Interpolator as a function of axes"""
        return rgi(points)
    return interpolator


class CORHEL_Kamodo(Kamodo):
    def __init__(self,
            rundir,
            mapfl_r1_r0_path = 'cor/mapfl_r1_r0/mapfl.in', 
            verbosity = 0):
        
        self.verbosity = verbosity
        self._rundir = rundir
        self._mapfl_r1_r0_path = mapfl_r1_r0_path
        self._map_data = {}
        
        self.load_mapfl_in()
        self.load_mapping()
    
        super(CORHEL_Kamodo, self).__init__() 
        
        self.register_mapping()
        
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
                
    def register_mapping(self):
        for key, mapdict in self._map_data.items():
            map_key = key.split('file')[0]
            if map_key[-1] == 'f':
                map_suffix = '_r0__r1'
            else:
                map_suffix = '_r1__r0'
            self[key[0] + map_suffix] = get_interpolator({k: mapdict[k] for k in ['phi','theta']}, mapdict['mapvar'])
        