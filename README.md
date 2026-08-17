<div align="center">

# 👿 WiFiDaemon

### *"Silent Guardian of the Airwaves"*

![Rust](https://img.shields.io/badge/Made_with-Rust-orange?style=for-the-badge&logo=rust)
![Build](https://img.shields.io/badge/build-passing-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Termux%20%7C%20Linux-lightgrey?style=for-the-badge)

---

```text
           __        ___ _     _
 _      _  \ \      / (_) | __| | ___  ___| |_ _ __ ___  _ __
| | | | |  \ \ /\ / /| | |/ _` |/ _ \/ __| __| '__/ _ \| '_ \
| |_| | |   \ V  V / | | | (_| |  __/\__ \ |_| | | (_) | | | |
 \__,_|_|    \_/\_/  |_|_|\__,_|\___||___/\__|_|  \___/|_| |_|
                      WiFiDAEMON 😈 v0.1.0
              "Silent Guardian of the Airwaves"
<div align="center">

# 👿 WiFiDaemon

### *"Silent Guardian of the Airwaves"*
---

```text
           __        ___ _     _
 _      _  \ \      / (_) | __| | ___  ___| |_ _ __ ___  _ __
| | | | |  \ \ /\ / /| | |/ _` |/ _ \/ __| __| '__/ _ \| '_ \
| |_| | |   \ V  V / | | | (_| |  __/\__ \ |_| | | (_) | | | |
 \__,_|_|    \_/\_/  |_|_|\__,_|\___||___/\__|_|  \___/|_| |_|
                      WiFiDAEMON 😈 v0.1.0
              "Silent Guardian of the Airwaves"

</div>WiFiDaemon is a Rust-powered wireless security daemon that captures, replays, and analyzes Wi-Fi management traffic.
It’s designed for ethical security research, penetration-testing education, and network telemetry visualization.


---

⚙️ Features

🧠 Smart Packet Capture: Reads .pcap files or performs live capture (if supported by the environment).

💾 Beacon Frame Analysis: Summarizes management traffic in clean JSON logs.

🧩 Cross-Platform: Works on Termux, Linux, and macOS.

🧱 Modular Design: Easy to extend for your own experiments.

🎨 ASCII Demon Banner: Eye-catching CLI startup with signature daemon art.

🧑‍💻 Educational Focus: Helps you understand how tools like Aircrack-NG, Airodump, and WiFite process network packets.



---

🚀 Quick Start

🔧 Install (Termux / Linux)

pkg install rust libpcap clang make git -y
git clone https://github.com/umenyi-bryan/wifidaemon.git
cd wifidaemon/daemon
cargo build --release

▶️ Run

./target/release/wifidaemon_daemon

or to replay a .pcap file:

./target/release/wifidaemon_daemon --pcap-file your_capture.pcap --output-json beacon_log.json

---

🧑‍🏫 Educational Value

WiFiDaemon is designed to help cybersecurity students explore:

802.11 management frames

Packet capture, filtering, and replay

Ethical analysis of wireless traffic

Rust systems programming for networking tools


> ⚠️ Disclaimer:
This tool is strictly for educational and ethical use.
Unauthorized interception of networks you don’t own or have permission to test is illegal.




---

🧠 Author

Created by Chinedu — @umenyi-bryan
Built with 💻, ☕, and a fascination for wireless magic.


---

🪪 License

Released under the MIT License.
You’re free to use, modify, and share — responsibly.


---

<div align="center">
🌀 *Hack the airwaves, but do it with honor.*  
</div>
```
