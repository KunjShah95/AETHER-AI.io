"""
File Watcher - Automated file watching and action triggering
Monitor files/directories and execute commands on changes
"""

import os
import time
import subprocess
import threading
from typing import Dict, List, Optional, Callable
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime

console = Console()

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    Observer = None
    FileSystemEventHandler = None


class FileWatchHandler(FileSystemEventHandler):
    """Handler for file system events"""
    
    def __init__(self, watch_id: str, action: str, callback: Callable):
        self.watch_id = watch_id
        self.action = action
        self.callback = callback
        self.last_triggered = {}
        self.debounce_seconds = 0.5  # Prevent rapid firing
    
    def _should_trigger(self, path: str) -> bool:
        """Check if enough time has passed since last trigger"""
        now = time.time()
        last = self.last_triggered.get(path, 0)
        if now - last > self.debounce_seconds:
            self.last_triggered[path] = now
            return True
        return False
    
    def on_modified(self, event: FileSystemEvent):
        """Called when a file is modified"""
        if not event.is_directory and self._should_trigger(event.src_path):
            self.callback(self.watch_id, 'modified', event.src_path)
    
    def on_created(self, event: FileSystemEvent):
        """Called when a file is created"""
        if not event.is_directory and self._should_trigger(event.src_path):
            self.callback(self.watch_id, 'created', event.src_path)
    
    def on_deleted(self, event: FileSystemEvent):
        """Called when a file is deleted"""
        if not event.is_directory:
            self.callback(self.watch_id, 'deleted', event.src_path)
    
    def on_moved(self, event: FileSystemEvent):
        """Called when a file is moved"""
        if not event.is_directory:
            self.callback(self.watch_id, 'moved', event.src_path)


