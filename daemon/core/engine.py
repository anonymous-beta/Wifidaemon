"""
DaemonEngine: central controller that wires interface, scanner, attacks, and chain engine.
"""
import json
import threading
import time

from daemon.core.interface import InterfaceManager
from daemon.core.scanner import WiFiScanner
from daemon.modules.attacks.deauth import DeauthAttack
from daemon.modules.attacks.handshake import HandshakeCapture
from daemon.modules.attacks.beacon_flood import BeaconFlood
from daemon.modules.attacks.auth_dos import AuthDoS
from daemon.modules.attacks.evil_twin import EvilTwin
from daemon.modules.attacks.wps_brute import WPSBrute
from daemon.modules.attacks.pmkid import PMKIDCapture
from daemon.modules.attacks.arp_replay import ARPReplay
from daemon.modules.attacks.michael import MichaelExploit
from daemon.modules.attacks.chain_engine import ChainEngine


class DaemonEngine:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.interface = InterfaceManager(config, logger)
        self.scanner = WiFiScanner(config, logger)
        self.chain = ChainEngine(self, logger)
        self._lock = threading.Lock()

        self.attacks = {
            "deauth": DeauthAttack,
            "handshake": HandshakeCapture,
            "beacon_flood": BeaconFlood,
            "auth_dos": AuthDoS,
            "evil_twin": EvilTwin,
            "wps_brute": WPSBrute,
            "pmkid": PMKIDCapture,
            "arp_replay": ARPReplay,
            "michael": MichaelExploit,
        }

    def scan(self, duration=30):
        if not self.config.state["monitor_mode"]:
            self.interface.enable_monitor()
        return self.scanner.scan(duration)

    def run_attack(self, name, args):
        if name not in self.attacks:
            self.logger.error(f"Unknown attack: {name}")
            return False
        if not self.config.state["monitor_mode"]:
            self.interface.enable_monitor()
        attack = self.attacks[name](self.config, self.logger)
        self.config.state["attacking"] = True
        try:
            result = attack.run(args)
        except Exception as e:
            self.logger.error(f"Attack failed: {e}")
            result = False
        self.config.state["attacking"] = False
        return result

    def run_chain(self, path):
        with open(path, "r") as f:
            chain_data = json.load(f)
        self.chain.execute(chain_data)

    def stop(self):
        self.scanner.stop()
        self.chain.stop()
