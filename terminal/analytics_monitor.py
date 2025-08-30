#!/usr/bin/env python3
"""
Analytics & Monitoring Module for NEXUS AI Terminal
Provides usage analytics, system monitoring, and performance metrics
"""

import os
import json
import time
import psutil
import platform
import threading
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import socket
import requests

class AnalyticsMonitor:
    """Handles analytics, monitoring, and performance tracking"""

    def __init__(self):
        self.analytics_db_path = os.path.expanduser("~/.nexus/analytics.db")
        self.monitoring_data = {}
        self.performance_metrics = {}
        self.usage_stats = defaultdict(int)
        self.error_analytics = []
        self.system_health = {}
        self._load_analytics()
        self.monitoring_active = False
        self.monitoring_thread = None

    def _load_analytics(self):
        """Load analytics database"""
        try:
            if os.path.exists(self.analytics_db_path):
                with open(self.analytics_db_path, 'r') as f:
                    data = json.load(f)
                    self.usage_stats = defaultdict(int, data.get("usage_stats", {}))
                    self.error_analytics = data.get("error_analytics", [])
                    self.performance_metrics = data.get("performance_metrics", {})
        except Exception as e:
            print(f"Warning: Could not load analytics database: {e}")

    def _save_analytics(self):
        """Save analytics database"""
        try:
            os.makedirs(os.path.dirname(self.analytics_db_path), exist_ok=True)
            data = {
                "usage_stats": dict(self.usage_stats),
                "error_analytics": self.error_analytics[-1000:],  # Keep last 1000 errors
                "performance_metrics": self.performance_metrics,
                "last_updated": time.time()
            }
            with open(self.analytics_db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save analytics database: {e}")

    def track_usage(self, feature: str, user: str = "anonymous"):
        """Track feature usage"""
        key = f"{user}:{feature}"
        self.usage_stats[key] += 1
        self.usage_stats[f"total:{feature}"] += 1
        self._save_analytics()

    def track_error(self, error_type: str, error_message: str, context: str = ""):
        """Track errors for analytics"""
        error_entry = {
            "type": error_type,
            "message": error_message,
            "context": context,
            "timestamp": time.time(),
            "date": datetime.now().isoformat()
        }
        self.error_analytics.append(error_entry)
        self._save_analytics()

    def get_usage_stats(self, days: int = 7) -> Dict:
        """Get usage statistics"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        # Filter recent usage
        recent_usage = {}
        for key, count in self.usage_stats.items():
            if ":" in key and key.startswith(("total:", "anonymous:", "admin:")):
                recent_usage[key] = count

        # Group by feature
        feature_stats = defaultdict(int)
        user_stats = defaultdict(int)

        for key, count in recent_usage.items():
            if key.startswith("total:"):
                feature = key.replace("total:", "")
                feature_stats[feature] = count
            else:
                user, feature = key.split(":", 1)
                user_stats[user] += count

        return {
            "feature_usage": dict(feature_stats),
            "user_activity": dict(user_stats),
            "total_interactions": sum(feature_stats.values()),
            "period_days": days
        }

    def get_error_analytics(self, days: int = 7) -> Dict:
        """Get error analytics"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        recent_errors = [
            error for error in self.error_analytics
            if error.get("timestamp", 0) > cutoff_time
        ]

        # Group errors by type
        error_types = defaultdict(int)
        error_trends = defaultdict(list)

        for error in recent_errors:
            error_type = error.get("type", "unknown")
            error_types[error_type] += 1

            # Group by hour for trend analysis
            error_time = datetime.fromtimestamp(error["timestamp"])
            hour_key = error_time.strftime("%Y-%m-%d %H")
            error_trends[hour_key].append(error)

        return {
            "total_errors": len(recent_errors),
            "error_types": dict(error_types),
            "most_common_error": max(error_types.items(), key=lambda x: x[1]) if error_types else None,
            "error_trends": {k: len(v) for k, v in error_trends.items()},
            "period_days": days
        }

    def start_monitoring(self):
        """Start system monitoring"""
        if self.monitoring_active:
            return "Monitoring already active"

        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()

        return "✅ System monitoring started"

    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        return "✅ System monitoring stopped"

    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                self.monitoring_data = self._collect_system_metrics()
                time.sleep(30)  # Update every 30 seconds
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(60)

    def _collect_system_metrics(self) -> Dict:
        """Collect comprehensive system metrics"""
        try:
            metrics = {
                "timestamp": time.time(),
                "cpu": {
                    "percent": psutil.cpu_percent(interval=1),
                    "count": psutil.cpu_count(),
                    "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None
                },
                "memory": {
                    "total": psutil.virtual_memory().total,
                    "available": psutil.virtual_memory().available,
                    "percent": psutil.virtual_memory().percent,
                    "used": psutil.virtual_memory().used
                },
                "disk": {
                    "total": psutil.disk_usage('/').total,
                    "used": psutil.disk_usage('/').used,
                    "free": psutil.disk_usage('/').free,
                    "percent": psutil.disk_usage('/').percent
                },
                "network": {
                    "bytes_sent": psutil.net_io_counters().bytes_sent,
                    "bytes_recv": psutil.net_io_counters().bytes_recv,
                    "packets_sent": psutil.net_io_counters().packets_sent,
                    "packets_recv": psutil.net_io_counters().packets_recv
                },
                "system": {
                    "os": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "architecture": platform.machine(),
                    "hostname": socket.gethostname(),
                    "uptime": time.time() - psutil.boot_time()
                },
                "processes": {
                    "total": len(psutil.pids()),
                    "running": len([p for p in psutil.process_iter() if p.status() == 'running'])
                }
            }

            return metrics

        except Exception as e:
            return {"error": f"Failed to collect metrics: {str(e)}"}

    def get_current_metrics(self) -> Dict:
        """Get current system metrics"""
        if not self.monitoring_data:
            self.monitoring_data = self._collect_system_metrics()

        return self.monitoring_data

    def get_performance_metrics(self) -> Dict:
        """Get performance metrics and analysis"""
        metrics = self.get_current_metrics()

        if "error" in metrics:
            return metrics

        # Analyze performance
        analysis = {
            "cpu_status": "good" if metrics["cpu"]["percent"] < 80 else "high",
            "memory_status": "good" if metrics["memory"]["percent"] < 85 else "high",
            "disk_status": "good" if metrics["disk"]["percent"] < 90 else "high",
            "overall_health": "healthy"
        }

        # Determine overall health
        if (metrics["cpu"]["percent"] > 90 or
            metrics["memory"]["percent"] > 95 or
            metrics["disk"]["percent"] > 95):
            analysis["overall_health"] = "critical"
        elif (metrics["cpu"]["percent"] > 80 or
              metrics["memory"]["percent"] > 85 or
              metrics["disk"]["percent"] > 85):
            analysis["overall_health"] = "warning"

        return {
            "metrics": metrics,
            "analysis": analysis,
            "recommendations": self._generate_recommendations(analysis)
        }

    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        if analysis["cpu_status"] == "high":
            recommendations.append("High CPU usage detected. Consider closing unnecessary applications.")
        if analysis["memory_status"] == "high":
            recommendations.append("High memory usage. Consider closing memory-intensive applications.")
        if analysis["disk_status"] == "high":
            recommendations.append("Low disk space. Consider cleaning up unnecessary files.")
        if analysis["overall_health"] == "critical":
            recommendations.append("System health is critical. Immediate action recommended.")
        if analysis["overall_health"] == "warning":
            recommendations.append("System performance is degraded. Monitor closely.")

        return recommendations

    def network_diagnostics(self) -> Dict:
        """Perform network diagnostics"""
        try:
            diagnostics = {
                "connectivity": {},
                "speed": {},
                "latency": {},
                "timestamp": time.time()
            }

            # Test connectivity to common services
            test_urls = [
                ("Google", "https://www.google.com"),
                ("GitHub", "https://www.github.com"),
                ("PyPI", "https://pypi.org"),
                ("HuggingFace", "https://huggingface.co")
            ]

            for name, url in test_urls:
                try:
                    start_time = time.time()
                    response = requests.get(url, timeout=10)
                    latency = (time.time() - start_time) * 1000  # Convert to ms

                    diagnostics["connectivity"][name] = {
                        "status": "reachable" if response.status_code == 200 else "unreachable",
                        "latency_ms": round(latency, 2),
                        "status_code": response.status_code
                    }
                except Exception as e:
                    diagnostics["connectivity"][name] = {
                        "status": "unreachable",
                        "error": str(e)
                    }

            # Basic speed test (download small file)
            try:
                start_time = time.time()
                response = requests.get("https://httpbin.org/uuid", timeout=10)
                download_time = time.time() - start_time
                size_bytes = len(response.content)

                speed_bps = size_bytes / download_time
                speed_mbps = (speed_bps * 8) / (1024 * 1024)  # Convert to Mbps

                diagnostics["speed"] = {
                    "download_mbps": round(speed_mbps, 2),
                    "latency_ms": round(download_time * 1000, 2)
                }
            except Exception as e:
                diagnostics["speed"] = {"error": f"Speed test failed: {str(e)}"}

            return diagnostics

        except Exception as e:
            return {"error": f"Network diagnostics failed: {str(e)}"}

    def analyze_logs(self, log_directory: str = ".", pattern: str = "*.log") -> Dict:
        """Analyze log files for issues and patterns"""
        try:
            import glob

            log_files = glob.glob(os.path.join(log_directory, pattern))
            if not log_files:
                return {"error": "No log files found"}

            analysis = {
                "files_analyzed": len(log_files),
                "total_lines": 0,
                "error_count": 0,
                "warning_count": 0,
                "info_count": 0,
                "recent_errors": [],
                "patterns": {},
                "timestamp": time.time()
            }

            for log_file in log_files[:10]:  # Limit to 10 files
                try:
                    with open(log_file, 'r', errors='ignore') as f:
                        lines = f.readlines()
                        analysis["total_lines"] += len(lines)

                        for i, line in enumerate(lines):
                            line_lower = line.lower()

                            if any(keyword in line_lower for keyword in ['error', 'err', 'exception', 'fail']):
                                analysis["error_count"] += 1
                                if i > len(lines) - 50:  # Recent errors (last 50 lines)
                                    analysis["recent_errors"].append({
                                        "file": os.path.basename(log_file),
                                        "line": i + 1,
                                        "content": line.strip()[:200]
                                    })

                            elif any(keyword in line_lower for keyword in ['warning', 'warn']):
                                analysis["warning_count"] += 1

                            elif 'info' in line_lower:
                                analysis["info_count"] += 1

                except Exception as e:
                    continue

            # Limit recent errors to 10
            analysis["recent_errors"] = analysis["recent_errors"][:10]

            return analysis

        except Exception as e:
            return {"error": f"Log analysis failed: {str(e)}"}

    def health_check(self) -> Dict:
        """Perform comprehensive system health check"""
        try:
            health = {
                "overall_status": "healthy",
                "checks": {},
                "timestamp": time.time(),
                "recommendations": []
            }

            # CPU Health
            cpu_percent = psutil.cpu_percent(interval=1)
            health["checks"]["cpu"] = {
                "status": "good" if cpu_percent < 80 else "warning" if cpu_percent < 90 else "critical",
                "value": cpu_percent,
                "message": f"CPU usage: {cpu_percent}%"
            }

            # Memory Health
            memory = psutil.virtual_memory()
            health["checks"]["memory"] = {
                "status": "good" if memory.percent < 80 else "warning" if memory.percent < 90 else "critical",
                "value": memory.percent,
                "message": f"Memory usage: {memory.percent}%"
            }

            # Disk Health
            disk = psutil.disk_usage('/')
            health["checks"]["disk"] = {
                "status": "good" if disk.percent < 85 else "warning" if disk.percent < 95 else "critical",
                "value": disk.percent,
                "message": f"Disk usage: {disk.percent}%"
            }

            # Network Health
            try:
                response = requests.get("https://httpbin.org/status/200", timeout=5)
                health["checks"]["network"] = {
                    "status": "good" if response.status_code == 200 else "critical",
                    "value": response.elapsed.total_seconds(),
                    "message": f"Network latency: {response.elapsed.total_seconds():.2f}s"
                }
            except:
                health["checks"]["network"] = {
                    "status": "critical",
                    "value": None,
                    "message": "Network connectivity issues"
                }

            # Determine overall status
            statuses = [check["status"] for check in health["checks"].values()]
            if "critical" in statuses:
                health["overall_status"] = "critical"
            elif "warning" in statuses:
                health["overall_status"] = "warning"

            # Generate recommendations
            for component, check in health["checks"].items():
                if check["status"] == "critical":
                    if component == "cpu":
                        health["recommendations"].append("Critical CPU usage. Close unnecessary applications.")
                    elif component == "memory":
                        health["recommendations"].append("Critical memory usage. Restart memory-intensive applications.")
                    elif component == "disk":
                        health["recommendations"].append("Critical disk usage. Free up disk space immediately.")
                    elif component == "network":
                        health["recommendations"].append("Network connectivity issues. Check internet connection.")

            return health

        except Exception as e:
            return {"error": f"Health check failed: {str(e)}"}</content>
<parameter name="filePath">c:\NEXUS-AI.io\terminal\analytics_monitor.py
