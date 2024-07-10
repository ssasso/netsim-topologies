#!/bin/bash

H=172.23.128.5
DIR=/root/UNITN/

rsync -e ssh -vatP ./ --exclude={'.git','rsync.sh'} root@$H:$DIR


