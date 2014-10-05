#
# CDO Operations
# Author:		Robert Sinn
# Last modified: xx xx 2014
#
# This file is part of Climate Analyser.
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
import operators as opps

def checkOpp(operation,option,inputFiles,outputFiles,incount = -1,outcount = -1):
	if option == operation:
		if len(inputFiles) != incount and incount != -1:
			raise Exception("Insufficent input files")
		if len(outputFiles) != outcount and outcount != -1:
			raise Exception("Insufficent output files")
		return 1

	return 0

def jobSelect(opp,inputFiles,outputFiles):
	if opp.startswith('cdo-'):
		func = opps.cdoOpps.cdoOpps(opp.split('-')[1],inputFiles,outputFiles)
		func(input = opps.cdoOpps.cdoCallString(inputFiles)
			,output = opps.cdoOpps.cdoCallString(outputFiles))
		return

	#if checkOpp('correlate',opp,inputFiles,outputFiles,2,1):
	#	func = correlate.run(inputFiles[0],inputFiles[1],outputFiles[0])
	#elif checkOpp('convolute',opp,inputFiles,outputFiles,2,1):
	#	func = convolute.run(inputFiles[0],inputFiles[1],outputFiles[0])
	#else:
	
	mod = getattr(opps,opp)
	func = getattr(mod,'run')
	
	func(inputFiles,outputFiles)

if __name__ == '__main__':
    exitCode = jobSelect(sys.argv[1],sys.argv[2].split(','),sys.argv[3].split(','))
    exit(exitCode)
