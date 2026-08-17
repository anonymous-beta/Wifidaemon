#!/bin/bash
set -e
echo "[👿] WiFiDAEMON Linux Installer"
sudo apt-get update
sudo apt-get install -y aircrack-ng hostapd dnsmasq hcxtools iw wireless-tools net-tools python3 python3-pip libpcap-dev
pip3 install scapy rich psutil
echo "[✅] Done. Run with: sudo python3 -m daemon --tui"
