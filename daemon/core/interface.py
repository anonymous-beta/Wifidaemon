"""
Interface Manager: enables/disables monitor mode, checks compatibility.
Works on Linux and Termux (with root).
"""
import subprocess
import shutil
import time


class InterfaceManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.iface = config.iface
        self.mon_iface = config.mon_iface

    def check_root(self):
        import os
        return os.geteuid() == 0

    def check_tools(self):
        required = ["airmon-ng", "iw", "ifconfig"]
        missing = [t for t in required if not shutil.which(t)]
        if missing:
            self.logger.warning(f"Missing tools: {missing}. Some features may be limited.")
        return missing

    def enable_monitor(self):
        self.logger.info(f"Enabling monitor mode on {self.iface}...")
        try:
            if shutil.which("airmon-ng"):
                subprocess.run(["airmon-ng", "start", self.iface], capture_output=True, check=False)
            else:
                subprocess.run(["ip", "link", "set", self.iface, "down"], capture_output=True, check=False)
                subprocess.run(["iw", "dev", self.iface, "set", "type", "monitor"], capture_output=True, check=False)
                subprocess.run(["ip", "link", "set", self.iface, "up"], capture_output=True, check=False)
            time.sleep(1)
            self.config.state["monitor_mode"] = True
            self.logger.success(f"Monitor mode enabled on {self.mon_iface}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to enable monitor mode: {e}")
            return False

    def disable_monitor(self):
        self.logger.info(f"Disabling monitor mode on {self.mon_iface}...")
        try:
            if shutil.which("airmon-ng"):
                subprocess.run(["airmon-ng", "stop", self.mon_iface], capture_output=True, check=False)
            else:
                subprocess.run(["ip", "link", "set", self.iface, "down"], capture_output=True, check=False)
                subprocess.run(["iw", "dev", self.iface, "set", "type", "managed"], capture_output=True, check=False)
                subprocess.run(["ip", "link", "set", self.iface, "up"], capture_output=True, check=False)
            self.config.state["monitor_mode"] = False
            self.logger.success("Monitor mode disabled.")
            return True
        except Exception as e:
            self.logger.error(f"Failed to disable monitor mode: {e}")
            return False

    def get_interfaces(self):
        try:
            result = subprocess.run(["iw", "dev"], capture_output=True, text=True)
            return result.stdout
        except Exception:
            return ""
