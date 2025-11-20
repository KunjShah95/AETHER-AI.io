import socket
import time
import logging
import subprocess
import platform

class NetworkTools:
    def __init__(self):
        pass

    def check_port(self, host: str, port: int, timeout: int = 2) -> str:
        """Check if a port is open on a host."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                result = s.connect_ex((host, port))
                if result == 0:
                    return f"✅ Port {port} on {host} is OPEN"
                else:
                    return f"❌ Port {port} on {host} is CLOSED"
        except Exception as e:
            return f"⚠️ Error checking port: {e}"

    def ping(self, host: str) -> str:
        """Ping a host."""
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', host]
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
            return f"📡 Ping results for {host}:\n{output}"
        except subprocess.CalledProcessError as e:
            return f"❌ Ping failed: {e.output}"
        except Exception as e:
            return f"⚠️ Error executing ping: {e}"

    def get_local_ip(self) -> str:
        """Get local IP address."""
        try:
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            return f"🏠 Local IP: {ip} (Hostname: {hostname})"
        except Exception as e:
            return f"⚠️ Error getting local IP: {e}"

    def scan_common_ports(self, host: str = "localhost") -> str:
        """Scan common ports on a host."""
        common_ports = [21, 22, 80, 443, 3306, 5432, 8000, 8080, 3000]
        results = []
        results.append(f"🔍 Scanning common ports on {host}...")
        for port in common_ports:
            res = self.check_port(host, port, timeout=0.5)
            if "OPEN" in res:
                results.append(res)
        
        if len(results) == 1:
            return f"🔍 No common ports found open on {host}."
        return "\n".join(results)
