bom-backend
===========

ZOO server, coordinates compute cloud.

JobScheduler.py:
Called through the Zoo WPS, the scheduler starts the job using Slurm
To delegate work over multiple nodes. 
Inputs: 
"Selection" = the operation to be performed
"urls" = the files to operate on, seperated by a comma
"jobid" = The job id assigned in django. This will get used as an output name.
ex: http://130.56.248.143/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0.0&identifier=jobScheduler&DataInputs=selection=correlate;urls=
sample1.nc,sample2.nc;jobid=123

Operation.py
Once called by the jobScheduler via slurm, the Operation program take in the operation
filenames and job id. Using these it will start up the job using the selected operation
which is run via the JobSelect script
Inputs: "Urls" = filenames seperated by comma's
"Selection" = the name of the operation to be applied
"jobId" = The id provided by Djanog. This will be used to create a file name
eg. 123.nc
ex: python Operation.py file1,file2 operation id

JobSelect.py
Called via Operation. THe JobSelection script can call any script contained in the
"operators" folder. So long as the python file is valid and it calls the "run" method
with the parameters inputFiles[] and outputFiles[] (See operators for more)
It can also call any cdo operation by using the prefix 'cdo-' so for example the regres
operator can be called with "cdo-regres"
Inputs: "op" = operation to be used (mapping to a python file in the operators folder.)
prefix with "cdo-" for cdo functions
"inputFiles" = an array of input files to be passed into the "Run" function
"outputFiles" = an array of output files to be passed into the "Run" function.

ChangeThredds.py
Using a Zoo call, set the associated Thredds Server using an encrypted url
The url should be first encrypted using the associated rsa public key and
then encoded using b16 encoding so the encrypted url can be safly included
in the Zoo call.
EX: http://130.56.248.143/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0.0&identifier=ChangeThredds&DataInputs=url='encryptedurl'

ChangeDjango.py
Using a Zoo call, set the associated Django Server using an encrypted url
The url should be first encrypted using the associated rsa public key and
then encoded using b16 encoding so the encrypted url can be safly included
in the Zoo call.
EX: http://130.56.248.143/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0.0&identifier=ChangeDjango&DataInputs=url='encryptedurl'

slurmInfo.py
Using a Zoo call request information from the slurm client. Commands are:
sinfo    -> sinfo -N -l
squeue -> squeue
snodes -> scontrol -o show nodes
sall      -> all of the above
EX: http://130.56.248.143/cgi-bin/zoo_loader.cgi?request=Execute&service=WPS&version=1.0.0.0&identifier=slurmInfo&DataInputs=option='command'