class FileWatcher:
    """File watching and automation system"""
    
    def __init__(self):
        self.watchers = {}
        self.observers = {}
        self.next_id = 1
        self.logs = []
        self.max_logs = 100
        
        if not WATCHDOG_AVAILABLE:
            console.print("[yellow]⚠️ watchdog not installed. Install with: pip install watchdog[/yellow]")
    
    def _execute_action(self, watch_id: str, event_type: str, file_path: str):
        """Execute the configured action when file changes"""
        if watch_id not in self.watchers:
            return
        
        watcher = self.watchers[watch_id]
        action = watcher['action']
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Log the event
        log_entry = {
            'timestamp': timestamp,
            'watch_id': watch_id,
            'event': event_type,
            'file': file_path,
            'action': action
        }
        self.logs.append(log_entry)
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)
        
        console.print(f"\n[cyan]👁️ File {event_type}:[/cyan] {file_path}")
        console.print(f"[yellow]⚡ Executing:[/yellow] {action}")
        
        try:
            # Replace placeholders in action
            action_cmd = action.replace('{file}', file_path)
            action_cmd = action_cmd.replace('{filename}', os.path.basename(file_path))
            action_cmd = action_cmd.replace('{dir}', os.path.dirname(file_path))
            
            # Execute the action
            result = subprocess.run(
                action_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                console.print(f"[green]✅ Action completed successfully[/green]")
                if result.stdout:
                    console.print(f"Output: {result.stdout[:500]}")
            else:
                console.print(f"[red]❌ Action failed (exit code: {result.returncode})[/red]")
                if result.stderr:
                    console.print(f"Error: {result.stderr[:500]}")
        
        except subprocess.TimeoutExpired:
            console.print("[red]❌ Action timed out (30s limit)[/red]")
        except Exception as e:
            console.print(f"[red]❌ Action error: {str(e)}[/red]")
    
    def start(self, path: str, action: str, patterns: Optional[List[str]] = None) -> str:
        """Start watching a path and execute action on changes"""
        if not WATCHDOG_AVAILABLE:
            return "❌ watchdog not installed. Install with: pip install watchdog"
        
        try:
            watch_path = Path(path).resolve()
            
            if not watch_path.exists():
                return f"❌ Path does not exist: {path}"
            
            watch_id = str(self.next_id)
            self.next_id += 1
            
            # Create event handler
            handler = FileWatchHandler(
                watch_id=watch_id,
                action=action,
                callback=self._execute_action
            )
            
            # Create and start observer
            observer = Observer()
            observer.schedule(handler, str(watch_path), recursive=True)
            observer.start()
            
            # Store watcher info
            self.watchers[watch_id] = {
                'path': str(watch_path),
                'action': action,
                'patterns': patterns or [],
                'started_at': datetime.now().isoformat(),
                'status': 'active'
            }
            self.observers[watch_id] = observer
            
            return f"✅ Watching {watch_path}\n" \
                   f"   ID: {watch_id}\n" \
                   f"   Action: {action}\n" \
                   f"   Use /watch stop {watch_id} to stop"
        
        except Exception as e:
            return f"❌ Error starting watcher: {str(e)}"
    
    def stop(self, watch_id: str) -> str:
        """Stop watching a path"""
        if watch_id not in self.watchers:
            return f"❌ Watcher {watch_id} not found"
        
        try:
            if watch_id in self.observers:
                observer = self.observers[watch_id]
                observer.stop()
                observer.join(timeout=5)
                del self.observers[watch_id]
            
            self.watchers[watch_id]['status'] = 'stopped'
            path = self.watchers[watch_id]['path']
            
            return f"✅ Stopped watching {path} (ID: {watch_id})"
        
        except Exception as e:
            return f"❌ Error stopping watcher: {str(e)}"
    
    def list_watchers(self) -> str:
        """List all active watchers"""
        if not self.watchers:
            return "📋 No active file watchers"
        
        table = Table(title="👁️ Active File Watchers", show_header=True, header_style="bold cyan")
        table.add_column("ID", style="white")
        table.add_column("Path", style="green")
        table.add_column("Action", style="yellow")
        table.add_column("Status", style="cyan")
        table.add_column("Started", style="dim")
        
        for watch_id, watcher in self.watchers.items():
            status_icon = "🟢" if watcher['status'] == 'active' else "🔴"
            table.add_row(
                watch_id,
                watcher['path'][:40] + "..." if len(watcher['path']) > 40 else watcher['path'],
                watcher['action'][:30] + "..." if len(watcher['action']) > 30 else watcher['action'],
                f"{status_icon} {watcher['status']}",
                watcher['started_at']
            )
        
        console.print(table)
        return ""
    
    def show_logs(self, limit: int = 20) -> str:
        """Show recent file watch logs"""
        if not self.logs:
            return "📜 No file watch logs yet"
        
        table = Table(title="📜 File Watch Logs", show_header=True, header_style="bold cyan")
        table.add_column("Time", style="dim")
        table.add_column("Watch ID", style="white")
        table.add_column("Event", style="yellow")
        table.add_column("File", style="green")
        
        for log in reversed(self.logs[-limit:]):
            table.add_row(
                log['timestamp'],
                log['watch_id'],
                log['event'],
                os.path.basename(log['file'])
            )
        
        console.print(table)
        return ""
    
    def stop_all(self) -> str:
        """Stop all watchers"""
        if not self.watchers:
            return "❌ No active watchers to stop"
        
        count = 0
        for watch_id in list(self.watchers.keys()):
            if self.watchers[watch_id]['status'] == 'active':
                self.stop(watch_id)
                count += 1
        
        return f"✅ Stopped {count} watcher(s)"
    
    # Predefined convenience methods
    
    def watch_compile(self, path: str, compiler: str = "auto") -> str:
        """Watch and auto-compile on changes"""
        if compiler == "auto":
            # Detect compiler based on file extension
            if path.endswith('.ts'):
                action = "tsc {file}"
            elif path.endswith('.scss') or path.endswith('.sass'):
                action = "sass {file} {file}.css"
            elif path.endswith('.coffee'):
                action = "coffee -c {file}"
            else:
                return "❌ Cannot auto-detect compiler. Specify compiler explicitly"
        else:
            action = f"{compiler} {{file}}"
        
        return self.start(path, action)
    
    def watch_lint(self, path: str, linter: str = "auto") -> str:
        """Watch and auto-lint on changes"""
        if linter == "auto":
            # Detect linter based on file type
            if path.endswith('.py'):
                action = "flake8 {file}"
            elif path.endswith('.js') or path.endswith('.ts'):
                action = "eslint {file}"
            else:
                return "❌ Cannot auto-detect linter. Specify linter explicitly"
        else:
            action = f"{linter} {{file}}"
        
        return self.start(path, action)
    
    def watch_test(self, path: str, test_cmd: str = "auto") -> str:
        """Watch and auto-run tests on changes"""
        if test_cmd == "auto":
            # Detect test command based on project
            if os.path.exists('package.json'):
                action = "npm test"
            elif os.path.exists('pytest.ini'):
                action = "pytest {file}"
            else:
                return "❌ Cannot auto-detect test command. Specify command explicitly"
        else:
            action = test_cmd
        
        return self.start(path, action)
    
    def watch_reload(self, path: str, port: int = 3000) -> str:
        """Watch and trigger browser reload"""
        # This would typically work with a dev server
        action = f"echo 'File changed: {{file}}' && curl -X POST http://localhost:{port}/reload"
        return self.start(path, action)
    
    def watch_deploy(self, path: str, deploy_cmd: str) -> str:
        """Watch and auto-deploy on changes"""
        return self.start(path, deploy_cmd)
    
    def watch_format(self, path: str, formatter: str = "auto") -> str:
        """Watch and auto-format on changes"""
        if formatter == "auto":
            if path.endswith('.py'):
                action = "black {file}"
            elif path.endswith('.js') or path.endswith('.ts'):
                action = "prettier --write {file}"
            else:
                return "❌ Cannot auto-detect formatter. Specify formatter explicitly"
        else:
            action = f"{formatter} {{file}}"
        
        return self.start(path, action)
    
    def get_status(self) -> str:
        """Get watcher status summary"""
        active = sum(1 for w in self.watchers.values() if w['status'] == 'active')
        total = len(self.watchers)
        log_count = len(self.logs)
        
        return f"👁️ File Watcher Status:\n" \
               f"   Active: {active}/{total}\n" \
               f"   Total Events: {log_count}\n" \
               f"   Watchdog: {'✅ Available' if WATCHDOG_AVAILABLE else '❌ Not installed'}"
