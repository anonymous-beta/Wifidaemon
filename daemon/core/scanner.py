"""
802.11 Scanner: passive discovery of APs and clients using Scapy.
"""
from scapy.all import sniff, Dot11, Dot11Beacon, Dot11ProbeResp, Dot11Elt
import threading
import time


class WiFiScanner:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.networks = {}
        self.clients = {}
        self._stop_event = threading.Event()

    def _packet_handler(self, pkt):
        if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
            bssid = pkt[Dot11].addr3
            ssid = pkt[Dot11Elt].info.decode(errors="ignore") if pkt.haslayer(Dot11Elt) else "<Hidden>"
            try:
                channel = pkt[Dot11Elt:3].info
                if isinstance(channel, bytes):
                    channel = channel[0]
                else:
                    channel = ord(channel)
            except Exception:
                channel = -1
            if bssid and bssid not in self.networks:
                self.networks[bssid] = {
                    "ssid": ssid or "<Hidden>",
                    "channel": channel,
                    "signal": getattr(pkt, "dBm_AntSignal", "N/A"),
                    "crypto": list(pkt[Dot11Beacon].network_stats().get("crypto", [])) if pkt.haslayer(Dot11Beacon) else []
                }
                self.logger.info(f"[AP] {ssid} | {bssid} | CH:{channel}")
        elif pkt.haslayer(Dot11) and pkt[Dot11].type == 2:
            client = pkt[Dot11].addr2
            bssid = pkt[Dot11].addr1
            if client and client not in self.clients and client != "ff:ff:ff:ff:ff:ff":
                self.clients[client] = {"bssid": bssid, "last_seen": time.time()}

    def scan(self, duration=30):
        self.logger.info(f"Starting passive scan on {self.config.mon_iface} for {duration}s...")
        self.config.state["scanning"] = True
        self._stop_event.clear()
        self.networks.clear()
        self.clients.clear()
        try:
            sniff(iface=self.config.mon_iface, prn=self._packet_handler, timeout=duration, stop_filter=lambda x: self._stop_event.is_set())
        except Exception as e:
            self.logger.error(f"Scan error: {e}")
        self.config.state["scanning"] = False
        self.config.state["networks"] = self.networks
        self.config.state["clients"] = self.clients
        self.logger.success(f"Scan complete. Found {len(self.networks)} APs, {len(self.clients)} clients.")
        return self.networks, self.clients

    def stop(self):
        self._stop_event.set()
