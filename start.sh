#!/bin/bash
cd /root/grenadine
echo "Setting up dependencies..."
sudo ./01_install_ap.sh
sudo ./02_interfaces_config.sh
sleep 5
echo "Starting grenadine..."
sudo python /root/grenadine/server.py &

