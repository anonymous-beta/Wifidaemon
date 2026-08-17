#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "[👿] WiFiDAEMON Termux Installer"
pkg update -y
pkg install -y root-repo aircrack-ng hostapd dnsmasq hcxtools iw wireless-tools net-tools python python-pip libpcap-dev
pip3 install scapy rich psutil
echo "[✅] Done. Run with: tsu -c 'python -m daemon --tui'"
