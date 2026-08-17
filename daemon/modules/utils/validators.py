"""Input validators."""
import re

MAC_RE = re.compile(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$")


def valid_mac(mac):
    return bool(MAC_RE.match(mac))


def valid_channel(ch):
    return isinstance(ch, int) and 1 <= ch <= 165


def valid_ssid(ssid):
    return ssid and len(ssid) <= 32
