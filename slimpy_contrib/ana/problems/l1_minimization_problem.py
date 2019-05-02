"""
Perform 2D de-noiseing using landweber method.

@note that, as of August 28, 2006:
 - dimension fixed (2D)

@par REQUIREMENTS:
- Madagascar with SLIM toolbox
- SLIMpy
    
@param    lmax  [Default=0.01]
@param    lmax    [Default=0.6]
@param    nouter Number of outer loops [Default=2]
@param    ninner Number of inner loops [Default=2]
"""

__copyright__ = """
Copyright 2008 Sean Ross-Ross
"""

__license__ =  """
This file is part of SLIMpy .

SLIMpy is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SLIMpy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with SLIMpy . If not, see <http://www.gnu.org/licenses/>.
"""



from SLIMpy import vector
from SLIMpy.linear_operators import surf, Identity
from slimpy_base.utils.slim_decorators import depends_on
from slimpy_contrib.ana.GenLandweber import GenThreshLandweber
from slimpy_contrib.ana.utils.thresholds import LinearCooling


__acknowledgments__ = """
Author:         G. Hennenfent
                Seismic Laboratory for Imaging and Modeling (SLIM)
                Department of Earth & Ocean Sciences (EOS)
                The University of British Columbia at Vancouver (UBC)

Acknowledgments: 
                Sean Ross-Ross
                Seismic Laboratory for Imaging and Modeling (SLIM)
                Department of Earth & Ocean Sciences (EOS)
                The University of British Columbia at Vancouver (UBC)

                Darren Thomson
                Seismic Laboratory for Imaging and Modeling (SLIM)
                Department of Earth & Ocean Sciences (EOS)
                The University of British Columbia at Vancouver (UBC)

Funding:        This work was carried out as part of the SINBAD project with
                financial support, secured through ITF, from the following
                organizations: BG Group, BP, Chevron, ExxonMobil, and Shell. SINBAD is
                part of a collaborative research and development grant (CRD) number
                334810-05 funded by the Natural Science and Engineering Research
                Council (NSERC)

"""



Get = lambda env, item: env.get( item ) or env.get( 'problem', env.get('default_pack',{}) ).get(item)


@depends_on( 'lmax', 'lmin' )
@depends_on( 'nouter', 'ninner' )
def solver_callback( target, source, env, A ):
    """
    solver_callback( target, source, env, space ) -> Solver
    Set the default value for the solver. Solver defaults 
    to the thresholded landweber with a linear cooling 
    threshold scheme.
    @return Thresholded Landweber Solver with LinearCooling scheme
    """
    
    space = A.domain()
    
    lambdaMax = Get( env,'lmax' )
    lambdaMin = Get( env,'lmin'  )
    outer = int( Get( env,'nouter' ) )
    inner = int( Get( env,'ninner'  ) )
    
    thresh = LinearCooling( float( lambdaMax ), float( lambdaMin ), outer )
    I = Identity( space )
    
    
    x0 = env.get( 'x0' , None )
    if x0 is None:
        x0 = space.zeros()
    else:
        x0 = vector( x0  )
    
    solver = GenThreshLandweber( outer, inner, thresh, I, x0 )
    
    return solver



def precondition_callback(target,source,env, space ):
    """
    precondition_callback(target,source,env, space) -> Identity(space)
    Default preconditioner defaults to the Identity 
    """
    return Identity(space)


l1_min = {}
l1_min['name'] = 'l1 minimizeation with landweber method'
l1_min['doc'] = { }

l1_min['precondition_callback'] = precondition_callback
l1_min['solver_callback'] = solver_callback

l1_min['lmax'] = .01
l1_min['doc']['lmax']  = """
        This parameter must be greater 
        than lmin. The closer lmax is to 0 the more
        acurate your result will be, if the solver has 
        enough iterations. A larger value, 
        however your results will be less acurate.
"""
l1_min['lmin'] = .60
l1_min['doc']['lmin']  = """
        The closer the 
        parameter is to 0 the more noise and signal is kept in the 
        result as lmin increases more noise will be removed. 
"""
l1_min['nouter'] = 2
l1_min['doc']['nouter']  = """
        number of outer iterations for the solver
"""
l1_min['ninner'] = 2
l1_min['doc']['ninner']  = """
        number of inner iterations for the solver
"""
l1_min['x0'] = None
l1_min['doc']['x0']  = """
        initial guess. x0 must be a vector in the domain of the result of the operator returned by transfrom callback
"""






