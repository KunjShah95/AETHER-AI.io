"""
Package Manager - Unified package management for npm, pip, cargo, and more
Simplifies dependency installation and management across different ecosystems
"""

import subprocess
import json
import os
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class PackageManager:
    """Universal package manager for multiple ecosystems"""
    
    def __init__(self):
        self.package_managers = {
            'npm': {'cmd': 'npm', 'install': 'install', 'uninstall': 'uninstall', 'update': 'update'},
            'pip': {'cmd': 'pip', 'install': 'install', 'uninstall': 'uninstall', 'update': 'install --upgrade'},
            'cargo': {'cmd': 'cargo', 'install': 'install', 'uninstall': 'uninstall', 'update': 'update'},
            'yarn': {'cmd': 'yarn', 'install': 'add', 'uninstall': 'remove', 'update': 'upgrade'},
            'pnpm': {'cmd': 'pnpm', 'install': 'add', 'uninstall': 'remove', 'update': 'update'},
        }
        self.detected_pm = self._detect_package_manager()
    
    def _detect_package_manager(self) -> str:
        """Auto-detect package manager from current directory"""
        if os.path.exists('package.json'):
            if os.path.exists('pnpm-lock.yaml'):
                return 'pnpm'
            elif os.path.exists('yarn.lock'):
                return 'yarn'
            else:
                return 'npm'
        elif os.path.exists('requirements.txt') or os.path.exists('setup.py') or os.path.exists('pyproject.toml'):
            return 'pip'
        elif os.path.exists('Cargo.toml'):
            return 'cargo'
        return 'npm'  # default
    
    def _run_command(self, command: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
        """Run shell command and return (returncode, stdout, stderr)"""
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=300  # 5 minutes max
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Command timed out after 5 minutes"
        except Exception as e:
            return 1, "", str(e)
    
    def search(self, package_name: str, pm: Optional[str] = None) -> str:
        """Search for packages"""
        pm = pm or self.detected_pm
        
        try:
            if pm == 'npm' or pm == 'yarn' or pm == 'pnpm':
                code, stdout, stderr = self._run_command(['npm', 'search', package_name, '--json'])
                if code == 0:
                    try:
                        results = json.loads(stdout)
                        if not results:
                            return f"📦 No packages found for '{package_name}'"
                        
                        table = Table(title=f"📦 NPM Package Search: '{package_name}'", 
                                    show_header=True, header_style="bold cyan")
                        table.add_column("Package", style="white")
                        table.add_column("Version", style="yellow")
                        table.add_column("Description", style="green")
                        
                        for pkg in results[:10]:  # Show top 10
                            table.add_row(
                                pkg.get('name', 'Unknown'),
                                pkg.get('version', 'N/A'),
                                pkg.get('description', 'No description')[:60]
                            )
                        
                        console.print(table)
                        return ""
                    except json.JSONDecodeError:
                        return stdout
            
            elif pm == 'pip':
                code, stdout, stderr = self._run_command(['pip', 'search', package_name])
                if code == 0:
                    return f"📦 PyPI Search Results:\n{stdout[:2000]}"
                else:
                    # pip search is currently disabled, use alternative
                    return f"💡 Tip: Search PyPI at https://pypi.org/search/?q={package_name}"
            
            else:
                return f"❌ Search not implemented for {pm}"
        
        except Exception as e:
            return f"❌ Search error: {str(e)}"
    
    def install(self, package_name: str, pm: Optional[str] = None, dev: bool = False) -> str:
        """Install a package"""
        pm = pm or self.detected_pm
        
        if pm not in self.package_managers:
            return f"❌ Unknown package manager: {pm}"
        
        pm_config = self.package_managers[pm]
        cmd = [pm_config['cmd'], pm_config['install'], package_name]
        
        # Add dev flag if needed
        if dev and pm in ['npm', 'yarn', 'pnpm']:
            cmd.append('--save-dev')
        elif dev and pm == 'pip':
            cmd.insert(1, '-e')  # pip install -e for editable/dev
        
        console.print(f"\n📦 Installing {package_name} via {pm}...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task(f"Installing {package_name}...", total=None)
            code, stdout, stderr = self._run_command(cmd)
        
        if code == 0:
            return f"✅ Successfully installed {package_name}\n{stdout[:500]}"
        else:
            return f"❌ Installation failed\n{stderr[:500]}"
    
    def uninstall(self, package_name: str, pm: Optional[str] = None) -> str:
        """Uninstall a package"""
        pm = pm or self.detected_pm
        
        if pm not in self.package_managers:
            return f"❌ Unknown package manager: {pm}"
        
        pm_config = self.package_managers[pm]
        cmd = [pm_config['cmd'], pm_config['uninstall'], package_name]
        
        console.print(f"\n🗑️ Uninstalling {package_name} via {pm}...")
        
        code, stdout, stderr = self._run_command(cmd)
        
        if code == 0:
            return f"✅ Successfully uninstalled {package_name}"
        else:
            return f"❌ Uninstallation failed\n{stderr[:500]}"
    
    def update(self, package_name: Optional[str] = None, pm: Optional[str] = None) -> str:
        """Update package(s)"""
        pm = pm or self.detected_pm
        
        if pm not in self.package_managers:
            return f"❌ Unknown package manager: {pm}"
        
        pm_config = self.package_managers[pm]
        
        if package_name:
            cmd = pm_config['update'].split() + [package_name]
        else:
            # Update all packages
            if pm == 'npm':
                cmd = ['npm', 'update']
            elif pm == 'pip':
                cmd = ['pip', 'list', '--outdated', '--format=json']
            elif pm == 'yarn':
                cmd = ['yarn', 'upgrade']
            elif pm == 'pnpm':
                cmd = ['pnpm', 'update']
            else:
                return f"❌ Bulk update not implemented for {pm}"
        
        cmd.insert(0, pm_config['cmd'])
        
        console.print(f"\n🔄 Updating packages via {pm}...")
        
        code, stdout, stderr = self._run_command(cmd)
        
        if code == 0:
            return f"✅ Update completed\n{stdout[:1000]}"
        else:
            return f"❌ Update failed\n{stderr[:500]}"
    
    def list_outdated(self, pm: Optional[str] = None) -> str:
        """List outdated packages"""
        pm = pm or self.detected_pm
        
        try:
            if pm == 'npm':
                code, stdout, stderr = self._run_command(['npm', 'outdated', '--json'])
                if code == 0 or stdout:
                    try:
                        outdated = json.loads(stdout) if stdout else {}
                        if not outdated:
                            return "✅ All packages are up to date!"
                        
                        table = Table(title="📦 Outdated NPM Packages", 
                                    show_header=True, header_style="bold cyan")
                        table.add_column("Package", style="white")
                        table.add_column("Current", style="yellow")
                        table.add_column("Wanted", style="green")
                        table.add_column("Latest", style="cyan")
                        
                        for pkg, info in outdated.items():
                            table.add_row(
                                pkg,
                                info.get('current', 'N/A'),
                                info.get('wanted', 'N/A'),
                                info.get('latest', 'N/A')
                            )
                        
                        console.print(table)
                        return ""
                    except json.JSONDecodeError:
                        return stdout
            
            elif pm == 'pip':
                code, stdout, stderr = self._run_command(['pip', 'list', '--outdated'])
                if code == 0:
                    if "Package" not in stdout:
                        return "✅ All packages are up to date!"
                    return f"📦 Outdated PIP Packages:\n{stdout}"
            
            elif pm == 'yarn':
                code, stdout, stderr = self._run_command(['yarn', 'outdated'])
                if code == 0 or stdout:
                    return f"📦 Outdated Yarn Packages:\n{stdout[:2000]}"
            
            else:
                return f"❌ Outdated check not implemented for {pm}"
        
        except Exception as e:
            return f"❌ Error checking outdated packages: {str(e)}"
    
    def audit(self, pm: Optional[str] = None) -> str:
        """Security audit of packages"""
        pm = pm or self.detected_pm
        
        try:
            if pm in ['npm', 'yarn', 'pnpm']:
                cmd = [pm, 'audit']
                console.print(f"\n🔍 Running security audit via {pm}...")
                
                code, stdout, stderr = self._run_command(cmd)
                
                if code == 0:
                    return f"✅ Security Audit Complete\n{stdout[:2000]}"
                else:
                    # npm audit returns non-zero if vulnerabilities found
                    return f"⚠️ Vulnerabilities Found\n{stdout[:2000]}"
            
            elif pm == 'pip':
                # Use pip-audit if available
                code, stdout, stderr = self._run_command(['pip-audit'])
                if "command not found" in stderr or "not recognized" in stderr:
                    return "💡 Install pip-audit for security scanning: pip install pip-audit"
                return stdout[:2000] if code == 0 else f"❌ Audit failed\n{stderr[:500]}"
            
            else:
                return f"❌ Security audit not available for {pm}"
        
        except Exception as e:
            return f"❌ Audit error: {str(e)}"
    
    def clean_cache(self, pm: Optional[str] = None) -> str:
        """Clean package manager cache"""
        pm = pm or self.detected_pm
        
        try:
            if pm == 'npm':
                code, stdout, stderr = self._run_command(['npm', 'cache', 'clean', '--force'])
            elif pm == 'yarn':
                code, stdout, stderr = self._run_command(['yarn', 'cache', 'clean'])
            elif pm == 'pnpm':
                code, stdout, stderr = self._run_command(['pnpm', 'store', 'prune'])
            elif pm == 'pip':
                code, stdout, stderr = self._run_command(['pip', 'cache', 'purge'])
            else:
                return f"❌ Cache clean not implemented for {pm}"
            
            if code == 0:
                return f"✅ {pm} cache cleaned successfully"
            else:
                return f"❌ Cache clean failed\n{stderr[:500]}"
        
        except Exception as e:
            return f"❌ Error cleaning cache: {str(e)}"
    
    def list_scripts(self, pm: Optional[str] = None) -> str:
        """List available package.json scripts"""
        pm = pm or self.detected_pm
        
        if pm not in ['npm', 'yarn', 'pnpm']:
            return "❌ Scripts are only available for npm/yarn/pnpm projects"
        
        try:
            if not os.path.exists('package.json'):
                return "❌ No package.json found in current directory"
            
            with open('package.json', 'r') as f:
                pkg = json.load(f)
            
            scripts = pkg.get('scripts', {})
            if not scripts:
                return "📋 No scripts defined in package.json"
            
            table = Table(title="📜 Available Scripts", show_header=True, header_style="bold cyan")
            table.add_column("Script", style="white")
            table.add_column("Command", style="green")
            
            for name, command in scripts.items():
                table.add_row(name, command)
            
            console.print(table)
            return f"\n💡 Run with: {pm} run <script_name>"
        
        except Exception as e:
            return f"❌ Error listing scripts: {str(e)}"
    
    def info(self, package_name: str, pm: Optional[str] = None) -> str:
        """Get package information"""
        pm = pm or self.detected_pm
        
        try:
            if pm in ['npm', 'yarn', 'pnpm']:
                code, stdout, stderr = self._run_command(['npm', 'view', package_name, '--json'])
                if code == 0:
                    try:
                        info = json.loads(stdout)
                        output = [
                            f"\n📦 Package: {info.get('name', 'Unknown')}",
                            f"Version: {info.get('version', 'N/A')}",
                            f"Description: {info.get('description', 'No description')}",
                            f"License: {info.get('license', 'Unknown')}",
                            f"Author: {info.get('author', {}).get('name', 'Unknown') if isinstance(info.get('author'), dict) else info.get('author', 'Unknown')}",
                            f"Homepage: {info.get('homepage', 'N/A')}",
                            f"Repository: {info.get('repository', {}).get('url', 'N/A') if isinstance(info.get('repository'), dict) else 'N/A'}",
                        ]
                        return "\n".join(output)
                    except json.JSONDecodeError:
                        return stdout[:1000]
            
            elif pm == 'pip':
                code, stdout, stderr = self._run_command(['pip', 'show', package_name])
                if code == 0:
                    return f"📦 Package Information:\n{stdout}"
                else:
                    return f"❌ Package not found: {package_name}"
            
            else:
                return f"❌ Info not implemented for {pm}"
        
        except Exception as e:
            return f"❌ Error getting package info: {str(e)}"
    
    def get_current_pm(self) -> str:
        """Get currently detected package manager"""
        return f"📦 Detected package manager: {self.detected_pm}"
