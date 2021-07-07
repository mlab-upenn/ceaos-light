#!/bin/sh
#launcher.sh

cd /
cd home/pi/ceaos-light
sudo python3 setup.py install
cd ceaos_light
sudo python3 driver.py
cd /