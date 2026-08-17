"""
WPA/WPA2 4-Way Handshake Capture Module
Sniffs EAPOL frames and saves to pcap.
"""
import os
import threading
from scapy.all import sniff, Dot11, EAPOL, wrpcap


class HandshakeCapture:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.handshakes = []
        self._stop = threading.Event()

    def _handler(self, pkt):
        if pkt.haslayer(EAPOL):
            self.handshakes.append(pkt)
            self.logger.info(f"EAPOL frame captured ({len(self.handshakes)})")
        if len(self.handshakes) >= 4:
            self._stop.set()

    def run(self, args):
        bssid = args.bssid
        iface = self.config.mon_iface
        output = args.output or "handshake.pcap"
        timeout = args.timeout

        self.logger.attack_log(f"Handshake capture on {bssid} -> {output}")
        self._stop.clear()
        self.handshakes.clear()
        try:
            sniff(iface=iface, prn=self._handler, timeout=timeout, stop_filter=lambda x: self._stop.is_set())
            if self.handshakes:
                wrpcap(output, self.handshakes)
                self.logger.success(f"Saved {len(self.handshakes)} EAPOL frames to {output}")
                return True
            else:
                self.logger.warning("No handshake captured.")
                return False
        except Exception as e:
            self.logger.error(f"Handshake capture failed: {e}")
            return False
