#
# SlurmInfo
# Author:		Robert Sinn
# Last modified: 20 10 2014
#
# Get Feedback from slurm via Zoo Calls
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

import subprocess
import os
import zoo

def callCommand(option):
	#Call slurm commands and return output.
	ret = subprocess.Popen([option], stdout=subprocess.PIPE)
	return ret.communicate()[0] + '\n'

def slurmInfo(conf,inputs,outputs):
        option = inputs["option"]["value"]
	slurmOut = ''
        if option == 'sinfo' or option == 'sall':
		slurmOut += callCommand('sinfo -N -l')
	if option == 'squeue' or option == 'sall':
		slurmOut += callCommand('squeue')
	if option == 'snodes' or option == 'sall':
		slurmOut += callCommand('scontrol -o show nodes')
	outputs["Result"]["value"] = slurmOut
	return zoo.SERVICE_SUCCEEDED
        
if __name__ == '__main__':
        slurmInfo()

