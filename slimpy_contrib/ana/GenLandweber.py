"""

TODO ..
Document the landweber method 
a bit more.


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

"""
You may use this code only under the conditions and terms of the
license contained in the file LICENSE provided with this source
code. If you do not agree to these terms you may not use this
software.

Sean Ross-Ross
"""


from slimpy_base.SLIMmath.Steppers import OneDimStep1
from SLIMpy.linear_operators import Identity

from slimpy_contrib.ana.utils.AbstractSolver import solver
from itertools import chain


class GenThreshLandweber(solver):

    """
    --latex
    Generalized Thresholded Landweber method using vector and linear operator commands.
    
    Parameters:
    \\begin{description}
        \\item 
            A: operator object containing a complete 
            definition of forward operator and the adjoint operator
        \\item 
            lambdaMax: maximum lambda
        \\item 
            lambdaMin: minimum lambda
        \\item
            lambdaN: number of steps in iteration from lambdaMax to lambdaMin
        \\item
            InnerN: number of iterations for any lambda
        \\item
            data: vector instance
        \\item
            VERBOSE: verbose if set to True
    \\end{description}

    Bugs:
        None so far, but keep trying.
        It is not fool-proof. So, you have to know what you are doing;
        i.e., how to use RSF.
    """
    def __init__( self, OuterN, InnerN, thresh, Update=None, x0=None ):
        self.OuterN = OuterN
        self.InnerN = InnerN

        self.thresh = thresh
        self.Update = Update
        self.x0 = x0
    
    def __repr__(self):
        name = self.__class__.__name__
        res1 = [repr( getattr(self,attr) ) for attr in ['OuterN','InnerN','thresh'] ]
        res2 = [ "%s=%s"%(attr,repr( getattr(self,attr) )) for attr in ['Update', 'x0'] ] 
        res = ", ".join( chain(res1,res2) )
        return name + "( %(res)s )" %vars()
        
    def solve(self, A, b ):
        
        log = self.env['record'](2,'solver')

        print >> log ,'Into GenThreshLandweber'
        
        # pre-computation of matched filter    
        At_b = A.adj() * b


        # prepare first guess
        print >> log , 'Initial guess:'
        
        if self.x0 is None:
            x = A.domain().zeros()
        else:
            x = self.x0
        
        if self.Update is None:
            U = Identity( A.range() )
        else:
            U = self.Update
            

        for i in OneDimStep1(1,self.OuterN):
            for j in OneDimStep1(1,self.InnerN):
                
                
                Ax = A*x
                
                At_Ax = A.adj() * Ax
                
                At_b_x = At_b - At_Ax
                
                xTmp = U * At_b_x + x
                
                thr = self.thresh.choose(data=x,coefs=At_b,i=i,OuterN=self.OuterN,j=j,InnerN=self.InnerN)
                
                x = xTmp.thr(thr)
                
        
        print >> log ,'Out off GenThreshLandweber '
        return x

        
