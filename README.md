bom-backend
===========

Install:
This project was originally created using Centos 6.5 As such it's use
in other environments may require changes.

git clone https://github.com/climate-analyser-team/climate-analyser-backend.git

in the Climate analyzer folder, run the install.sh script.
If no errors appear please verify that the /var/www/cgi-bin folder
exists and that it works with apache as approite.
Also please include a privateKey.pem and publicKey.pem (same as Django)
as certain functions are dependant on authentication.

sudo ./config_s3fs.sh Thredds	
#This creates a folder that allows us to share resources
Mount and unmount files should be kept in cgi-bin for ease of use

Change the Address in the DjangoServer file to the Django address,
to enable notifications.
Also set the address in the ThreddServer file.

It is recomended that you generate a key for munge or copy it over
from another node. Which will be used in the next install 
dd if=/dev/urandom bs=1 count=1024 >munge.key

A slurm.conf file is included but it will have to be set up to suit your
configuaration. Also note that the /etc/hosts file may need to be
updated to provide addresses for the nodes.
It is also recomended that all nodes be added to a security group
opening ports to the other nodes.

run installSlurm.sh

To properly use Cdo tools you may need to edit the cdo.py script.
By default edit the file /usr/lib/python2.6/site-packages/cdo.py
and replace the line(64): self.CDO = 'cdo'
With: self.CDO = '/usr/local/bin/cdo'

To start up slurm use the following commands
sudo munged
sudo slurmctld	#Technically you can drop one or the other as appropite
sudo slurmd	#But including both allows the Zoo server to act as a node
Also run these and the mount_nectar.sh script when restarting the instance

-------------------------------------------------

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

