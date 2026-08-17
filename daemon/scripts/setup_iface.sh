#!/bin/bash
IFACE=${1:-wlan0}
echo "[👿] Setting monitor mode on $IFACE"
airmon-ng start "$IFACE"
echo "[✅] $IFACE should now be in monitor mode."
