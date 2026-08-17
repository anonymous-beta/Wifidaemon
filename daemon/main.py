"""
WiFiDAEMON Entry Point
Handles CLI arguments, initializes the engine, and dispatches to TUI or attack mode.
"""
import argparse
import sys
import os

from daemon.core.engine import DaemonEngine
from daemon.core.config import DaemonConfig
from daemon.tui.demon_tui import DemonTUI
from daemon.modules.utils.logger import DemonLogger
from daemon.modules.utils.banner import print_banner


def main():
    parser = argparse.ArgumentParser(
        prog="wifidaemon",
        description="👿 WiFiDAEMON — Advanced WiFi Pentesting Framework"
    )
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--tui", action="store_true", help="Launch the Demon TUI")
    parser.add_argument("--scan", action="store_true", help="Run a quick scan")
    parser.add_argument("--iface", "-i", type=str, default="wlan0", help="Wireless interface")
    parser.add_argument("--attack", type=str, choices=[
        "deauth", "handshake", "beacon_flood", "auth_dos", "evil_twin",
        "wps_brute", "pmkid", "arp_replay", "michael"
    ], help="Attack module to run")
    parser.add_argument("--bssid", "-b", type=str, help="Target BSSID")
    parser.add_argument("--ssid", "-e", type=str, help="Target SSID / Evil Twin name")
    parser.add_argument("--channel", "-c", type=int, help="Target channel")
    parser.add_argument("--count", "-n", type=int, default=128, help="Packet count")
    parser.add_argument("--output", "-o", type=str, help="Output file (pcap/json)")
    parser.add_argument("--chain", type=str, help="Path to chain JSON file")
    parser.add_argument("--client", type=str, help="Target client MAC (for deauth)")
    parser.add_argument("--wordlist", type=str, help="Wordlist path")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout per attack (seconds)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    if args.version:
        print("WiFiDAEMON v2.0.0-DEMON")
        sys.exit(0)

    if os.geteuid() != 0:
        print("[⚠️] WiFiDAEMON requires root privileges. Run with sudo.")
        sys.exit(1)

    config = DaemonConfig(iface=args.iface, verbose=args.verbose)
    logger = DemonLogger(verbose=args.verbose)
    engine = DaemonEngine(config, logger)

    if args.tui:
        print_banner()
        tui = DemonTUI(engine)
        tui.run()
    elif args.scan:
        print_banner()
        engine.scan()
    elif args.attack:
        print_banner()
        engine.run_attack(args.attack, args)
    elif args.chain:
        print_banner()
        engine.run_chain(args.chain)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
