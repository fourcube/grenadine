#!/bin/bash
cd /root/grenadine
git pull
echo "Setting up dependencies..."
sudo ./configure_wlan.sh
sleep 5
echo "Starting grenadine..."
sudo python /root/grenadine/server.py &
