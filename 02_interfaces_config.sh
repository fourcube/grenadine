#!/bin/bash
cp config/interfaces.cfg /etc/network/interfaces
cp config/hostap.default /etc/default/hostap
cp config/hostapd.cfg /etc/hostapd/hostapd.conf
cp config/dnsmasq.conf /etc/dnsmasq.conf
cp config/ifstate /etc/network/run/ifstate
sudo service hostapd restart
sudo service dnsmasq restart
sudo ifdown wlan0
sudo ifup wlan0
