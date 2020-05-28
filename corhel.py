from kamodo import Kamodo, kamodofy, gridify, get_defaults
import psihdf
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import os, re
import matplotlib.pyplot as plt
import forge

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


        self['xhat'] = lambda s: np.array([s, 0, 0])
        self['yhat'] = lambda s: np.array([0, s, 0])
        self['zhat'] = lambda s: np.array([0, 0, s])
        self['rhat(phi, theta, s)'] = 'sin(theta)*cos(phi)*xhat + sin(theta)*sin(phi)*yhat + cos(theta)*zhat'
        self['thetahat(phi, theta, s)'] = 'cos(theta)*cos(phi)*xhat + cos(theta)*sin(phi)*yhat - sin(theta)*zhat'
        self['phihat(phi, s)'] = '-sin(phi)*xhat + cos(phi)*yhat'
        self['Avec(A_phi, A_theta, A_r, phi, theta)'] = 'A_r*rhat(phi, theta, 1)+A_theta*thetahat(phi, theta, 1)+A_phi*phihat(phi, 1)'

        self['r'] = 'sqrt(x**2 + y**2 + z**2)'
        self['theta'] = 'pi/2 - asin(z/r)'
        self['phi'] = 'pi - atan2(y,x)'


        

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
        self['x(r,theta, phi)'] = 'r*sin(theta)*cos(phi)'
        self['y(r,theta, phi)'] = 'r*sin(theta)*sin(phi)'
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
            imas_path = 'cor/mhd/imas',
            verbosity = 0,
            steps = [-1],
            missing_value = np.nan, **kwargs):

        
        self.verbosity = verbosity
        self._rundir = rundir
        self._mapfl_r1_r0_path = mapfl_r1_r0_path
        self._imas_path = imas_path
        self._imas = {}
        self._map_data = {}
        self._mas_data = {}
        self._missing_value = missing_value
        self._steps = steps
        self.load_mapfl_in()
        self.load_mapping()

        self.load_imas()
        self.register_mas_files()
        self.load_mas()

        self._mas_names = dict(
            bp = 'b_phi',
            bt = 'b_theta',
            br = 'b_r',
            jp = 'j_phi',
            jt = 'j_theta',
            jr = 'b_r',
            vp = 'v_phi',
            vt = 'v_theta',
            vr = 'v_r',
            )
    
        super(CORHEL_Kamodo, self).__init__(**kwargs)
        
        self.register_mapping()
        self.register_mas()
        
        # # register spherical coordinates
        # # use rhs underscores to avoid triggering composition 
        # self['r'] = 'sqrt(x_**2 + y_**2 + z_**2)'
        # self['theta'] = 'pi/2 - asin(z_/r)'
        # self['phi'] = 'pi - atan2(y_,x_)'

        # # register Cartesian coordinates
        # # make sure lhs ordering is r, theta, phi
        # self['x(r_, theta_, phi_)'] = 'r_*sin(theta_)*cos(pi - phi_)'
        # self['y(r_, theta_, phi_)'] = 'r_*sin(theta_)*sin(pi - phi_)'
        # self['z'] = 'r_*sin(pi/2 - theta_)'

        # # # register cartesian parameters
        # # self['e_r0__r1_'] = 'e_r0__r1(phi, theta)'
        # # self['p_r0__r1_'] = 'p_r0__r1(phi, theta)'
        # # self['t_r0__r1_'] = 't_r0__r1(phi, theta)'
        # # self['r_r0__r1_'] = 'r_r0__r1(phi, theta)'


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

    def load_imas(self):
        """Load the imas file"""
        imas_path = '{}/{}'.format(self._rundir, self._imas_path)
        self._mhddir = os.path.dirname(os.path.realpath(imas_path))

        with open(imas_path) as f:
            while True:
                l = f.readline()
                if len(l) == 0:
                    break
                if l[0] != '!':
                    if l.strip()[-1] == ',':
                        l = l.strip() + f.readline().strip()
                    try: 
                        var, val = [x.strip() for x in l.split('=')]
                        if val == '.true.':
                            val = True
                        elif val == '.false.':
                            val = False
                        elif val[0] == "'":
                            if ',' in val:
                                val = [v.strip("'") for v in val.split(',')]
                            else:
                                val = val.strip("'")
                        elif ',' in val:
                            val = [float(v) for v in val.split(',')]
                        elif '.' in val:
                            val = float(val)
                        else:
                            val = int(val)
                        self._imas[var] = val
                    except:
                        continue
        
    def register_mas_files(self):
        """Register all files in imas plotlist"""
        mas_files = dict()
        for varname in self._imas['plotlist']:
            var_files = []
            for filename in os.listdir(self._mhddir):
                if 'potfld' in filename:
                    continue
                if filename.startswith(varname) & \
                    filename.endswith('.hdf') & \
                    (re.search("\d+", filename) is not None):
                        var_files.append(filename)
            var_files.sort()
            mas_files[varname] = var_files

        self._mas_files = mas_files


    def load_mas(self):
        """Load all regitstered MAS files"""
        for varname, files in self._mas_files.items():
            for file in [files[i] for i in self._steps]:
                # parse the step from file names like br001.hdf
                step = int(file.split(varname)[-1].split('.hdf')[0])
                if len(self._steps) == 1:
                    regname = varname
                else:
                    regname = '{}_{}'.format(varname, step) 
                fname = '{}/{}'.format(self._mhddir, file)
                try:
                    phi, theta, r, masvar = psihdf.rdhdf(fname)
                    self._mas_data[regname] = dict(
                        phi = phi, 
                        theta = theta, 
                        r = r, 
                        masvar = masvar)
                except Exception as m:
                    print('could not register {}'.format(regname))
                    print(m)



            
    def get_interpolator(self, axes, variable):
        rgi = RegularGridInterpolator(
            axes.values(), 
            variable,
            bounds_error = False,
            fill_value = self._missing_value)

        if len(axes) == 2:
            @gridify(phi_i = axes['phi'], theta_j = axes['theta'])
            def grid_interpolator(rvec):
                """Interpolator as a function of axes"""
                return rgi(rvec)

            # phi_ij, theta_ij = np.meshgrid(axes['phi'], axes['theta'], indexing = 'ij')
            def interpolator(phi = axes['phi'], theta = axes['theta']):
                """Interpolator as a function of phi, theta"""
                if len(phi.shape) > 1:
                    points = np.column_stack((phi.ravel(), theta.ravel()))
                    return (rgi(points)).reshape(phi.shape)
                else:
                    return grid_interpolator(phi, theta)
        elif len(axes) == 3:
            @gridify(phi_i = axes['phi'], theta_j = axes['theta'], r_k = axes['r'])
            def grid_interpolator(rvec):
                """Interpolator as a function of axes"""
                return rgi(rvec)

            # phi_ij, theta_ij = np.meshgrid(axes['phi'], axes['theta'], indexing = 'ij')
            def interpolator(phi = axes['phi'], theta = axes['theta'], r = axes['r']):
                """Interpolator as a function of phi, theta"""
                if len(np.array(phi).shape) > 1:
                    points = np.column_stack((phi.ravel(), theta.ravel(), r.ravel()))
                    return (rgi(points)).reshape(phi.shape)
                else:
                    return grid_interpolator(phi, theta, r)
        else:
            print('cannot handle axes')


        return kamodofy(interpolator)

    def register_mapping(self):
        for key, mapdict in self._map_data.items():
            map_key = key.split('file')[0]
            if map_key[-1] == 'f':
                map_suffix = '_r0__r1'
            else:
                map_suffix = '_r1__r0'
            axes = {k: mapdict[k] for k in ['phi','theta']}
            self[key[0] + map_suffix] = self.get_interpolator(axes, mapdict['mapvar'])
            # self[key[0] + map_suffix] = self.get_cartesian_mapping(axes, mapdict['mapvar'])
    

    def get_cartesian_mapping(self, axes, mapvar):
        cartesian = Cartesian()
        interpolator = self.get_interpolator(axes, mapvar)

        def cart_interpolator(phi = axes['phi'], theta = axes['theta'], r = 1.0):
            pp, tt = [np.squeeze(ar) for ar in np.meshgrid(phi, theta)]

            def sph_to_cart(x = cartesian.x(r, tt, pp),
                            y = cartesian.y(r, tt, pp),
                            z = cartesian.z(r, tt)):
                return np.squeeze(interpolator(pp, tt))
            yield kamodofy(sph_to_cart)
        return cart_interpolator

    def get_cartesian(self, axes, masvar, regname):
        """Create an interpolator that yields cartesian signature"""
        cartesian = Cartesian()
        interpolator = self.get_interpolator(axes, masvar)

        def cart_interpolator(phi = axes['phi'], theta = axes['theta'], r = axes['r']):
            rr, tt, pp = [np.squeeze(ar) for ar in np.meshgrid(r, theta, phi)]
            
            def sph_to_cart(x = cartesian.x(rr, tt, pp),
                            y = cartesian.y(rr, tt, pp),
                            z = cartesian.z(rr, tt)):
                return np.squeeze(interpolator(pp, tt, rr))
            sph_to_cart.__name__ = regname
            yield kamodofy(sph_to_cart)
        return cart_interpolator


    def register_mas(self):
        """Register all loaded MAS variables"""
        for varname, masdict in self._mas_data.items():
            axes = {k: masdict[k] for k in ['phi', 'theta', 'r']}
            regname = self._mas_names.get(varname, varname)
            self[regname] = self.get_interpolator(axes, masdict['masvar'])
            # self[regname] = self.get_cartesian(axes, masdict['masvar'], regname)


    def contour(self, varname, **args):
        defaults = get_defaults(self[varname])
        for arg, vals in args.items():
            defaults[arg] = vals
        result = self[varname](**defaults)
        c_0 = np.linspace(result.min(), result.max(), 30)
        new_defaults = {}
        for k, v in defaults.items():
            if k not in args:
                new_defaults[k] = v
        x_i, y_j = new_defaults.values()
        new_params = list(new_defaults.keys())
        def var_contour(c_0 = c_0):
            if not hasattr(c_0, '__iter__'):
                c_0 = [c_0]
            try:
                try:
                    t, c1, c2 = get_contours(x_i = x_i, y_j = y_j, m_ij = result, c_vals = c_0)
                except:
                    t, c1, c2 = get_contours(x_i = x_i, y_j = y_j, m_ij = result.T, c_vals = c_0)
            except:
                print('could not generate contours')
                print('x_i {}, y_j {}, m_ij {}'.format(x_i.shape, y_j.shape, result.shape))
                raise
            @forge.sign(forge.arg(new_params[0], default = c1),
                        forge.arg(new_params[1], default = c2))
            def contour_lambda(**kwargs):
                return t
            
            yield kamodofy(contour_lambda)
        return var_contour
