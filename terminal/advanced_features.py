#!/usr/bin/env python3
"""
Advanced Features Module for NEXUS AI Terminal
Contains utility functions for enhanced development, testing, and integration features
"""

import os
import sys
import subprocess
import tempfile
import json
import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class AdvancedFeatures:
    """Container for advanced terminal features"""

    @staticmethod
    def execute_python_code(code: str, timeout: int = 30) -> Tuple[str, str, int]:
        """
        Execute Python code in isolation and return results

        Args:
            code: Python code to execute
            timeout: Execution timeout in seconds

        Returns:
            Tuple of (stdout, stderr, return_code)
        """
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name

            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )

            # Clean up
            os.unlink(temp_file)

            return result.stdout, result.stderr, result.returncode

        except subprocess.TimeoutExpired:
            return "", "Code execution timed out", -1
        except Exception as e:
            return "", f"Error executing code: {str(e)}", -1

    @staticmethod
    def setup_debug_session(filename: str) -> str:
        """
        Set up a debug session for a Python file

        Args:
            filename: Path to Python file to debug

        Returns:
            Debug setup instructions
        """
        if not os.path.exists(filename):
            return f"File not found: {filename}"

        try:
            with open(filename, 'r') as f:
                code = f.read()

            # Create debug version with breakpoint
            debug_code = "import pdb\npdb.set_trace()\n" + code

            debug_file = filename.replace('.py', '_debug.py')
            with open(debug_file, 'w') as f:
                f.write(debug_code)

            return f"Debug file created: {debug_file}\nRun: python {debug_file}"

        except Exception as e:
            return f"Error setting up debug: {str(e)}"

    @staticmethod
    def profile_code(filename: str) -> str:
        """
        Profile Python code performance

        Args:
            filename: Path to Python file to profile

        Returns:
            Performance profile results
        """
        try:
            import cProfile
            import pstats

            if not os.path.exists(filename):
                return f"File not found: {filename}"

            # Profile the code execution
            pr = cProfile.Profile()
            pr.enable()

            # Execute the file in a separate process to avoid conflicts
            result = subprocess.run(
                [sys.executable, filename],
                capture_output=True,
                text=True,
                timeout=60
            )

            pr.disable()

            # Get profiling stats
            import io
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
            ps.print_stats(15)  # Top 15 functions

            profile_output = s.getvalue()

            execution_info = ""
            if result.returncode == 0:
                execution_info = f"✅ Code executed successfully\n"
            else:
                execution_info = f"❌ Code execution failed\n{result.stderr}\n"

            return f"{execution_info}📊 Performance Profile:\n{profile_output}"

        except subprocess.TimeoutExpired:
            return "❌ Profiling timed out (60s limit)"
        except Exception as e:
            return f"❌ Error profiling: {str(e)}"

    @staticmethod
    def run_tests(filename: str) -> str:
        """
        Run unit tests on a Python file

        Args:
            filename: Path to Python file to test

        Returns:
            Test results
        """
        try:
            if not os.path.exists(filename):
                return f"❌ File not found: {filename}"

            # Run pytest
            result = subprocess.run(
                [sys.executable, '-m', 'pytest', filename, '-v', '--tb=short'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(filename) or '.'
            )

            if result.returncode == 0:
                return f"✅ Tests passed:\n{result.stdout}"
            else:
                return f"❌ Tests failed:\n{result.stdout}\n{result.stderr}"

        except Exception as e:
            return f"❌ Error running tests: {str(e)}"

    @staticmethod
    def lint_code(filename: str) -> str:
        """
        Lint Python code for style and potential issues

        Args:
            filename: Path to Python file to lint

        Returns:
            Linting results
        """
        try:
            if not os.path.exists(filename):
                return f"❌ File not found: {filename}"

            # Run flake8
            result = subprocess.run(
                [sys.executable, '-m', 'flake8', filename, '--max-line-length=100'],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(filename) or '.'
            )

            if result.returncode == 0:
                return "✅ No linting issues found"
            else:
                return f"⚠️ Linting issues:\n{result.stdout}"

        except Exception as e:
            return f"❌ Error running linter: {str(e)}"

    @staticmethod
    def test_api_endpoint(url: str) -> str:
        """
        Test a REST API endpoint

        Args:
            url: API endpoint URL

        Returns:
            API test results
        """
        try:
            import requests
            from urllib.parse import urlparse

            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            # Make request with timeout
            response = requests.get(url, timeout=10)

            result = "🌐 API Test Results:\n"
            result += f"URL: {url}\n"
            result += f"Status: {response.status_code}\n"
            result += f"Response Time: {response.elapsed.total_seconds()}s\n"
            result += f"Content-Type: {response.headers.get('content-type', 'N/A')}\n"
            result += f"Content Length: {len(response.text)} chars\n"

            if response.status_code == 200:
                result += "✅ Success!\n"
                # Try to format JSON response
                try:
                    if 'json' in response.headers.get('content-type', '').lower():
                        json_data = response.json()
                        result += f"JSON Response: {json.dumps(json_data, indent=2)[:500]}..."
                    else:
                        result += f"Response Preview: {response.text[:200]}..."
                except:
                    result += f"Response Preview: {response.text[:200]}..."
            else:
                result += f"❌ Error: {response.reason}"

            return result

        except requests.exceptions.RequestException as e:
            return f"❌ API test failed: {str(e)}"
        except Exception as e:
            return f"❌ Error testing API: {str(e)}"

    @staticmethod
    def connect_database(db_type: str, connection_string: str) -> str:
        """
        Test database connection

        Args:
            db_type: Type of database (postgres, mysql, mongodb)
            connection_string: Database connection string

        Returns:
            Connection test results
        """
        try:
            if db_type.lower() == "postgres":
                import psycopg2
                conn = psycopg2.connect(connection_string)
                conn.close()
                return "✅ PostgreSQL connection successful"

            elif db_type.lower() == "mysql":
                import pymysql
                # Parse connection string for pymysql
                # This is a simplified example - real implementation would parse properly
                conn = pymysql.connect(connection_string)
                conn.close()
                return "✅ MySQL connection successful"

            elif db_type.lower() == "mongodb":
                from pymongo import MongoClient
                client = MongoClient(connection_string)
                # Test connection
                client.admin.command('ping')
                client.close()
                return "✅ MongoDB connection successful"

            elif db_type.lower() == "redis":
                import redis
                r = redis.from_url(connection_string)
                r.ping()
                r.close()
                return "✅ Redis connection successful"

            else:
                return f"❌ Unsupported database type: {db_type}"

        except ImportError as e:
            return f"❌ Database driver not installed: {str(e)}"
        except Exception as e:
            return f"❌ Database connection failed: {str(e)}"

    @staticmethod
    def create_project_template(project_type: str) -> str:
        """
        Create a project template

        Args:
            project_type: Type of project to create

        Returns:
            Project creation results
        """
        project_templates = {
            "react": {
                "package.json": '''{
  "name": "my-react-app",
  "version": "1.0.0",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  }
}''',
                "src/App.js": '''import React from 'react';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Hello React!</h1>
        <p>Built with NEXUS AI Terminal</p>
      </header>
    </div>
  );
}

export default App;''',
                "public/index.html": '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>React App</title>
</head>
<body>
  <div id="root"></div>
</body>
</html>'''
            },

            "django": {
                "requirements.txt": "Django==4.2.7\ndjango-cors-headers==4.3.1",
                "manage.py": "# Django management script - will be created by django-admin",
                "myapp/views.py": '''from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello Django! Built with NEXUS AI Terminal")

def home(request):
    return render(request, 'home.html')''',
                "myapp/models.py": '''from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name''',
                "README.md": "# Django Project\n\nCreated with NEXUS AI Terminal"
            },

            "fastapi": {
                "main.py": '''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="NEXUS API", description="Built with NEXUS AI Terminal")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Hello FastAPI!", "built_with": "NEXUS AI Terminal"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}''',
                "requirements.txt": "fastapi==0.104.1\nuvicorn==0.24.0",
                "README.md": "# FastAPI Project\n\nCreated with NEXUS AI Terminal\n\nRun with: `uvicorn main:app --reload`"
            },

            "flask": {
                "app.py": '''from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello Flask!",
        "built_with": "NEXUS AI Terminal"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(debug=True)''',
                "requirements.txt": "Flask==3.0.0",
                "README.md": "# Flask Project\n\nCreated with NEXUS AI Terminal\n\nRun with: `python app.py`"
            }
        }

        if project_type not in project_templates:
            return f"❌ Unknown project type. Available: {', '.join(project_templates.keys())}"

        try:
            project_dir = f"{project_type}_project"
            os.makedirs(project_dir, exist_ok=True)

            for file_path, content in project_templates[project_type].items():
                full_path = os.path.join(project_dir, file_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write(content)

            return f"✅ {project_type.upper()} project created in ./{project_dir}/\n\nNext steps:\n1. cd {project_dir}\n2. Install dependencies: pip install -r requirements.txt (if applicable)\n3. Run the project as indicated in README.md"

        except Exception as e:
            return f"❌ Error creating project: {str(e)}"

    @staticmethod
    def explore_directory(path: str = ".") -> str:
        """
        Explore directory contents

        Args:
            path: Directory path to explore

        Returns:
            Directory listing
        """
        try:
            current_dir = Path(path)
            if not current_dir.exists():
                return f"❌ Directory not found: {path}"

            items = []
            total_files = 0
            total_dirs = 0
            total_size = 0

            for item in current_dir.iterdir():
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        total_size += size
                        total_files += 1
                        size_str = AdvancedFeatures._format_file_size(size)
                        items.append(f"📄 {item.name} ({size_str})")
                    elif item.is_dir():
                        total_dirs += 1
                        items.append(f"📁 {item.name}/")
                except (OSError, PermissionError):
                    items.append(f"🔒 {item.name} (access denied)")

            output = f"📂 Directory: {current_dir.absolute()}\n"
            output += f"📊 Summary: {total_files} files, {total_dirs} directories, {AdvancedFeatures._format_file_size(total_size)} total\n\n"

            # Sort items: directories first, then files
            dirs = [item for item in items if item.startswith("📁")]
            files = [item for item in items if not item.startswith("📁") and not item.startswith("🔒")]
            locked = [item for item in items if item.startswith("🔒")]

            all_items = dirs + files + locked

            if len(all_items) <= 30:
                output += "\n".join(all_items)
            else:
                output += "\n".join(all_items[:25])
                output += f"\n... and {len(all_items) - 25} more items"

            return output

        except Exception as e:
            return f"❌ Error exploring directory: {str(e)}"

    @staticmethod
    def _format_file_size(size_bytes: int) -> str:
        """Format file size in human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return ".1f"
            size_bytes /= 1024.0
        return ".1f"

    @staticmethod
    def monitor_system() -> str:
        """
        Monitor system resources

        Returns:
            System monitoring information
        """
        try:
            import psutil
            import platform

            # CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()

            # Memory information
            memory = psutil.virtual_memory()

            # Disk information
            disk = psutil.disk_usage('/')

            # Network information
            net = psutil.net_io_counters()

            output = "📊 System Monitor:\n\n"
            output += f"🖥️ OS: {platform.system()} {platform.release()}\n"
            output += f"🔧 CPU: {cpu_count} cores, {cpu_percent}% used"
            if cpu_freq:
                output += f", {cpu_freq.current:.0f}MHz"
            output += "\n"

            output += f"💾 Memory: {memory.percent}% used "
            output += f"({AdvancedFeatures._format_file_size(memory.used)} / {AdvancedFeatures._format_file_size(memory.total)})\n"

            output += f"💿 Disk: {disk.percent}% used "
            output += f"({AdvancedFeatures._format_file_size(disk.used)} / {AdvancedFeatures._format_file_size(disk.total)})\n"

            output += f"🌐 Network: {AdvancedFeatures._format_file_size(net.bytes_sent)} sent, "
            output += f"{AdvancedFeatures._format_file_size(net.bytes_recv)} received\n"

            # Process information
            process_count = len(psutil.pids())
            output += f"⚙️ Processes: {process_count} running\n"

            return output

        except ImportError:
            return "❌ System monitoring requires 'psutil' package. Install with: pip install psutil"
        except Exception as e:
            return f"❌ Error monitoring system: {str(e)}"

    @staticmethod
    def analyze_logs(directory: str = ".") -> str:
        """
        Analyze log files in a directory

        Args:
            directory: Directory to scan for log files

        Returns:
            Log analysis results
        """
        try:
            log_files = []
            for file in os.listdir(directory):
                if file.endswith(('.log', '.txt')) and os.path.isfile(os.path.join(directory, file)):
                    log_files.append(file)

            if not log_files:
                return "❌ No log files found in current directory"

            analysis = {}
            for log_file in log_files[:5]:  # Limit to 5 files
                try:
                    with open(os.path.join(directory, log_file), 'r', errors='ignore') as f:
                        content = f.read(10000)  # Read first 10KB

                    lines = content.split('\n')
                    total_lines = len(lines)

                    # Analyze different log levels
                    errors = len([l for l in lines if 'ERROR' in l.upper() or 'ERR' in l.upper()])
                    warnings = len([l for l in lines if 'WARNING' in l.upper() or 'WARN' in l.upper()])
                    info = len([l for l in lines if 'INFO' in l.upper()])

                    # Find recent entries (last 100 lines)
                    recent_lines = lines[-100:] if len(lines) > 100 else lines
                    recent_errors = len([l for l in recent_lines if 'ERROR' in l.upper() or 'ERR' in l.upper()])

                    analysis[log_file] = {
                        'total_lines': total_lines,
                        'errors': errors,
                        'warnings': warnings,
                        'info': info,
                        'recent_errors': recent_errors
                    }

                except Exception as e:
                    analysis[log_file] = {'error': str(e)}

            output = "📋 Log Analysis:\n\n"
            for file, stats in analysis.items():
                if 'error' in stats:
                    output += f"📄 {file}: Error reading file - {stats['error']}\n"
                else:
                    output += f"📄 {file}:\n"
                    output += f"  📊 Total Lines: {stats['total_lines']}\n"
                    output += f"  ❌ Errors: {stats['errors']}\n"
                    output += f"  ⚠️ Warnings: {stats['warnings']}\n"
                    output += f"  ℹ️ Info: {stats['info']}\n"
                    output += f"  🔥 Recent Errors: {stats['recent_errors']}\n"
                output += "\n"

            return output

        except Exception as e:
            return f"❌ Error analyzing logs: {str(e)}"
