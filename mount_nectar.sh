#!/bin/bash
/usr/bin/s3fs data Thredds/ -o url="https://swift.rc.nectar.org.au:8888/" -o use_path_request_style -o allow_other -o uid=500 -o gid=0

