"""
DemonTUI: Rich-based Terminal User Interface for WiFiDAEMON.
Dark, demon-themed, real-time dashboard.
"""
import time
import threading
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box


class DemonTUI:
    def __init__(self, engine):
        self.engine = engine
        self.layout = Layout()
        self._stop = threading.Event()
        self._build_layout()

    def _build_layout(self):
        self.layout.split_column(
            Layout(name="header", size=9),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=5)
        )
        self.layout["body"].split_row(
            Layout(name="networks", ratio=3),
            Layout(name="side", ratio=2)
        )
        self.layout["side"].split_column(
            Layout(name="status", ratio=1),
            Layout(name="clients", ratio=1)
        )

    def _header(self):
        ascii_art = (
            "       __        ___ _     _\n"
            " _ _   \\ \\      / (_) | __| | ___  ___| |_ _ __ ___  _ __\n"
            "| | | | \\ \\ /\\ / /| | |/ _` |/ _ \\/ __| __| '__/ _ \\| '_ \\\n"
            "| |_| |  \\ V  V / | | | (_| |  __/\\__ \\ |_| | | (_) | | | |\n"
            " \\__,_|   \\_/\\_/  |_|_|\\__,_|\\___||___/\\__|_|  \\___/|_| |_|"
        )
        text = Text(ascii_art, style="bold magenta")
        text.append("\n👿 WiFiDAEMON v2.0.0-DEMON   ", style="bold red")
        text.append("Silent Guardian of the Airwaves", style="dim")
        return Panel(text, border_style="red", padding=(0, 1))

    def _networks_table(self):
        table = Table(
            title="Discovered Networks",
            box=box.MINIMAL_DOUBLE_HEAD,
            border_style="red",
            header_style="bold cyan",
            expand=True
        )
        table.add_column("#", style="dim", width=4, justify="right")
        table.add_column("BSSID", style="bold green", no_wrap=True)
        table.add_column("SSID", style="white")
        table.add_column("CH", justify="center", style="yellow")
        table.add_column("Sig", justify="right", style="blue")
        table.add_column("Crypto", style="dim")

        nets = self.engine.config.state.get("networks", {})
        for i, (bssid, info) in enumerate(nets.items(), 1):
            ssid = info.get("ssid", "<Hidden>") or "<Hidden>"
            ch = str(info.get("channel", "?"))
            sig = str(info.get("signal", "?"))
            crypto = ",".join(info.get("crypto", [])) or "Open"
            table.add_row(str(i), bssid, ssid, ch, sig, crypto)
        return table

    def _status_panel(self):
        s = self.engine.config.state
        t = Text()
        t.append("Interface  ", style="bold")
        t.append(f"{self.engine.config.iface}\n", style="green")
        t.append("Monitor    ", style="bold")
        t.append(f"{'ENABLED' if s.get('monitor_mode') else 'OFF'}\n", style="green" if s.get("monitor_mode") else "red")
        t.append("Networks   ", style="bold")
        t.append(f"{len(s.get('networks', {}))}\n", style="cyan")
        t.append("Clients    ", style="bold")
        t.append(f"{len(s.get('clients', {}))}\n", style="yellow")
        t.append("Attacking  ", style="bold")
        t.append("YES" if s.get("attacking") else "NO", style="red" if s.get("attacking") else "dim")
        return Panel(t, title="[bold purple]Demon Status", border_style="purple")

    def _clients_table(self):
        table = Table(title="Clients", box=box.SIMPLE, border_style="red", expand=True)
        table.add_column("MAC", style="bold yellow", no_wrap=True)
        table.add_column("BSSID", style="green")

        clients = self.engine.config.state.get("clients", {})
        for mac, info in list(clients.items())[:30]:
            table.add_row(mac, info.get("bssid", "?"))
        return table

    def _logs_panel(self):
        logs = self.engine.config.state.get("logs", [])[-5:]
        content = Text("\n".join(logs), style="dim")
        return Panel(content, title="[bold red]Demon Log", border_style="red")

    def _footer(self):
        t = Text()
        t.append(" Controls  ", style="underline bold white")
        t.append(" [Q]", style="bold red")
        t.append("uit  ")
        t.append("[S]", style="bold green")
        t.append("can  ")
        t.append("[D]", style="bold yellow")
        t.append("eauth  ")
        t.append("[H]", style="bold cyan")
        t.append("andshake  ")
        t.append("[C]", style="bold magenta")
        t.append("hain  ")
        t.append("[R]", style="bold white")
        t.append("eset")
        return Panel(t, border_style="dim")

    def _update(self):
        self.layout["header"].update(self._header())
        self.layout["networks"].update(Panel(self._networks_table(), border_style="red"))
        self.layout["status"].update(self._status_panel())
        self.layout["clients"].update(Panel(self._clients_table(), border_style="red"))
        self.layout["footer"].update(self._footer())

    def _background_scan(self):
        while not self._stop.is_set():
            if not self.engine.config.state.get("scanning") and not self.engine.config.state.get("attacking"):
                try:
                    self.engine.scan(duration=8)
                except Exception:
                    pass
            time.sleep(6)

    def run(self):
        self.engine.interface.enable_monitor()
        scan_thread = threading.Thread(target=self._background_scan, daemon=True)
        scan_thread.start()

        with Live(self.layout, refresh_per_second=4, screen=True):
            while not self._stop.is_set():
                self._update()
                time.sleep(0.25)
