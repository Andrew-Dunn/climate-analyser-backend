#!/bin/bash

if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root through sudo." 1>&2
   exit 1
fi

RUNASUSER="sudo -u $SUDO_USER"

yum -y install tar bzip2 gcc gcc-c++ autoconf bison flex patch httpd
yum -y install gdal-devel libxml2-devel python-devel libcurl-devel openssl-devel

$RUNASUSER bash <<EOS
curl http://www.zoo-project.org/dl/zoo-project-1.3.0.tar.bz2 -o zoo-project-1.3.0.tar.bz2
tar -xjf zoo-project-1.3.0.tar.bz2
rm zoo-project-1.3.0.tar.bz2

curl http://www.fastcgi.com/dist/fcgi.tar.gz -o fcgi.tar.gz
tar -xzf fcgi.tar.gz
EOS

cd $(ls fcgi*/ -d | head -n 1)

$RUNASUSER bash <<EOS
patch -p0 <<EOF
--- include/fcgio.h     2002-02-25 13:16:11.000000000 +0000
+++ include/fcgio.h     2014-07-14 01:40:07.914260118 +0000
@@ -31,6 +31,7 @@
 #define FCGIO_H

 #include <iostream>
+#include <stdio.h>

 #include "fcgiapp.h"

EOF
autoconf
./configure
make
EOS
make install

echo "/usr/local/lib" > /etc/ld.so.conf.d/climate-analyser.conf
ldconfig

cd ../zoo-project-1.3.0
cd thirds/cgic*

$RUNASUSER bash <<EOS
sed -e "s:/usr/lib\(64\)\{0,1\}/libfcgi\.so:-lfcgi:g" Makefile > Makefile.tmp \
    && mv Makefile.tmp Makefile
make
make install
EOS

cd ../../zoo-project/zoo-kernel/

$RUNASUSER bash <<EOS
autoconf
./configure --with-python
make
make zoo_loader.cgi
EOS

mkdir -p /var/www/cgi-bin
rm -rf $PWD/cgi-bin
cp main.cfg /var/www/cgi-bin/
cp zoo_loader.cgi /var/www/cgi-bin/

cd ../../..
ln -s /var/www/cgi-bin $PWD/cgi-bin

cp Operation.{zcfg,py} cgi-bin

rm -f /etc/httpd/conf/httpd.conf
ln -s $PWD/httpd.conf /etc/httpd/conf/httpd.conf
