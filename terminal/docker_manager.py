import logging
from typing import List, Dict, Optional
from datetime import datetime

try:
    import docker
except ImportError:
    docker = None

class DockerManager:
    def __init__(self):
        self.enabled = docker is not None
        self.client = None
        if self.enabled:
            try:
                self.client = docker.from_env()
                self.client.ping()
            except Exception as e:
                logging.warning(f"Docker available but not running/accessible: {e}")
                self.enabled = False

    def list_containers(self, all: bool = False) -> List[Dict]:
        if not self.enabled:
            return []
        try:
            containers = self.client.containers.list(all=all)
            return [{
                'id': c.short_id,
                'name': c.name,
                'status': c.status,
                'image': c.image.tags[0] if c.image.tags else c.image.id[:12],
                'ports': c.ports
            } for c in containers]
        except Exception as e:
            logging.error(f"Docker List Error: {e}")
            return []

    def start_container(self, container_id: str) -> str:
        if not self.enabled:
            return "❌ Docker not available"
        try:
            container = self.client.containers.get(container_id)
            container.start()
            return f"✅ Container {container.name} started"
        except Exception as e:
            return f"❌ Error starting container: {e}"

    def stop_container(self, container_id: str) -> str:
        if not self.enabled:
            return "❌ Docker not available"
        try:
            container = self.client.containers.get(container_id)
            container.stop()
            return f"✅ Container {container.name} stopped"
        except Exception as e:
            return f"❌ Error stopping container: {e}"

    def get_logs(self, container_id: str, tail: int = 100) -> str:
        if not self.enabled:
            return "❌ Docker not available"
        try:
            container = self.client.containers.get(container_id)
            return container.logs(tail=tail).decode('utf-8')
        except Exception as e:
            return f"❌ Error getting logs: {e}"

    def get_info(self) -> str:
        if not self.enabled:
            return "Docker not available or not running."
        try:
            info = self.client.info()
            return f"Docker v{info['ServerVersion']} | Containers: {info['Containers']} | Images: {info['Images']}"
        except Exception as e:
            return f"Error getting Docker info: {e}"
