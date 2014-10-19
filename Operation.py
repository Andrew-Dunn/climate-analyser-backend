#
# Operation Manager
# Author:		Robert Sinn
# Last modified: 20 10 2014
#
# This file is part of Climate Analyser. The Operation script runs the
# encompassing process that sets up the relevant files. Checks for
# duplicates, sets the job status for the Django server and passes the
# Job over to the Job Selector
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
import requests
import jobSelect
import os.path
import os
import string
import random
import rsa
import urllib
import base64
import re

from cdo import *

def getFileNameFromInput(inputFile):
	#Excludes variables from name
	return inputFile.split('?',1)[0]

def getLocation(inputFile):
	return ("/var/www/cgi-bin/Thredds/inputs/" 
							+ getFileNameFromInput(inputFile))

def dataLink(serverAddr,inputFile):
	#Creates a opendap url including relevant variables.
	loc = (serverAddr + "/thredds/dodsC/datafiles/inputs/" + 
						getFileNameFromInput(inputFile))
	return (loc + getVariables(loc+'.dds', inputFile))

def getVariables(loc,inputFile):
	if "?" in inputFile:
		return "?" + ddsVariables(loc,inputFile.split('?',1)[1].split(','))
	else:
		return ""

def ddsVariables(url,grids):
	#get all Maps associated with grids
        vars = []
        output = urllib.urlopen(url).read()
        for grid in grids:
                vars += varSearch(grid,output)
        return ','.join(list(set(vars + grids)))

def varSearch(grid,output):
        varstring = re.search(grid+'(.*);',output).group(1)
        varstring = varstring.strip('[').strip(']')
        return arrayScrub(varstring.split(']['))

def arrayScrub(inputs):
        for x in range(0, len(inputs)):
                inputs[x] = inputs[x].split(' = ')[0]
        return inputs

def compileVarArray(serverAddr,inputs):
	#Creates list of dataLinks for use by JobSelect
        for x in range(0, len(inputs)):
                inputs[x] = dataLink(serverAddr,inputs[x])
        return inputs


def readFileExistsInThredds(name):
	return os.path.isfile(name)

def filecheck(inputs):
	#Deprecated, remains  avalible so that url downloading support
	#can be re-added
	for inputFile in inputs:
		if readFileExistsInThredds(getLocation(inputFile)) == 0:
			downloadFile(inputFile)

def localFile(url):
	#Deprecated
	if not "/dodsC/" in url:
		return 1
	else:
		return 0

def downloadFile(url):
	#Deprecated, remains  avalible so that url downloading support
	#can be re-added
	if localFile(url):
		filePath = getLocation(url)
		r = requests.get(url)
		f = open(filePath, 'wb')
		for chunk in r.iter_content(chunk_size=512 * 1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
		f.close()
	else:
		cdo = Cdo()
		print url.split('?',1)[0]
    		cdo.copy(input = url.split('?',1)[0], output = getLocation(url))
	return 

def getinputs(inputFiles):
	#Deprecated, remains  avalible so that url downloading support
	#can be re-added
	inputs = inputFiles.split(",http")
        for x in range(1, len(inputs)):
                inputs[x] = 'http' + inputs[x]
	return inputs

def jobStatus(jobid,status):
	#Contact the Django server to notify it of the job status
	djangoFile = open('DjangoServer')
	djangoAddr = djangoFile.read().strip()
	publicfile = open('publicKey.pem')
	pubdata = publicfile.read()
	pubkey = rsa.PublicKey.load_pkcs1(pubdata)
	
	wCall = djangoAddr + '/update_computation_status?id='
	wCall += encryptField(pubkey,jobid)
	wCall += '&status='
	wCall += encryptField(pubkey,status)
	urllib.urlopen(wCall)

def encryptField(pubkey, value):
	crypto = rsa.encrypt(value,pubkey)
	return base64.b16encode(crypto) #Encoding used for url compatibility

def getServerAddr():
	serverFile = open('ThreddServer')
	return serverFile.read().strip()

def Operation(Inputs,Selection,Jobid):
	jobStatus(Jobid,'1') #Start of Job
	inputs = Inputs.split('|')
	filename = Jobid + '.nc'
	outputFile = "/var/www/cgi-bin/Thredds/outputs/" + filename

	serverAddr = getServerAddr()
	if len(inputs) < 1:
		jobStatus(Jobid,'3') #Not enough files
		return
	try:
		if readFileExistsInThredds(outputFile):
			jobStatus(Jobid,'2') #File already exists
		        return
	except:
		jobStatus(Jobid,'4')
		return # "Could not open outputFile for writing." 
	
        jobSelect.jobSelect(Selection,compileVarArray(serverAddr,inputs),[outputFile])

	jobStatus(Jobid,'2') #Success
        return  

def main():
        try:
                Operation(sys.argv[1],sys.argv[2],sys.argv[3])
        except Exception as e:
                jobStatus(sys.argv[3],'7') #Operation Failed
                raise e

if __name__ == '__main__':
        exitCode = main()
        exit(exitCode)
