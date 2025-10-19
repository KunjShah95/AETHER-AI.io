"""
NEXUS AI Terminal - Integration Hub
Connect and manage external services and APIs
"""

import os
import json
import time
import threading
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import hashlib
import hmac
import base64
from urllib.parse import urlencode, quote
import subprocess
import re

class IntegrationHub:
    """Central hub for managing external service integrations"""

    def __init__(self):
        self.integrations_file = "integrations.json"
        self.services = {}
        self.webhooks = {}
        self.api_keys = {}
        self.connection_status = {}
        self.load_integrations()

        # Supported services
        self.supported_services = {
            "github": {
                "name": "GitHub",
                "description": "Version control and collaboration platform",
                "auth_type": "token",
                "base_url": "https://api.github.com",
                "features": ["repos", "issues", "pull_requests", "webhooks"]
            },
            "slack": {
                "name": "Slack",
                "description": "Team communication platform",
                "auth_type": "token",
                "base_url": "https://slack.com/api",
                "features": ["messages", "channels", "users", "webhooks"]
            },
            "discord": {
                "name": "Discord",
                "description": "Gaming and community platform",
                "auth_type": "bot_token",
                "base_url": "https://discord.com/api",
                "features": ["messages", "channels", "users", "webhooks"]
            },
            "trello": {
                "name": "Trello",
                "description": "Project management tool",
                "auth_type": "token",
                "base_url": "https://api.trello.com/1",
                "features": ["boards", "cards", "lists", "webhooks"]
            },
            "jira": {
                "name": "Jira",
                "description": "Issue tracking and project management",
                "auth_type": "basic",
                "base_url": "https://api.atlassian.com",
                "features": ["issues", "projects", "users", "webhooks"]
            },
            "notion": {
                "name": "Notion",
                "description": "All-in-one workspace",
                "auth_type": "token",
                "base_url": "https://api.notion.com/v1",
                "features": ["pages", "databases", "users", "webhooks"]
            },
            "linear": {
                "name": "Linear",
                "description": "Issue tracking for software teams",
                "auth_type": "token",
                "base_url": "https://api.linear.app/graphql",
                "features": ["issues", "projects", "teams", "webhooks"]
            },
            "figma": {
                "name": "Figma",
                "description": "Design and prototyping tool",
                "auth_type": "token",
                "base_url": "https://api.figma.com/v1",
                "features": ["files", "projects", "teams", "comments"]
            },
            "stripe": {
                "name": "Stripe",
                "description": "Payment processing platform",
                "auth_type": "secret_key",
                "base_url": "https://api.stripe.com/v1",
                "features": ["payments", "customers", "subscriptions", "webhooks"]
            },
            "twilio": {
                "name": "Twilio",
                "description": "Communication APIs (SMS, Voice, Email)",
                "auth_type": "api_key",
                "base_url": "https://api.twilio.com",
                "features": ["sms", "calls", "emails", "webhooks"]
            }
        }

    def load_integrations(self):
        """Load saved integrations from file"""
        try:
            if os.path.exists(self.integrations_file):
                with open(self.integrations_file, 'r') as f:
                    data = json.load(f)
                    self.services = data.get('services', {})
                    self.webhooks = data.get('webhooks', {})
                    self.api_keys = data.get('api_keys', {})
        except Exception as e:
            print(f"Warning: Could not load integrations: {e}")

    def save_integrations(self):
        """Save integrations to file"""
        try:
            data = {
                'services': self.services,
                'webhooks': self.webhooks,
                'api_keys': self.api_keys
            }
            with open(self.integrations_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            return f"❌ Error saving integrations: {e}"
        return "✅ Integrations saved successfully"

    def add_service(self, service_name: str, config: Dict) -> str:
        """Add a new service integration"""
        if service_name not in self.supported_services:
            return f"❌ Service '{service_name}' not supported. Available: {', '.join(self.supported_services.keys())}"

        service_config = self.supported_services[service_name].copy()
        service_config.update(config)
        service_config['added_at'] = datetime.now().isoformat()
        service_config['status'] = 'configured'

        self.services[service_name] = service_config
        self.save_integrations()

        return f"✅ Service '{service_name}' added successfully"

    def remove_service(self, service_name: str) -> str:
        """Remove a service integration"""
        if service_name not in self.services:
            return f"❌ Service '{service_name}' not found"

        del self.services[service_name]
        if service_name in self.api_keys:
            del self.api_keys[service_name]

        self.save_integrations()
        return f"✅ Service '{service_name}' removed successfully"

    def test_connection(self, service_name: str) -> str:
        """Test connection to a service"""
        if service_name not in self.services:
            return f"❌ Service '{service_name}' not configured"

        service = self.services[service_name]

        try:
            if service_name == "github":
                return self._test_github_connection(service)
            elif service_name == "slack":
                return self._test_slack_connection(service)
            elif service_name == "discord":
                return self._test_discord_connection(service)
            elif service_name == "trello":
                return self._test_trello_connection(service)
            elif service_name == "jira":
                return self._test_jira_connection(service)
            elif service_name == "notion":
                return self._test_notion_connection(service)
            else:
                return f"⚠️ Connection test not implemented for {service_name}"

        except Exception as e:
            self.connection_status[service_name] = 'failed'
            return f"❌ Connection failed: {str(e)}"

    def _test_github_connection(self, service: Dict) -> str:
        """Test GitHub API connection"""
        token = service.get('token')
        if not token:
            return "❌ GitHub token not configured"

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.get('https://api.github.com/user', headers=headers, timeout=10)

        if response.status_code == 200:
            user_data = response.json()
            self.connection_status['github'] = 'connected'
            return f"✅ GitHub connected as {user_data.get('login', 'unknown user')}"
        else:
            self.connection_status['github'] = 'failed'
            return f"❌ GitHub connection failed: {response.status_code}"

    def _test_slack_connection(self, service: Dict) -> str:
        """Test Slack API connection"""
        token = service.get('token')
        if not token:
            return "❌ Slack token not configured"

        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post('https://slack.com/api/auth.test', headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                self.connection_status['slack'] = 'connected'
                return f"✅ Slack connected to workspace {data.get('team', 'unknown')}"
            else:
                return f"❌ Slack auth failed: {data.get('error', 'unknown error')}"
        else:
            self.connection_status['slack'] = 'failed'
            return f"❌ Slack connection failed: {response.status_code}"

    def _test_discord_connection(self, service: Dict) -> str:
        """Test Discord API connection"""
        token = service.get('token')
        if not token:
            return "❌ Discord token not configured"

        headers = {'Authorization': f'Bot {token}'}
        response = requests.get('https://discord.com/api/users/@me', headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            self.connection_status['discord'] = 'connected'
            return f"✅ Discord connected as {data.get('username', 'unknown bot')}"
        else:
            self.connection_status['discord'] = 'failed'
            return f"❌ Discord connection failed: {response.status_code}"

    def _test_trello_connection(self, service: Dict) -> str:
        """Test Trello API connection"""
        api_key = service.get('api_key')
        token = service.get('token')

        if not api_key or not token:
            return "❌ Trello API key and token not configured"

        url = f"https://api.trello.com/1/members/me?key={api_key}&token={token}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            self.connection_status['trello'] = 'connected'
            return f"✅ Trello connected as {data.get('fullName', 'unknown user')}"
        else:
            self.connection_status['trello'] = 'failed'
            return f"❌ Trello connection failed: {response.status_code}"

    def _test_jira_connection(self, service: Dict) -> str:
        """Test Jira API connection"""
        email = service.get('email')
        api_token = service.get('api_token')
        domain = service.get('domain')

        if not all([email, api_token, domain]):
            return "❌ Jira email, API token, and domain not configured"

        auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()
        headers = {'Authorization': f'Basic {auth}'}

        url = f"https://{domain}.atlassian.net/rest/api/3/myself"
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            self.connection_status['jira'] = 'connected'
            return f"✅ Jira connected as {data.get('displayName', 'unknown user')}"
        else:
            self.connection_status['jira'] = 'failed'
            return f"❌ Jira connection failed: {response.status_code}"

    def _test_notion_connection(self, service: Dict) -> str:
        """Test Notion API connection"""
        token = service.get('token')
        if not token:
            return "❌ Notion token not configured"

        headers = {
            'Authorization': f'Bearer {token}',
            'Notion-Version': '2022-06-28'
        }

        response = requests.get('https://api.notion.com/v1/users', headers=headers, timeout=10)

        if response.status_code == 200:
            self.connection_status['notion'] = 'connected'
            return "✅ Notion connected successfully"
        else:
            self.connection_status['notion'] = 'failed'
            return f"❌ Notion connection failed: {response.status_code}"

    def list_services(self) -> str:
        """List all configured services"""
        if not self.services:
            return "📋 No services configured. Use /integrate add [service] to add one."

        output = "🔗 Configured Services:\n\n"
        for name, service in self.services.items():
            status = self.connection_status.get(name, 'unknown')
            status_icon = {"connected": "🟢", "failed": "🔴", "unknown": "⚪"}.get(status, "⚪")
            output += f"{status_icon} {name.upper()}: {service.get('name', name)}\n"
            output += f"   📝 {service.get('description', 'No description')}\n"
            output += f"   🔧 Status: {status}\n"
            output += f"   📅 Added: {service.get('added_at', 'Unknown')[:10]}\n\n"

        return output

    def list_supported_services(self) -> str:
        """List all supported services"""
        output = "🚀 Supported Services:\n\n"
        for name, service in self.supported_services.items():
            configured = "✅" if name in self.services else "❌"
            output += f"{configured} {name.upper()}: {service['name']}\n"
            output += f"   📝 {service['description']}\n"
            output += f"   🔐 Auth: {service['auth_type']}\n"
            output += f"   ⚡ Features: {', '.join(service['features'])}\n\n"

        return output

    def get_service_info(self, service_name: str) -> str:
        """Get detailed information about a service"""
        if service_name not in self.supported_services:
            return f"❌ Service '{service_name}' not supported"

        service = self.supported_services[service_name]
        configured = service_name in self.services

        output = f"ℹ️ Service Information: {service_name.upper()}\n\n"
        output += f"📝 Name: {service['name']}\n"
        output += f"📖 Description: {service['description']}\n"
        output += f"🔐 Authentication: {service['auth_type']}\n"
        output += f"🌐 Base URL: {service['base_url']}\n"
        output += f"⚡ Features: {', '.join(service['features'])}\n"
        output += f"✅ Configured: {'Yes' if configured else 'No'}\n"

        if configured:
            config = self.services[service_name]
            output += f"📅 Added: {config.get('added_at', 'Unknown')[:10]}\n"
            status = self.connection_status.get(service_name, 'unknown')
            output += f"🔗 Status: {status}\n"

        return output

    def execute_service_action(self, service_name: str, action: str, **params) -> str:
        """Execute an action on a configured service"""
        if service_name not in self.services:
            return f"❌ Service '{service_name}' not configured"

        if service_name not in self.connection_status or self.connection_status[service_name] != 'connected':
            return f"❌ Service '{service_name}' not connected. Use /integrate test {service_name} first"

        try:
            if service_name == "github":
                return self._execute_github_action(action, self.services[service_name], **params)
            elif service_name == "slack":
                return self._execute_slack_action(action, self.services[service_name], **params)
            elif service_name == "discord":
                return self._execute_discord_action(action, self.services[service_name], **params)
            else:
                return f"⚠️ Action execution not implemented for {service_name}"

        except Exception as e:
            return f"❌ Action failed: {str(e)}"

    def _execute_github_action(self, action: str, service: Dict, **params) -> str:
        """Execute GitHub-specific actions"""
        token = service.get('token')
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        if action == "list_repos":
            response = requests.get('https://api.github.com/user/repos', headers=headers, params={'per_page': 10})
            if response.status_code == 200:
                repos = response.json()
                output = "📚 Your GitHub Repositories:\n\n"
                for repo in repos[:10]:
                    output += f"📁 {repo['name']}\n"
                    output += f"   🌟 {repo['stargazers_count']} stars | 🍴 {repo['forks_count']} forks\n"
                    output += f"   📝 {repo['description'] or 'No description'}\n\n"
                return output
            else:
                return f"❌ Failed to fetch repos: {response.status_code}"

        elif action == "create_issue":
            repo = params.get('repo')
            title = params.get('title')
            body = params.get('body', '')

            if not repo or not title:
                return "❌ Missing required parameters: repo, title"

            data = {'title': title, 'body': body}
            response = requests.post(f'https://api.github.com/repos/{repo}/issues', headers=headers, json=data)

            if response.status_code == 201:
                issue = response.json()
                return f"✅ Issue created: #{issue['number']} - {issue['title']}"
            else:
                return f"❌ Failed to create issue: {response.status_code}"

        return f"⚠️ Unknown GitHub action: {action}"

    def _execute_slack_action(self, action: str, service: Dict, **params) -> str:
        """Execute Slack-specific actions"""
        token = service.get('token')
        headers = {'Authorization': f'Bearer {token}'}

        if action == "list_channels":
            response = requests.get('https://slack.com/api/conversations.list', headers=headers, params={'limit': 20})
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    output = "📺 Slack Channels:\n\n"
                    for channel in data.get('channels', [])[:10]:
                        output += f"#{channel['name']}\n"
                        output += f"   👥 {channel.get('num_members', 0)} members\n\n"
                    return output
                else:
                    return f"❌ Slack API error: {data.get('error')}"
            else:
                return f"❌ Failed to fetch channels: {response.status_code}"

        elif action == "send_message":
            channel = params.get('channel')
            text = params.get('text')

            if not channel or not text:
                return "❌ Missing required parameters: channel, text"

            data = {'channel': channel, 'text': text}
            response = requests.post('https://slack.com/api/chat.postMessage', headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                if result.get('ok'):
                    return "✅ Message sent successfully"
                else:
                    return f"❌ Failed to send message: {result.get('error')}"
            else:
                return f"❌ Failed to send message: {response.status_code}"

        return f"⚠️ Unknown Slack action: {action}"

    def _execute_discord_action(self, action: str, service: Dict, **params) -> str:
        """Execute Discord-specific actions"""
        token = service.get('token')
        headers = {'Authorization': f'Bot {token}'}

        if action == "list_guilds":
            response = requests.get('https://discord.com/api/users/@me/guilds', headers=headers)
            if response.status_code == 200:
                guilds = response.json()
                output = "🏰 Discord Servers:\n\n"
                for guild in guilds[:10]:
                    output += f"🏠 {guild['name']}\n"
                    output += f"   👑 Owner: {guild.get('owner', 'Unknown')}\n\n"
                return output
            else:
                return f"❌ Failed to fetch guilds: {response.status_code}"

        return f"⚠️ Unknown Discord action: {action}"

    def setup_webhook(self, service_name: str, webhook_url: str, events: List[str]) -> str:
        """Setup webhook for a service"""
        """Register a webhook for a given service with validation."""
        if service_name not in self.services:
            return f"❌ Service '{service_name}' not configured"

        # Basic validations: url must be a string and events must be a list
        if not isinstance(webhook_url, str) or not isinstance(events, list):
            raise ValueError("Invalid webhook url or events list")

        # Prevent local network addresses or file:/// curls (simple guard)
        if re.match(r"^(?:http|https)://(?:127\.|localhost|10\.|192\.168\.)", webhook_url, re.IGNORECASE):
            raise ValueError("Refusing to register webhooks to local or private IP addresses")

        # Limit number of events and sanitize event names
        if len(events) > 10:
            raise ValueError("Too many events requested for webhook")

        clean_events = []
        for e in events:
            if not isinstance(e, str):
                continue
            e_clean = re.sub(r"[^a-zA-Z0-9_\-]", "", e).lower()
            if e_clean:
                clean_events.append(e_clean)

        webhook_config = {
            'service': service_name,
            'url': webhook_url,
            'events': clean_events,
            'created_at': datetime.now().isoformat(),
            'active': True
        }

        webhook_id = f"{service_name}_{hashlib.md5(webhook_url.encode()).hexdigest()[:8]}"

        # simple threat detection on url and events (use AdvancedSecurity if available)
        try:
            from .advanced_security import AdvancedSecurity
            adv = AdvancedSecurity()
            threats = adv.detect_threats(webhook_url + ' ' + ' '.join(clean_events))
            if threats and any(t.get('severity', 0) >= 5 for t in threats):
                return f"❌ Webhook appears to contain suspicious content and was rejected"
        except Exception:
            # If advanced security isn't available or raises, proceed conservatively
            pass

        self.webhooks[webhook_id] = webhook_config
        self.save_integrations()

        return f"✅ Webhook '{webhook_id}' created for {service_name}"

    def list_webhooks(self) -> str:
        """List all configured webhooks"""
        if not self.webhooks:
            return "🔗 No webhooks configured"

        output = "🪝 Configured Webhooks:\n\n"
        for webhook_id, config in self.webhooks.items():
            status = "🟢 Active" if config.get('active', False) else "🔴 Inactive"
            output += f"🪝 {webhook_id}\n"
            output += f"   🔗 Service: {config['service']}\n"
            output += f"   🌐 URL: {config['url']}\n"
            output += f"   📅 Created: {config.get('created_at', 'Unknown')[:10]}\n"
            output += f"   {status}\n\n"

        return output

    def get_integration_stats(self) -> Dict:
        """Get integration statistics"""
        stats = {
            'total_services': len(self.services),
            'supported_services': len(self.supported_services),
            'connected_services': sum(1 for status in self.connection_status.values() if status == 'connected'),
            'failed_connections': sum(1 for status in self.connection_status.values() if status == 'failed'),
            'total_webhooks': len(self.webhooks),
            'active_webhooks': sum(1 for w in self.webhooks.values() if w.get('active', False))
        }

        return stats

    def export_configuration(self, format_type: str = "json") -> str:
        """Export integration configuration"""
        config = {
            'services': self.services,
            'webhooks': self.webhooks,
            'connection_status': self.connection_status,
            'exported_at': datetime.now().isoformat()
        }

        if format_type == "json":
            return json.dumps(config, indent=2)
        else:
            return f"❌ Unsupported export format: {format_type}. Use 'json'"
