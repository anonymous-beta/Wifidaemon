"""Demon ASCII banner."""
from rich.console import Console

BANNER = """
[bold magenta]
           __        ___ _     _
 _      _  \\ \\      / (_) | __| | ___  ___| |_ _ __ ___  _ __
| | | | |  \\ \\ /\\ / /| | |/ _` |/ _ \\/ __| __| '__/ _ \\| '_ \\
| |_| | |   \\ V  V / | | | (_| |  __/\\__ \\ |_| | | (_) | | | |
 \\__,_|_|    \\_/\\_/  |_|_|\\__,_|\\___||___/\\__|_|  \\___/|_| |_|
[/bold magenta]
[bold red]                      WiFiDAEMON v2.0.0-DEMON[/bold red]
              [dim]"Silent Guardian of the Airwaves"[/dim]
"""


def print_banner():
    console = Console()
    console.print(BANNER)
