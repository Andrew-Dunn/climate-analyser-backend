#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

RUNASUSER="sudo -u $SUDO_USER"

if [ "$#" != "1" ]; then
    echo "Usage: ./config_s3fs.sh MOUNTPOINT"
    exit 0
fi

yum -y install git make gcc gcc-c++ pkgconfig libstdc++-devel curl curlpp curlpp-devel curl-devel libxml2 libxml2* libxml2-devel openssl-devel mailcap
yum -y remove fuse fuse* fuse-devel

$RUNASUSER bash <<EOF
wget "http://downloads.sourceforge.net/project/fuse/fuse-2.X/2.9.3/fuse-2.9.3.tar.gz?r=&ts=1401776172&use_mirror=ufpr"
tar -xzf fuse-2.9.3.tar.gz*
rm -f fuse-2.9.3.tar.gz*
mv fuse-2.9.3 fuse
EOF

cd fuse

$RUNASUSER bash <<EOF
./configure --prefix=/usr
make
EOF

make install
ldconfig
modprobe fuse
cd ..
rm -rf fuse

$RUNASUSER bash <<EOF
git clone https://github.com/s3fs-fuse/s3fs-fuse.git
EOF

cd s3fs-fuse

$RUNASUSER bash <<EOF
export PKG_CONFIG_PATH=/usr/lib/pkgconfig:/usr/lib64/pkgconfig/
./autogen.sh
./configure --prefix=/usr
make
EOF

make install
cd ..
rm -rf s3fs-fuse

$RUNASUSER bash <<EOF
echo "data:13d754307d964db69662286d5e99f48a:09e164c5802d45de805f492e3903f654" > ~/.passwd-s3fs
chmod 400 ~/.passwd-s3fs
EOF

mkdir -p $1
chown $SUDO_UID:$SUDO_GID $1

echo "user_allow_other" > /etc/fuse.conf

$RUNASUSER bash <<EOF
cat > ~/mount_nectar.sh <<EOI
#!/bin/bash
/usr/bin/s3fs data $1 -o url="https://swift.rc.nectar.org.au:8888/" -o use_path_request_style -o allow_other -o uid=$SUDO_UID -o gid=$SUDO_GID
EOI

cat > ~/unmount_nectar.sh <<EOI
#!/bin/bash
fusermount -u $1
EOI

chmod +x ~/mount_nectar.sh
chmod +x ~/unmount_nectar.sh

~/mount_nectar.sh
echo "Data storage has been mounted to '$1'"
EOF
