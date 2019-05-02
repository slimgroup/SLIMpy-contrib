"""
Sover class for use in ANA
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


from slimpy_base.Environment.InstanceManager import InstanceManager


class solver( object ):
    """
    Abstract class
    """
#    slimvars = GlobalVars()
    env = InstanceManager()
#    log = env['record']
    
    def __init__( self ):
        
        pass
    
    def solve( self, A, x ):
        """
        Not ImplementedError
        """
        raise NotImplementedError( "Must subclass sovler base class" )
    
    def __str__(self):
        return "<SLIMpy abstract solver>"
    
    def __repr__(self):
        return "<SLIMpy abstract solver>"
    