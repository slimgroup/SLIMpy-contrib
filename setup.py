"""
Contributions to SLIMpy

"""

from distutils.core import setup

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


packages = [
            'slimpy_contrib',
            'slimpy_contrib.ana',
            'slimpy_contrib.ana.utils',
            'slimpy_contrib.ana.problems',
            'slimpy_contrib.functions',
            'slimpy_contrib.linear_operators',
            ]

setup(
      name='SLIMpy-Contrib',
      version='0.1',
      description='SLIMpy User Contributions to SLIMpy',
      author = "Sean Ross-Ross",
      author_email='srossross@gmail.com',
      url='http://slim.eos.ubc.ca/SLIMpy' ,
      
      packages = packages,
     )

