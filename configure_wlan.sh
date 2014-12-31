#!/bin/bash
sleep 5
iwlist wlan0 scanning
iwconfig wlan0 essid Grenadine
dhclient wlan0
