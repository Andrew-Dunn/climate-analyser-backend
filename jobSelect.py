#
# Job Select tool
# Author:		Robert Sinn
# Last modified: 17 10 2014
#
# This file is part of Climate Analyser. By importing the "operators"
# folder, any python file can be used so long as the name is passed
# in and the file contains a run(input[],output[]) function. So long as
# the python file is valid.
#
# Climate Analyser is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Climate Analyser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Climate Analyser.
# If not, see <http://www.gnu.org/licenses/>.
#

import sys
from operators import *
import operators as ops

def jobSelect(op,inputFiles,outputFiles):
	#CDO operators can be called with the prefix "cdo-" by doing so any
	#cdo operator can be used so long as the correct number of files are
	#passed in
	if op.startswith('cdo-'):
		func = ops.cdoOps.cdoOps(op.split('-')[1],inputFiles,outputFiles)
		func(input = ops.cdoOps.cdoCallString(inputFiles)
			,output = ops.cdoOps.cdoCallString(outputFiles))
		return
	
	mod = getattr(ops,op)	#returns operation
	func = getattr(mod,'run')  #returns operation.run
	
	func(inputFiles,outputFiles) #Run selected operation

if __name__ == '__main__':
    exitCode = jobSelect(sys.argv[1],sys.argv[2].split(','),sys.argv[3].split(','))
    exit(exitCode)
