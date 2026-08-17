"""
DemonLogger: rich, colored logging with file output.
"""
import os
from datetime import datetime
from rich.console import Console
from rich.theme import Theme

demon_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "demon": "bold magenta",
    "scan": "bright_blue",
    "attack": "bold red",
})


class DemonLogger:
    def __init__(self, verbose=False, log_dir="logs"):
        self.verbose = verbose
        self.console = Console(theme=demon_theme)
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.log_file = os.path.join(log_dir, f"daemon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    def _write(self, level, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] [{level}] {msg}"
        with open(self.log_file, "a") as f:
            f.write(line + "\n")

    def info(self, msg):
        self._write("INFO", msg)
        self.console.print(f"[info][👿 INFO][/info] {msg}")

    def warning(self, msg):
        self._write("WARN", msg)
        self.console.print(f"[warning][⚠️ WARN][/warning] {msg}")

    def error(self, msg):
        self._write("ERROR", msg)
        self.console.print(f"[error][💀 ERROR][/error] {msg}")

    def success(self, msg):
        self._write("SUCCESS", msg)
        self.console.print(f"[success][✅ SUCCESS][/success] {msg}")

    def demon(self, msg):
        self._write("DEMON", msg)
        self.console.print(f"[demon][👹 DEMON][/demon] {msg}")

    def scan_log(self, msg):
        self._write("SCAN", msg)
        self.console.print(f"[scan][📡 SCAN][/scan] {msg}")

    def attack_log(self, msg):
        self._write("ATTACK", msg)
        self.console.print(f"[attack][⚔️ ATTACK][/attack] {msg}")
