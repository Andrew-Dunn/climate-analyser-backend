Install:
This project was originally created using Centos 6.5 As such it's use
in other environments may require changes.

git clone https://github.com/climate-analyser-team/climate-analyser-backend.git

in the Climate analyzer folder, run the install.sh script.
PLEASE NOTE: due to a gdal dependency error in yum the constuction
of the zoo_loader.cgi may fail. In this case I have included a prebuilt version.
This does not appear to be a problem.

If no errors appear please verify that the /var/www/cgi-bin folder
exists and that it works with apache as approite.
Also please include a privateKey.pem and publicKey.pem (same as Django)
as certain functions are dependant on authentication.
Run createKeyPairs.py to generate keys if needed

sudo ./config_s3fs.sh Thredds	
#This creates a folder that allows us to share resources
Mount and unmount files should be kept in cgi-bin for ease of use

Change the Address in the DjangoServer file to the Django address,
to enable notifications.
Also set the address in the ThreddServer file.

It is recomended that you generate a key for munge or copy it over
from another node. Which will be used in the next install script
All munge keys must be the same so only generate one key 
dd if=/dev/urandom bs=1 count=1024 >munge.key

A slurm.conf file is included but it will have to be set up to suit your
configuaration. Also note that the /etc/hosts file may need to be
updated to provide addresses for the nodes.
It is also recomended that all nodes be added to a security group
opening ports to the other nodes.

run installSlurm.sh

To properly use Cdo tools you may need to edit the cdo.py script.
Otherwise you may encounter strange issues running cdo operations.
By default edit the file /usr/lib/python2.6/site-packages/cdo.py
and replace the line(64): self.CDO = 'cdo'
With: self.CDO = '/usr/local/bin/cdo'

To start up slurm use the following commands
sudo munged
sudo slurmctld	#On the Zoo server only
sudo slurmd	#including both allows the Zoo server to act as a node
Also run these and the mount_nectar.sh script when restarting the instance
