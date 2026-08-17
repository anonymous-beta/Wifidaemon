"""Global configuration for WiFiDAEMON."""


class DaemonConfig:
    def __init__(self, iface="wlan0", verbose=False, timeout=60):
        self.iface = iface
        self.mon_iface = iface + "mon"
        self.verbose = verbose
        self.timeout = timeout
        self._state = {
            "monitor_mode": False,
            "scanning": False,
            "attacking": False,
            "networks": {},
            "clients": {},
            "logs": []
        }

    @property
    def state(self):
        return self._state

    def log(self, msg):
        self._state["logs"].append(msg)
        if len(self._state["logs"]) > 500:
            self._state["logs"] = self._state["logs"][-500:]
