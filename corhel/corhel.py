from kamodo import Kamodo, kamodofy, gridify, get_defaults
from corhel import psihdf
from scipy.interpolate import RegularGridInterpolator
import numpy as np
import os, re
import matplotlib.pyplot as plt
import forge
import mcubes
import json

class Spherical(Kamodo):
    def __init__(self,
        x=np.linspace(-1, 1, 100),
        y=np.linspace(-1, 1, 100),
        z=np.array([1])):
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
        self['phi'] = 'mod(atan2(y,x), 2*pi)'



class Cartesian(Kamodo):
    def __init__(self,
                 r=np.array([1]),
                 theta=np.linspace(0, np.pi, 180),
                 phi=np.linspace(0, 2*np.pi, 360),
                 gridify_interpolators=True):
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

        self['z(r,theta)'] = 'r*sin(pi/2 - theta)'
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
                 mapfl_r1_r0_path='cor/mapfl_r1_r0/mapfl.in',
                 mhd_path='cor/mhd',
                 verbosity=0,
                 steps=(-1,),
                 missing_value=np.nan,
                 cartesian=False,
                 variables=None,
                 view_file='view_info.json',
                 gridify_interpolators=True,
                 **kwargs):

        self.verbosity = verbosity
        self._rundir = rundir
        self._mapfl_r1_r0_path = mapfl_r1_r0_path
        self._mhd_path = mhd_path
        self._imas = {}
        self._map_data = {}
        self._mas_data = {}
        self._missing_value = missing_value
        self._steps = steps
        self._cartesian = cartesian
        self._variables = variables
        self._view_file = view_file
        self._flux_rope_view = self.load_view()
        self._gridify = gridify_interpolators
        self.load_mapfl_in()
        self.load_mapping()

        self.load_imas()
        self.register_mas_files()
        self.load_mas()

        self._mas_names = dict(
            bp='b_phi',
            bt='b_theta',
            br='b_r',
            jp='j_phi',
            jt='j_theta',
            jr='b_r',
            vp='v_phi',
            vt='v_theta',
            vr='v_r',
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

    def load_view(self):
        """loads flux rope view information from mhd_path"""
        if self._view_file is not None:
            view_file = "{}/{}/{}".format(self._rundir, self._mhd_path, self._view_file)
            if os.path.exists(view_file):
                with open(view_file) as view:
                    return json.load(view)

    def load_mapfl_in(self):
        mapfl_in_path = '{}/{}'.format(self._rundir, self._mapfl_r1_r0_path)


        self._mapdir = os.path.dirname(os.path.realpath(mapfl_in_path))

        if os.path.exists(mapfl_in_path):
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
        """read mapping data from file"""
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
                    self._map_data[param_key] = dict(phi=phi, theta=theta, mapvar=mapvar)
                except Exception as m:
                    if self.verbosity > 2:
                        print(m)

    def load_imas(self):
        """Load the imas file"""
        imas_path = '{}/{}/imas'.format(self._rundir, self._mhd_path)
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
                if '_' in filename: #occurs when vis slices end up in mhddir
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
        if self._variables is not None:
            variables = self._variables
        else:
            variables = self._mas_files.keys()

        for varname in variables:
            try:
                files = self._mas_files[varname]
            except KeyError:
                raise KeyError('{} not found. Available fields: {}'.format(varname, list(self._mas_files.keys())))
            for file in [files[i] for i in self._steps]:
                # parse the step from file names like br001.hdf
                try:
                    step = int(file.split(varname)[-1].split('.hdf')[0])
                except:
                    print('issue with varname {}, file: {}, skipping'.format(varname, file))
                    pass
                if len(self._steps) == 1:
                    regname = varname
                else:
                    regname = '{}_{}'.format(varname, step)
                fname = '{}/{}'.format(self._mhddir, file)
                try:
                    phi, theta, r, masvar = psihdf.rdhdf(fname)
                    self._mas_data[regname] = dict(
                        phi=phi,
                        theta=theta,
                        r=r,
                        masvar=masvar)
                except Exception as m:
                    print('could not register {}'.format(regname))
                    print(m)


    def get_interpolator(self, axes, variable):
        rgi = RegularGridInterpolator(
            axes.values(),
            variable,
            bounds_error=False,
            fill_value=self._missing_value)

        if len(axes) == 2:
            if self._gridify:
                @gridify(phi_i=axes['phi'], theta_j=axes['theta'])
                def grid_interpolator(rvec):
                    """Interpolator as a function of axes"""
                    return rgi(rvec)
            else:
                def grid_interpolator(rvec):
                    """Interpolator as a function of axes"""
                    points = np.column_stack((phi.ravel(), theta.ravel()))
                    return rgi(points)


            # phi_ij, theta_ij=np.meshgrid(axes['phi'], axes['theta'], indexing='ij')
            def interpolator(phi=axes['phi'], theta=axes['theta']):
                """Interpolator as a function of phi, theta"""
                if len(phi.shape) > 1:
                    points = np.column_stack((phi.ravel(), theta.ravel()))
                    return (rgi(points)).reshape(phi.shape)
                else:
                    return grid_interpolator(phi, theta)

        elif len(axes) == 3:

            if self._gridify:
                @gridify(phi_i = axes['phi'], theta_j = axes['theta'], r_k = axes['r'])
                def grid_interpolator(rvec):
                    """Interpolator as a function of axes"""
                    # num_size_1 = [np.size(ptr_) for ptr_ in (phi_i, theta_j, r_k)].count((1,))
                    result = rgi(rvec)
                    return result
            else:
                def grid_interpolator(phi, theta, r):
                    """Interpolator as a function of axes"""
                    # num_size_1 = [np.size(ptr_) for ptr_ in (phi_i, theta_j, r_k)].count((1,))
                    points = np.column_stack((phi.ravel(), theta.ravel(), r.ravel()))
                    result = rgi(points)
                    return result

            # phi_ij, theta_ij = np.meshgrid(axes['phi'], axes['theta'], indexing = 'ij')
            # def interpolator(phi = axes['phi'], theta = axes['theta'], r = axes['r']):
            def interpolator(phi = axes['phi'], theta = axes['theta'], r = axes['r'][0]):
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
            axes = {k: mapdict[k] for k in ['phi', 'theta']}
            if self._cartesian:
                self[key[0] + map_suffix] = self.get_cartesian_mapping(axes, mapdict['mapvar'])
            else:
                self[key[0] + map_suffix] = self.get_interpolator(axes, mapdict['mapvar'])


    def get_cartesian_mapping(self, axes, mapvar):
        cartesian = Cartesian()
        # spherical = Spherical()
        interpolator = self.get_interpolator(axes, mapvar)

        def cart_interpolator(phi = axes['phi'], theta = axes['theta'], r = 1.0):
            pp, tt = [np.squeeze(ar) for ar in np.meshgrid(phi, theta)]

            def sph_to_cart(x=cartesian.x(r, tt, pp),
                            y=cartesian.y(r, tt, pp),
                            z=cartesian.z(r, tt)):
                # pp_ = spherical.phi(x, y)
                # tt_ = spherical.theta(x, y, z)
                return np.squeeze(interpolator(pp, tt))
            yield kamodofy(sph_to_cart)

        return cart_interpolator

    def get_cartesian(self, axes, masvar, regname):
        """Create an interpolator that yields cartesian signature"""
        cartesian = Cartesian()
        # spherical = Spherical()
        interpolator = self.get_interpolator(axes, masvar)

        def cart_interpolator(
            phi=axes['phi'],
            theta=axes['theta'],
            r=axes['r'][[0, -1]]):
            rr, tt, pp = [np.squeeze(ar) for ar in np.meshgrid(r, theta, phi)]

            def sph_to_cart(x=cartesian.x(rr, tt, pp),
                            y=cartesian.y(rr, tt, pp),
                            z=cartesian.z(rr, tt)):
                # rr_ = spherical.r(x, y, z)
                # pp_ = spherical.phi(x, y)
                # tt_ = spherical.theta(x, y, z)
                return np.squeeze(interpolator(pp, tt, rr))
            sph_to_cart.__name__ = regname
            yield kamodofy(sph_to_cart)
        return cart_interpolator


    def register_mas(self):
        """Register all loaded MAS variables"""
        for varname, masdict in self._mas_data.items():
            axes = {k: masdict[k] for k in ['phi', 'theta', 'r']}
            regname = self._mas_names.get(varname, varname)
            try:
                self[regname] = self.get_interpolator(axes, masdict['masvar'])
            except ValueError as error_msg:
                print("could not register {}: {}".format(regname, error_msg))

            if self._cartesian:
                self[regname] = kamodofy(self.get_cartesian(axes, masdict['masvar'], regname))

        self['b_r__c'] = self.br_iso


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

    @kamodofy
    def br_iso(self, c = 0):
        phi = self._mas_data['br']['phi']
        theta = self._mas_data['br']['theta']
        r = self._mas_data['br']['r']
        br = self._mas_data['br']['masvar']

        # br[nphi, ntheta, nr]
        # X, Y, Z = np.mgrid[:len(phi), :len(theta), :len(r)] # order?
        vertices, triangles = mcubes.marching_cubes(br, c)
        phi_, theta_, r_ = vertices.T

        phi_ = np.interp(phi_, range(len(phi)), phi)
        theta_ = np.interp(theta_, range(len(theta)), theta)
        r_ = np.interp(r_, range(len(r)), r)

        cartesian = Cartesian()

        x = cartesian.x(r_, theta_, phi_)
        y = cartesian.y(r_, theta_, phi_)
        z = cartesian.z(r_, theta_)

        @kamodofy
        def isosurface(x=x, y=y, z=z):
            return triangles

        yield isosurface

    def get_tracer(self):
        # get fields once
        from scipy.integrate import solve_ivp
        from scipy.interpolate import interp1d
        from collections import defaultdict

        b_r = self.b_r
        b_theta = self.b_theta
        b_phi = self.b_phi

        def bvec(r, theta, phi):
            br_ = b_r(phi, theta, r)
            btheta_ = b_theta(phi, theta, r)
            bphi_ = b_phi(phi, theta, r)
            return np.hstack([br_, btheta_, bphi_])

        def bhat_plus(s, rvec):
            r, theta, phi = rvec
            phi = np.mod(phi, 2*np.pi)
            theta = np.mod(theta, np.pi)
            result = bvec(r, theta, phi)
            result /= np.linalg.norm(result)
        #     print(result)
            return result

        def bhat_minus(s, rvec):
            r, theta, phi = rvec
            phi = np.mod(phi, 2*np.pi)
            theta = np.mod(theta, np.pi)
            result = bvec(r, theta, phi)
            result *= -1.0
            result /= np.linalg.norm(result)
        #     print(result)
            return result

        def boundary(s, rvec):
            if np.isnan(rvec).any() == np.nan:
                return -1
            return 2.0*((1 < rvec[0] < 30) - .5)
        boundary.terminal = True


        cartesian = Cartesian()
        spherical = Spherical()

        r_sph = spherical.r
        theta_sph = spherical.theta
        phi_sph = spherical.phi

        x_cart = cartesian.x
        y_cart = cartesian.y
        z_cart = cartesian.z

        solns = defaultdict(dict)
        bhat = dict()
        bhat['forward'] = bhat_plus
        bhat['reverse'] = bhat_minus

        @kamodofy(hidden_args=['interval', 'res'])
        def f(xvec, interval=(0, 50), res=50):
            for (x_, y_, z_) in xvec:
                point = np.array([r_sph(x_, y_, z_), theta_sph(x_, y_, z_), phi_sph(x_, y_)])
                for direction in 'forward', 'reverse':
                    # print('solving')
                    result = solve_ivp(bhat[direction],
                                       interval,
                                       point,
                                       dense_output=True,
                                       events=boundary,
                                       vectorized=True,
                                       first_step=.001,
                                       # t_eval=np.linspace(*interval, num=res),
                                       # min_step=.0001,
                                       # max_step=10,
                                      )
                    # print('solved')
                    t, t_id = np.unique(np.round(result['t'], 4), return_index=True)
                    # y = result['y'].T[t_id]

                    soln = result['sol']
                    # s = np.linspace(t[0],t[-1], num=50)
                    try:
                        t = interp1d(np.linspace(0, 1, len(t)), t)(np.linspace(0, 1, num=res))
                    except:
                        print(result)
                        raise
                    if len(result['t_events']) > 0:
                        # print(result['t_events'])
                        if len(result['t_events'][0]) > 0:
                            tend = result['t_events'][0][0]
                            t = np.linspace(interval[0], tend, 50)

   
                    # f_b_interp = interp1d(t, y.T)
                    @kamodofy
                    def f_B(s=t):
                        # r, theta, phi = f_b_interp(s)
                        r, theta, phi = soln(s)
                        r[r>30] = np.nan
                        r[r<1] = np.nan
                        x = x_cart(r, theta, phi)
                        z = z_cart(r, theta)
                        y = y_cart(r, theta, phi)
                        return np.vstack([x, y, z]).T
                    yield f_B

        return f

    # def bvec(self, x,y,z):
    #     interpolator = self.get_interpolator(axes, masvar)

    #     get_interpolator

    #     for varname, masdict in self._mas_data.items():
    #         axes = {k: masdict[k] for k in ['phi', 'theta', 'r']}
    #         regname = self._mas_names.get(varname, varname)
    #         try:
    #             self[regname] = self.get_interpolator(axes, masdict['masvar'])
    #         except ValueError as error_msg:
    #             print("could not register {}: {}".format(regname, error_msg))

    #         if self._cartesian:
    #             self[regname] = self.get_cartesian(axes, masdict['masvar'], regname)

    #     self['b_r__c'] = self.br_iso


