"""
DESCRIPTION:
    LSQR For SLIMpy

    Attempts to solve the least squares problem that minimizes norm(y-A*x)
    if A is inconsistent, otherwise it attemps to solve the system of linear equations A*x=y

    Inputs:
      modelspace -- The space of the model, to generate initial guess.
      maxiter -- Maximum number of iteration for solver.
      tol -- Desired tolerance for solution.
      fastlsqr -- bool to calcualte reside if governed by max tol.
      
      A -- operator object containing a complete 
      y -- vector instance
    Outputs:
      x -- The solution (N vector) to the problem.
"""
import pdb
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

"""
\author          Peyman P. Moghaddam

                 Seismic Laboratory for Imaging and Modeling (SLIM)
                 Department of Earth & Ocean Sciences (EOS)
                 The University of British Columbia at Vancouver (UBC)

\par Acknowledgments: 
                 Deli Wang
                 Seismic Laboratory for Imaging and Modeling (SLIM)
                 Department of Earth & Ocean Sciences (EOS)
                 The University of British Columbia at Vancouver (UBC)

                 C. Brown
                 Seismic Laboratory for Imaging and Modeling (SLIM)
                 Department of Earth & Ocean Sciences (EOS)
                 The University of British Columbia at Vancouver (UBC)

Copyright: You may use this code only under the conditions and terms of
the license contained in the file license.doc, provided with this software.
If you do not agree to these terms you may not use this software.

"""

from slimpy_contrib.ana.utils.AbstractSolver import solver

class LSQRsolver(solver):
    """
    LSQR For SLIMpy

    Attempts to solve the least squares problem that minimizes norm(y-A*x)
    if A is inconsistent, otherwise it attemps to solve the system of linear equations A*x=y
    """
    def __init__(self, modelSpace=None, maxiter=200, tol=1e-6, fastlsqr=True):
        """
        Constructor
        @param modelSpace The space of the model, to generate initial guess.
        @param maxiter Maximum number of iteration for solver.
        @param tol Desired tolerance for solution.
        @param fastlsqr bool to calcualte reside if governed by max tol.
        
        """
        self.modelSpace = modelSpace
        self.maxiter = maxiter
        self.tol = tol
        self.fastlsqr = fastlsqr

    
    def solve(self, A, y):
        """
        @param A -- operator object containing a complete 
        @param y -- vector instance
        \return x The solution (N vector) to the problem.

        """
        #define initial guess.
        if self.modelSpace is None:
            x = A.domain().zeros()
        else:
            x = self.modelSpace.zeros()
        
        beta = y.norm()
        u = y/beta
        v = A.adj()*u
        alpha = v.norm()
        v /= alpha
        w = v
        
        phibar=beta     # constant
        rhobar=alpha    # constant
        
        resid = beta
        counter = 0
        while ((resid>self.tol) and (counter<self.maxiter)):
            counter += 1
        
            u = (A*v)-alpha*u
            beta = u.norm()
            u /= beta
            
            v = (A.adj()*u)-beta*v
            alpha = v.norm()
            v /= alpha
        
            rho = (rhobar**2+beta**2)**.5
            c = rhobar/rho
            s = beta/rho
            
            theta = s*alpha
            rhobar = c*alpha
            phi = c*phibar
            phibar *= -s
            
            x += phi/rho*w
            w = v-theta/rho*w
            
            if not self.fastlsqr:
                r = y-(A*x)
                rT = A.adj()*r
                resid = r.norm()
                resid_mod = rT.norm()
                condMa = rT.max()
                condMi = rT.min()

                print 'inter:', counter

#                pdb.set_trace()

                print '  ||y-Ax||    = %g' %(resid.item())
                print '  ||A^Tr||    = %g' %(resid_mod.item())
                print '  ||A^Tr||inf = %g' %(max(abs(condMa.item()), abs(condMi.item())))
        
        return x

        
        
        
        
