#!/bin/sh
echo "getting MicroWebSrv V1 from https://github.com/jczic/MicroWebSrv"
wget https://github.com/jczic/MicroWebSrv/archive/refs/heads/master.zip
wget -N https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebSocket.py
wget -N https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebSrv.py
wget -N https://raw.githubusercontent.com/jczic/MicroWebSrv/master/microWebTemplate.py
