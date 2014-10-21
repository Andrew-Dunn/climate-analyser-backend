if [ "$(id -u)" != "0" ]; then
echo "This script must be run as root through sudo." 1>&2
exit 1
fi
RUNASUSER="sudo -u $SUDO_USER"


yum -y groupinstall "Development tools"
yum -y install readline-devel
yum -y install perl-devel
yum -y install munge-devel
yum -y install pam-devel
yum -y install perl-DBI
yum -y install mailx
yum -y install gperf

yum -y install munge
chown root /etc/munge
chown root /var/lib/munge
chown root /var/log/munge
mkdir /var/run/munge
chown root /var/run/munge
cp munge.key /etc/munge/munge.key
chown root /etc/munge/munge.key
chmod 700 /etc/munge/munge.key

#Download found at http://www.schedmd.com/#archives
curl http://www.schedmd.com/download/latest/slurm-14.03.9.tar.bz2 -o slurm-14.03.9.tar.bz2
rpmbuild -ta slurm*.tar.bz2
rpm -i /root/rpmbuild/RPMS/x86_64/slurm-*
cp slurm.conf /etc/slurm/slurm.conf

mkdir /slurm
chown ec2-user /slurm

curl http://www.colm.net/wp-content/uploads/2014/10/ragel-6.9.tar.gz -o ragel.tar.gz
tar -xf ragel.tar.gz
cd ragel-6.9
./configure --prefix=/
make
make install
cd ..
svn co https://apps.man.poznan.pl/svn/slurm-drmaa/
cd slurm-drmaa/trunk/
./autogen.sh
./configure  --with-slurm-inc=/usr/include/slurm --with-slurm-lib=/usr/lib64/slurm --prefix=/
make
make install
cp /lib/libdrmaa* /lib64


pip install drmaa
pip install pydap
pip install pydap.responses.netcdf
pip install rsa

