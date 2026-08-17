"""
Chain Engine: execute multiple attacks in sequence with delays, timeouts, and conditions.
Chain JSON format:
[
  {
    "attack": "deauth",
    "params": {"bssid": "...", "client": "...", "count": 64, "iface": "wlan0mon"},
    "timeout": 30,
    "delay": 2,
    "condition": {"type": "scan_found", "bssid": "..."}
  },
  ...
]
"""
import json
import time
import threading


class ChainEngine:
    def __init__(self, engine, logger):
        self.engine = engine
        self.logger = logger
        self._stop = threading.Event()
        self._running = False

    def _check_condition(self, condition):
        if not condition:
            return True
        ctype = condition.get("type")
        if ctype == "scan_found":
            target = condition.get("bssid")
            nets = self.engine.config.state.get("networks", {})
            return target in nets
        if ctype == "always":
            return True
        return True

    def execute(self, chain_data):
        self._stop.clear()
        self._running = True
        self.logger.demon("Chain Engine started.")
        for idx, step in enumerate(chain_data):
            if self._stop.is_set():
                self.logger.warning("Chain stopped by user.")
                break

            attack_name = step.get("attack")
            params = step.get("params", {})
            timeout = step.get("timeout", 60)
            delay = step.get("delay", 0)
            condition = step.get("condition")

            self.logger.info(f"[Chain {idx+1}/{len(chain_data)}] Preparing {attack_name}...")

            if not self._check_condition(condition):
                self.logger.warning(f"Condition not met for {attack_name}. Skipping.")
                continue

            class Args:
                pass
            args = Args()
            for k, v in params.items():
                setattr(args, k, v)
            for attr in ["bssid", "ssid", "client", "output", "wordlist", "count", "channel", "iface", "timeout"]:
                if not hasattr(args, attr):
                    setattr(args, attr, None)
            if not args.count:
                args.count = 128
            if not args.timeout:
                args.timeout = timeout

            if delay:
                self.logger.info(f"Delaying {delay}s before {attack_name}...")
                time.sleep(delay)

            self.engine.run_attack(attack_name, args)

        self._running = False
        self.logger.demon("Chain Engine finished.")

    def stop(self):
        self._stop.set()
