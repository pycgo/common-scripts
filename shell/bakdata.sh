#!/bin/bash
src_path="/var/lib/docker/overlay2/4ba299567d126826da590c783ef93a87ab9b983a945fa047e01bb48d370b3035/merged/ql/config"
cd $src_path
today=`date +%Y-%m-%d`
cp config.yml /root/bak/config.yml$today
cp env.sh /root/bak/env.sh$today
