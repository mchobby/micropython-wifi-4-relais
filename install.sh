#!/bin/sh
SER="/dev/ttyACM0"
CUR_DIR=`pwd`
while :
do

clear
echo "Wait for Pico-W on $SER..."
while [ ! -f /media/domeu/RPI-RP2/INFO_UF2.TXT ]; do sleep 1; done
echo "Flashing MicroPython..."
cp /home/domeu/Téléchargements/upy/rp2-pico-w-20220913-unstable-v1.19.1-408-g74805435f.uf2 /media/domeu/RPI-RP2/
echo "Wait Pico-W reboot on $SER..."
while ! (ls $SER 2>/dev/null) do sleep 1; done;

echo "Copy wifi-4-relay files"
mpremote connect $SER fs mkdir lib
mpremote connect $SER fs mkdir www
echo " - Copying WebServer ..."
mpremote connect $SER fs cp lib/microWebSocket.py :lib/microWebSocket.py
mpremote connect $SER fs cp lib/microWebSrv.py :lib/microWebSrv.py
mpremote connect $SER fs cp lib/microWebTemplate.py :lib/microWebTemplate.py
echo " - Copying www ..."
mpremote connect $SER fs cp www/favicon.ico :www/favicon.ico
mpremote connect $SER fs cp www/style.css :www/style.css
mpremote connect $SER fs cp www/credit.html :www/credit.html
mpremote connect $SER fs cp www/index.pyhtml :www/index.pyhtml
mpremote connect $SER fs cp www/status.pyhtml :www/status.pyhtml
echo " - Copying main ..."
mpremote connect $SER fs cp main.py :main.py
mpremote connect $SER fs cp blink.py :blink.py
mpremote connect $SER fs cp examples/iotest.py :iotest.py
mpremote connect $SER fs cp examples/boot.timeout.sample :boot.py
mpremote connect $SER fs cp examples/wifi_cfg.sample :wifi_cfg.py

# Test the board
mpremote connect $SER run blink.py

cd ../lib

done
