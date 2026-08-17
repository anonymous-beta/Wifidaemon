<div align="center">

<img src="assets/logo.png" alt="WiFiDAEMON Logo" width="200">

# 👿 WiFiDAEMON

### *"Silent Guardian of the Airwaves"*

[![Python](https://img.shields.io/badge/Python-3.8%2B-red?style=for-the-badge&logo=python)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Termux-purple?style=for-the-badge)](https://github.com/anonymous-beta/Wifidaemon)
[![License](https://img.shields.io/badge/License-MIT-darkred?style=for-the-badge)](LICENSE)
[![Root](https://img.shields.io/badge/Requires-Root%20%E2%9A%A1-black?style=for-the-badge)]()

```text
           __        ___ _     _
 _      _  \ \      / (_) | __| | ___  ___| |_ _ __ ___  _ __
| | | | |  \ \ /\ / /| | |/ _` |/ _ \/ __| __| '__/ _ \| '_ \
| |_| | |   \ V  V / | | | (_| |  __/\__ \ |_| | | (_) | | | |
 \__,_|_|    \_/\_/  |_|_|\__,_|\___||___/\__|_|  \___/|_| |_|
                      WiFiDAEMON v2.0.0-DEMON
              "Silent Guardian of the Airwaves"
```

</div>

---

## 🔥 Overview

**WiFiDAEMON** is a next-generation, modular, and demon-themed Wi-Fi pentesting framework. Built from the ground up to replace legacy tools with a unified, chainable, and visually stunning terminal experience.

Designed for **Linux** and **Termux (root)**. No bloat. No slop. Just pure wireless dominance.

---

## ⚡ Features

| Module | Description |
|--------|-------------|
| 🧿 **Smart Scanner** | Passive & active discovery with client enumeration |
| 💀 **Deauth Flood** | Targeted or broadcast deauthentication storms |
| 🔐 **Handshake Capture** | Automated WPA/WPA2 4-way handshake snatching |
| 👹 **Evil Twin** | Rogue AP with captive portal DNA |
| 📡 **Beacon Flood** | SSID spam and network confusion |
| 🛡️ **Auth DoS** | Authentication flood to lock clients |
| 🔑 **WPS Bruteforce** | PIN attacks via `reaver` / `bully` |
| 🧬 **PMKID Capture** | Modern WPA keyless capture |
| ⚔️ **ARP Replay** | Classic WEP injection & keystream recovery |
| 🩸 **Michael Exploit** | TKIP MIC failure demonstration |
| 🔗 **Chain Engine** | Chain any attacks in sequence with delays & conditions |
| 🖥️ **Demon TUI** | Rich, real-time dashboard with live scan tables & logs |

---

## 📸 Terminal UI

```text
┌─────────────────────────────────────────────────────────────┐
│  👿 WiFiDAEMON v2.0.0-DEMON  |  Silent Guardian             │
├─────────────────────────────────────────────────────────────┤
│  Networks          │  Status                                │
│  #  BSSID    SSID  │  Interface: wlan0mon                   │
│  1  AA:BB.. Demon  │  Monitor:   ENABLED                    │
│  2  CC:DD.. Hidden │  Networks: 42                          │
│                    │  Status:   ATTACKING                   │
├─────────────────────────────────────────────────────────────┤
│  DEMON LOG                                                  │
│  [20:01] Monitor mode enabled on wlan0mon                   │
│  [20:02] Scan complete: 42 networks found                   │
│  [20:03] Deauth chain started -> Handshake capture active   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Linux

```bash
# 1. Clone the repository
git clone https://github.com/anonymous-beta/Wifidaemon.git
cd Wifidaemon

# 2. Install system dependencies
sudo bash daemon/scripts/install_linux.sh

# 3. Install Python dependencies
pip3 install -r requirements.txt

# 4. Launch the Demon
sudo python3 -m daemon --tui
```

### Termux (Root Required)

```bash
# 1. Clone
git clone https://github.com/anonymous-beta/Wifidaemon.git
cd Wifidaemon

# 2. Install
bash daemon/scripts/install_termux.sh

# 3. Run with root
tsu -c "python -m daemon --tui"
```

---

## 🎮 Usage

### Interactive TUI (Recommended)
```bash
sudo python3 -m daemon --tui
```

### Quick Scan
```bash
sudo python3 -m daemon --scan -i wlan0mon
```

### Single Attack
```bash
# Deauth
sudo python3 -m daemon --attack deauth -b AA:BB:CC:DD:EE:FF -i wlan0mon --count 128

# Handshake capture
sudo python3 -m daemon --attack handshake -b AA:BB:CC:DD:EE:FF -i wlan0mon --output handshake.pcap

# Beacon flood
sudo python3 -m daemon --attack beacon_flood -i wlan0mon --count 1000

# Evil Twin
sudo python3 -m daemon --attack evil_twin -e "Free_WiFi" -i wlan0 --channel 6
```

### Chain Attacks
Create `chain.json`:
```json
[
  {"attack": "deauth", "params": {"target_bssid": "AA:BB:CC:DD:EE:FF", "iface": "wlan0mon", "count": 64}, "timeout": 30, "delay": 2},
  {"attack": "handshake", "params": {"target_bssid": "AA:BB:CC:DD:EE:FF", "iface": "wlan0mon", "output": "daemon_handshake.pcap"}, "timeout": 60}
]
```

Run:
```bash
sudo python3 -m daemon --chain chain.json
```

---

## 🏗️ Architecture

```text
Wifidaemon/
├── daemon/
│   ├── core/          # Engine, scanner, interface manager, state
│   ├── tui/           # Demon-themed Terminal UI (Rich-based)
│   ├── modules/
│   │   ├── attacks/   # All attack modules + chain engine
│   │   └── utils/     # Packet crafter, logger, validators
│   └── scripts/       # Platform install scripts
├── wordlists/         # Custom wordlist storage
├── logs/              # Runtime logs
└── docs/              # Extended documentation
```

---

## ⚠️ Disclaimer

**WiFiDAEMON is strictly for authorized security testing and educational purposes.**

Unauthorized access to computer networks is illegal. The author assumes **zero liability** for misuse. If you break the law, the demons come for *you*.

> *"Hack the airwaves, but do it with honor."*

---

## 🧙 Author

**Anonymous-beta**  
📧 anonym09g@gmail.com  
🔗 https://github.com/anonymous-beta

---

## 🪪 License

MIT License — See [LICENSE](LICENSE) for details.

<div align="center">

👿 *Summon the Daemon. Own the Airwaves.*

</div>
