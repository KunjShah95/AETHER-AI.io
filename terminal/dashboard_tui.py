from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Log, Digits
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.reactive import reactive
from datetime import datetime
import psutil
import platform
import time

class SystemMonitor(Static):
    """Displays system information."""
    
    cpu_usage = reactive(0.0)
    memory_usage = reactive(0.0)

    def on_mount(self) -> None:
        self.set_interval(1, self.update_stats)

    def update_stats(self) -> None:
        self.cpu_usage = psutil.cpu_percent()
        self.memory_usage = psutil.virtual_memory().percent

    def watch_cpu_usage(self, usage: float) -> None:
        self.update_display()

    def update_display(self) -> None:
        self.update(f"""
[b]System Status[/b]
OS: {platform.system()} {platform.release()}
CPU: {self.cpu_usage}%
RAM: {self.memory_usage}%
        """)

class Clock(Static):
    """Displays the time."""
    
    time = reactive(datetime.now().strftime("%H:%M:%S"))

    def on_mount(self) -> None:
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        self.time = datetime.now().strftime("%H:%M:%S")
        self.update(f"[b]{self.time}[/b]")

class NexusDashboard(App):
    """A Textual app to manage Nexus AI."""

    CSS = """
    Screen {
        layout: grid;
        grid-size: 2 2;
        grid-gutter: 1;
        padding: 1;
    }
    
    .box {
        height: 100%;
        border: solid green;
        padding: 1;
    }

    SystemMonitor {
        height: 100%;
    }
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode"), ("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(SystemMonitor(classes="box"), classes="box")
        yield Container(Clock(classes="box"), classes="box")
        yield Log(id="activity_log", classes="box")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(Log).write_line("Nexus AI Dashboard Initialized...")
        self.query_one(Log).write_line("Monitoring system...")

if __name__ == "__main__":
    app = NexusDashboard()
    app.run()
