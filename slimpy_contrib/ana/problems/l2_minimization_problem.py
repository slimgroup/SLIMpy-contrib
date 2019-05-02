"""
@package slimpy_contrib.problems.l2_minimization_problem
@brief basic l1 minimisaton problem
@detail
This package defines a basic l1 minimisaton problem
to be solved by the SLIMpy/SCons 
\ref slimproj_core.builders.NewSolve.SolveBuilder "Solve Builder"

@par Example
@code
from slimproj import *
# build 'res.rsf' from 'data.rsf'
Solve( 'res', 'data', OuterN=4, log='dnoise.log', problem=l2_min_problem ) 
@endcode

@author Sean Ross-Ross
"""

from slimpy_contrib.ana.lsqr import LSQRsolver
from slimpy_base.utils.slim_decorators import depends_on
from SLIMpy.linear_operators import Identity

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

#===============================================================================
# set parameters to tell sconss when to update 
#===============================================================================

Get = lambda env, item: env.get( item ) or env.get( 'problem', env.get('default_pack',{})).get(item) 

@depends_on( 'maxiter', 'tol' )
@depends_on( 'fastlsqr' )
def solver_callback( target, source, env, A ):
    """
    solver_callback( target, source, env, space ) -> Solver
    Set the default value for the solver.
    \param A not used but kept for compatibility 
    """
    
    maxiter =       Get( env,'maxiter' )
    tol =           Get( env,'tol'  )
    fastlsqr =      Get( env,'fastlsqr' ) 
    
    solver = LSQRsolver( maxiter=maxiter, tol=tol, fastlsqr=fastlsqr )
    return solver



def precondition_callback( t,s,e, space ):
    return Identity( space )



l2_min_problem = {}
l2_min_problem['name'] = 'l_2 Minimization Problem'
l2_min_problem['doc'] = { }


l2_min_problem['solver_callback'] = solver_callback
l2_min_problem['precondition_callback'] = precondition_callback

l2_min_problem['maxiter'] = 200
l2_min_problem['doc']['maxiter']  = """
        Maximum number of iteration for solver.
"""
l2_min_problem['tol'] = 1e-6
l2_min_problem['doc']['tol']  = """
        Desired tolerance for solution.
"""

l2_min_problem['fastlsqr'] = False
l2_min_problem['doc']['fastlsqr']  = """
        bool to calcualte reside if governed by max tol.

"""



