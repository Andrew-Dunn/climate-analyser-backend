#
# Operation Manager
# Author:		Robert Sinn
# Last modified: 17 x10 2014
#
# This file is part of Climate Analyser. The Job Scheduler exists to
# Use Slurm (with the Drmaa Library) to create jobs over multiple
# nodes/servers.
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

import drmaa
import os
import time
import zoo

def resultOut(jobid,serverAddr):
        filename = jobid + '.nc'
        outputLink = "[opendap]"
        outputLink += (serverAddr + "/thredds/catalog/datafiles/outputs/catalog.html?dataset=climateAnalyserStorage/outputs/" + filename)
        outputLink += "[/opendap]"
        outputLink += "[ncfile]"
        outputLink += (serverAddr + "/thredds/fileServer/datafiles/outputs/" + filename)
        outputLink += "[/ncfile]"
        outputLink += "[wms]"
        outputLink += (serverAddr + "/thredds/wms/datafiles/outputs/" + filename + "?service=WMS&version=1.3.0&request=GetCapabilities")
        outputLink += "[/wms]"
        return outputLink


def jobScheduler(conf,inputs,outputs):
	serverFile = open('ThreddServer')
	serverAddr = serverFile.read().strip()
	urls = inputs["urls"]["value"]
	jobType = inputs["selection"]["value"]
	jobId = inputs["jobid"]["value"]

        sess = drmaa.Session()
        sess.initialize()
        # 'Creating job template'
        jt = sess.createJobTemplate()
        jt.remoteCommand = 'python Operation.py'
        jt.args = [urls,jobType,jobId]
	jt.joinFiles = False #Comment out this line for dedugging 
	jt.jobName = jobId
        jid = sess.runJob(jt)
        #'Your job has been submitted with id ' + jobid

	if sess.jobStatus(jid) == 'queued_active':
		outputs["Status"]["value"] = str(0)
	else:
		outputs["Status"]["value"] = str(12)

	sess.deleteJobTemplate(jt)
	sess.exit()

	outputs["Result"]["value"]=(resultOut(jobId,serverAddr))
	return zoo.SERVICE_SUCCEEDED

