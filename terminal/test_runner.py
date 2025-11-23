"""
Test Runner - Automated testing tool for multiple frameworks
Supports pytest, jest, mocha, and more
"""

import subprocess
import json
import os
import re
from typing import Dict, List, Optional, Tuple
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax

console = Console()


class TestRunner:
    """Universal test runner for multiple testing frameworks"""
    
    def __init__(self):
        self.frameworks = {
            'pytest': {'cmd': 'pytest', 'pattern': 'test_*.py', 'coverage': '--cov'},
            'jest': {'cmd': 'jest', 'pattern': '*.test.js', 'coverage': '--coverage'},
            'mocha': {'cmd': 'mocha', 'pattern': '*.test.js', 'coverage': '--coverage'},
            'vitest': {'cmd': 'vitest', 'pattern': '*.test.ts', 'coverage': '--coverage'},
            'unittest': {'cmd': 'python -m unittest', 'pattern': 'test_*.py', 'coverage': None},
        }
        self.detected_framework = self._detect_framework()
        self.last_results = None
    
    def _detect_framework(self) -> str:
        """Auto-detect testing framework from current directory"""
        if os.path.exists('package.json'):
            try:
                with open('package.json', 'r') as f:
                    pkg = json.load(f)
                    deps = {**pkg.get('dependencies', {}), **pkg.get('devDependencies', {})}
                    
                    if 'vitest' in deps:
                        return 'vitest'
                    elif 'jest' in deps or '@jest' in str(deps):
                        return 'jest'
                    elif 'mocha' in deps:
                        return 'mocha'
            except:
                pass
        
        if os.path.exists('pytest.ini') or os.path.exists('pyproject.toml'):
            return 'pytest'
        
        # Check for test files
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    return 'pytest'
                if file.endswith('.test.js') or file.endswith('.test.ts'):
                    return 'jest'
        
        return 'pytest'  # default
    
    def _run_command(self, command: List[str], capture_output: bool = True) -> Tuple[int, str, str]:
        """Run shell command and return (returncode, stdout, stderr)"""
        try:
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=300,  # 5 minutes max
                shell=os.name == 'nt'  # Use shell on Windows
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return 1, "", "Tests timed out after 5 minutes"
        except Exception as e:
            return 1, "", str(e)
    
    def run_tests(self, pattern: Optional[str] = None, framework: Optional[str] = None, 
                  verbose: bool = False, watch: bool = False) -> str:
        """Run tests"""
        framework = framework or self.detected_framework
        
        if framework not in self.frameworks:
            return f"❌ Unknown framework: {framework}\n   Supported: {', '.join(self.frameworks.keys())}"
        
        fw_config = self.frameworks[framework]
        cmd = fw_config['cmd'].split()
        
        # Add pattern if provided
        if pattern:
            cmd.append(pattern)
        
        # Add verbose flag
        if verbose:
            if framework in ['pytest']:
                cmd.append('-v')
            elif framework in ['jest', 'vitest']:
                cmd.append('--verbose')
        
        # Add watch mode
        if watch:
            if framework in ['jest', 'vitest']:
                cmd.append('--watch')
            elif framework == 'pytest':
                cmd.extend(['-f'])  # pytest-watch needed
                return "💡 For watch mode in pytest, install: pip install pytest-watch\n   Then use: ptw"
        
        console.print(f"\n🧪 Running tests via {framework}...")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task = progress.add_task(f"Running tests...", total=None)
            code, stdout, stderr = self._run_command(cmd)
        
        # Parse and display results
        self.last_results = {
            'framework': framework,
            'returncode': code,
            'stdout': stdout,
            'stderr': stderr
        }
        
        return self._format_results(code, stdout, stderr, framework)
    
    def _format_results(self, code: int, stdout: str, stderr: str, framework: str) -> str:
        """Format test results for display"""
        output = []
        
        if code == 0:
            output.append("✅ [bold green]All tests passed![/bold green]")
        else:
            output.append("❌ [bold red]Some tests failed[/bold red]")
        
        # Extract test counts
        if framework == 'pytest':
            # Parse pytest output
            match = re.search(r'(\d+) passed', stdout)
            passed = match.group(1) if match else '0'
            match = re.search(r'(\d+) failed', stdout)
            failed = match.group(1) if match else '0'
            match = re.search(r'in ([\d.]+s)', stdout)
            duration = match.group(1) if match else 'N/A'
            
            output.append(f"\nTests: {passed} passed, {failed} failed")
            output.append(f"Duration: {duration}")
        
        elif framework in ['jest', 'vitest']:
            # Parse Jest/Vitest output
            match = re.search(r'Tests:\s+(\d+) passed', stdout)
            passed = match.group(1) if match else '0'
            match = re.search(r'(\d+) failed', stdout)
            failed = match.group(1) if match else '0'
            match = re.search(r'Time:\s+([\d.]+\s*s)', stdout)
            duration = match.group(1) if match else 'N/A'
            
            output.append(f"\nTests: {passed} passed, {failed} failed")
            output.append(f"Duration: {duration}")
        
        # Show output
        console.print("\n".join(output))
        
        # Show detailed output in syntax-highlighted panel
        if stdout:
            syntax = Syntax(stdout[:2000], "text", theme="monokai", line_numbers=False)
            console.print("\n📋 Test Output:", style="bold cyan")
            console.print(syntax)
        
        if stderr and code != 0:
            console.print("\n⚠️ Errors:", style="bold red")
            console.print(stderr[:1000])
        
        return ""
    
    def run_coverage(self, framework: Optional[str] = None) -> str:
        """Run tests with coverage report"""
        framework = framework or self.detected_framework
        
        if framework not in self.frameworks:
            return f"❌ Unknown framework: {framework}"
        
        fw_config = self.frameworks[framework]
        coverage_flag = fw_config.get('coverage')
        
        if not coverage_flag:
            return f"❌ Coverage not configured for {framework}"
        
        cmd = fw_config['cmd'].split()
        cmd.append(coverage_flag)
        
        if framework == 'pytest':
            cmd.extend(['--cov-report', 'term-missing'])
        
        console.print(f"\n📊 Running coverage via {framework}...")
        
        code, stdout, stderr = self._run_command(cmd)
        
        if code == 0 or stdout:
            console.print("\n✅ Coverage Report:")
            syntax = Syntax(stdout[:3000], "text", theme="monokai")
            console.print(syntax)
            return ""
        else:
            return f"❌ Coverage failed\n{stderr[:500]}"
    
    def watch_mode(self, framework: Optional[str] = None) -> str:
        """Start test watch mode"""
        framework = framework or self.detected_framework
        
        if framework in ['jest', 'vitest']:
            return self.run_tests(framework=framework, watch=True)
        elif framework == 'pytest':
            return "💡 For pytest watch mode, install pytest-watch:\n   pip install pytest-watch\n   Then run: ptw"
        else:
            return f"❌ Watch mode not available for {framework}"
    
    def run_specific(self, test_path: str, framework: Optional[str] = None) -> str:
        """Run specific test file or function"""
        framework = framework or self.detected_framework
        
        return self.run_tests(pattern=test_path, framework=framework, verbose=True)
    
    def run_parallel(self, num_workers: int = 4, framework: Optional[str] = None) -> str:
        """Run tests in parallel"""
        framework = framework or self.detected_framework
        
        if framework not in self.frameworks:
            return f"❌ Unknown framework: {framework}"
        
        cmd = self.frameworks[framework]['cmd'].split()
        
        if framework == 'pytest':
            cmd.extend(['-n', str(num_workers)])
            console.print("💡 Pytest parallel requires pytest-xdist: pip install pytest-xdist")
        elif framework in ['jest', 'vitest']:
            cmd.extend(['--maxWorkers', str(num_workers)])
        else:
            return f"❌ Parallel execution not configured for {framework}"
        
        console.print(f"\n⚡ Running tests in parallel ({num_workers} workers)...")
        
        code, stdout, stderr = self._run_command(cmd)
        return self._format_results(code, stdout, stderr, framework)
    
    def list_tests(self, framework: Optional[str] = None) -> str:
        """List all available tests"""
        framework = framework or self.detected_framework
        
        try:
            if framework == 'pytest':
                code, stdout, stderr = self._run_command(['pytest', '--collect-only', '-q'])
                if code == 0 or stdout:
                    return f"📋 Available Tests:\n{stdout[:2000]}"
            elif framework in ['jest', 'vitest']:
                code, stdout, stderr = self._run_command([framework, '--listTests'])
                if code == 0 or stdout:
                    return f"📋 Available Tests:\n{stdout[:2000]}"
            else:
                return f"❌ Test listing not implemented for {framework}"
        except Exception as e:
            return f"❌ Error listing tests: {str(e)}"
    
    def generate_report(self, output_format: str = 'html', framework: Optional[str] = None) -> str:
        """Generate test report"""
        framework = framework or self.detected_framework
        
        if framework == 'pytest':
            cmd = ['pytest', '--html=test_report.html', '--self-contained-html']
            console.print("\n📄 Generating HTML report...")
            code, stdout, stderr = self._run_command(cmd)
            
            if code == 0 or os.path.exists('test_report.html'):
                return "✅ Test report generated: test_report.html"
            else:
                return "💡 Install pytest-html: pip install pytest-html"
        
        elif framework in ['jest', 'vitest']:
            return "💡 Use --coverage for Jest/Vitest reports"
        
        else:
            return f"❌ Report generation not implemented for {framework}"
    
    def get_last_results(self) -> str:
        """Get last test results"""
        if not self.last_results:
            return "❌ No test results available"
        
        return f"📊 Last Test Run ({self.last_results['framework']}):\n" \
               f"Exit Code: {self.last_results['returncode']}\n" \
               f"Output:\n{self.last_results['stdout'][:1000]}"
    
    def get_current_framework(self) -> str:
        """Get currently detected testing framework"""
        return f"🧪 Detected testing framework: {self.detected_framework}"
