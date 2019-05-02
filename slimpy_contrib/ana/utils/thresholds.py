"""
Theshold schemes to pass to landweber solver
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

from slimpy_base.SLIMmath.Steppers import OneDimStepN

class threshobj( object ):
    """
    Base class for the shreshold schemes.
    
    """
    def __init__( self ):
        pass
    
    def choose( self, param=0.007, **kargs ):
        """
        choose must be called with the key word param
        """
        return param
    
#class LinearCooling( threshobj ):
#    """
#    Linear Threshold scheme for landweber
#    """
#    def __init__( self, lambdaMax, lambdaMin, OuterN ):
#        self.lambdaMax = lambdaMax
#        self.lambdaMin = lambdaMin
#        self.OuterN = OuterN
#        self.prev_i = None
#        stepper = OneDimStepN( lambdaMax, lambdaMin, OuterN )
#        self.slist = list(stepper) 
#        self.stepper = self.slist.__iter__()
#        
#        
#    def choose( self, coefs, i, OuterN, **kargs ):
#        """
#        """
#        if self.prev_i != i:
##            print self.prev_i , i
#            self.prev_i = i
#            self.step  =self.stepper.next( )
#            
#        return self.step

class LinearCooling( threshobj ):
    """
    Linear Threshold scheme for landweber
    """
    def __init__( self, lambdaMax, lambdaMin, OuterN ):
        self.lmax = lambdaMax
        self.lmin = lambdaMin
        self.OuterN = OuterN
        self.prev_i = None
        
        
        
#        stepper = OneDimStepN( lambdaMax, lambdaMin, OuterN )
#        self.slist = list(stepper) 
#        self.stepper = self.slist.__iter__()
        
    def init(self,coefs):
        size = coefs.space.get_size( )
        idxstop = int( size*self.lmin )
        idxstart  = int( size*self.lmax )
        idxstep = self.OuterN
        stepper = OneDimStepN( idxstart, idxstop, idxstep )
        
        idxlist = [ int(idx) for idx in stepper ]
        self.idxlist = idxlist
        
        thrlist = [ coefs.orderstat(idx) for idx in idxlist]
        return thrlist
         
        
    def choose( self, coefs, i, OuterN, **kargs ):
        """
        """
        
        
        if self.prev_i is None:
            self.thrlist = self.init(coefs)
            self.thrstep = iter( self.thrlist )
        
        if self.prev_i != i:
            self.prev_i = i
            self.step  = self.thrstep.next( )

        return self.step

