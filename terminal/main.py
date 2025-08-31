#!/usr/bin/env python3
import os
import google.generativeai as genai
from groq import Groq
import ollama
import subprocess
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import yaml
import re
import logging
from datetime import datetime
import sys
import time
import requests
from typing import Dict, Optional
import shlex
import hashlib
import json
import threading
import openai

# Additional imports for advanced features
try:
    import psutil
    import platform
    import tempfile
    import cProfile
    import pstats
    import io
    from pathlib import Path
except ImportError:
    # Optional dependencies - features will gracefully fail if not available
    pass

# Import advanced features module
try:
    from advanced_features import AdvancedFeatures
except ImportError:
    AdvancedFeatures = None

# Import new advanced modules
try:
    from context_aware_ai import ContextAwareAI
    from analytics_monitor import AnalyticsMonitor
    from games_learning import GamesLearning
    from creative_tools import CreativeTools
    from advanced_security import AdvancedSecurity
    from task_manager import TaskManager
    from theme_manager import ThemeManager
    from code_review_assistant import CodeReviewAssistant
    from integration_hub import IntegrationHub
except ImportError:
    ContextAwareAI = None
    AnalyticsMonitor = None
    GamesLearning = None
    CreativeTools = None
    AdvancedSecurity = None
    TaskManager = None
    ThemeManager = None
    CodeReviewAssistant = None
    IntegrationHub = None

# --- Configuration ---
load_dotenv()

# Initialize console with default theme
console = Console()

# Global theme manager reference (will be set when NexusAI initializes)
global_theme_manager = None

def update_console_theme(theme_manager=None):
    """Update the global console theme"""
    global console, global_theme_manager
    if theme_manager:
        global_theme_manager = theme_manager
        rich_theme = theme_manager.get_rich_theme()
        console = Console(theme=rich_theme)
    else:
        console = Console()

logging.basicConfig(
    filename='ai_assistant.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Settings
CONFIG_PATH = os.path.expanduser("~/.nexus/config.yaml")
USER_DB_PATH = os.path.expanduser("~/.nexus/users.json")
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1.5
VERSION = "3.0"
REQUEST_TIMEOUT = 30

# Security settings
ALLOWED_DOMAINS = [
    "api.groq.com",
    "generativelanguage.googleapis.com",
    "api-inference.huggingface.co"
]

# --- Custom Exceptions ---
class SecurityError(Exception):
    pass

class APIError(Exception):
    pass

# --- Security Manager ---
class SecurityManager:
    def __init__(self):
        self.blocklist = [
            r"sudo\s", r"rm\s+-[rf]", r"chmod\s+777",
            r"wget\s", r"curl\s", r"\|\s*sh",
            r">\s*/dev", r"nohup", r"fork\(\)",
            r"eval\(", r"base64_decode", r"UNION\s+SELECT",
            r"DROP\s+TABLE", r"<script", r"javascript:"
        ]
        # Allowlist for commands and file extensions
        self.allowed_commands = [
            'ls', 'pwd', 'whoami', 'date', 'uptime', 'echo', 'cat', 'head', 'tail', 'df', 'du', 'free', 'uname', 'id'
        ]
        self.allowed_file_extensions = ['.txt', '.log', '.md', '.csv']
        self.violation_count = 0
        self.violation_threshold = 5

    def sanitize(self, input_str: str) -> str:
        if not isinstance(input_str, str) or len(input_str) > 10000:
            self.log_violation('Input too long or not a string')
            raise SecurityError("Invalid input")
        if not self.is_printable(input_str):
            self.log_violation('Non-printable characters detected')
            raise SecurityError("Input contains non-printable characters")
        if self.has_suspicious_unicode(input_str):
            self.log_violation('Suspicious unicode detected')
            raise SecurityError("Input contains suspicious unicode characters")
        sanitized = input_str.strip().replace("\0", "")
        for pattern in self.blocklist:
            if re.search(pattern, sanitized, re.IGNORECASE):
                self.log_violation(f'Blocked pattern: {pattern}')
                raise SecurityError("Blocked dangerous pattern")
        return sanitized

    def validate_api_key(self, key: str, provider: str = "generic") -> bool:
        if not key or not isinstance(key, str):
            return False
        rules = {
            "gemini": {"min_length": 30, "prefixes": ["AI"]},
            "groq": {"min_length": 40, "prefixes": ["gsk_"]},
            "huggingface": {"min_length": 30, "prefixes": ["hf_"]},
            "generic": {"min_length": 20, "prefixes": []}
        }
        rule = rules.get(provider.lower(), rules["generic"])
        if len(key) < rule["min_length"]:
            return False
        if rule["prefixes"] and not any(key.startswith(p) for p in rule["prefixes"]):
            return False
        return re.match(r'^[a-zA-Z0-9_-]+$', key) is not None

    def is_command_allowed(self, cmd: str) -> bool:
        return cmd in self.allowed_commands

    def is_file_extension_allowed(self, filename: str) -> bool:
        return any(filename.endswith(ext) for ext in self.allowed_file_extensions)

    def is_printable(self, s: str) -> bool:
        return all(32 <= ord(c) <= 126 or c in '\n\r\t' for c in s)

    def has_suspicious_unicode(self, s: str) -> bool:
        # Block invisible, right-to-left, or control unicode chars
        suspicious = [
            '\u202e', '\u202d', '\u202a', '\u202b', '\u202c', '\u200b', '\ufeff', '\u2066', '\u2067', '\u2068', '\u2069'
        ]
        return any(code in s for code in suspicious)

    def log_violation(self, reason: str):
        self.violation_count += 1
        logging.warning(f"Security violation: {reason}")
        if self.violation_count >= self.violation_threshold:
            logging.critical("Repeated security violations detected!")
            # Optionally, trigger alert/lockout here

    def validate_url(self, url: str) -> bool:
        # Only allow http(s) and block local addresses
        if not url.startswith(('http://', 'https://')):
            return False
        if re.search(r'(localhost|127\\.0\\.1|0\\.0\\.0\\.0|::1)', url):
            return False
        return True

# --- AI Manager ---
class AIManager:
    def __init__(self):
        self.security = SecurityManager()
        self.gemini = None
        self.groq = None
        self.session = self._create_session()
        self.status = {
            "gemini": "Not configured",
            "groq": "Not configured",
            "ollama": "Ready" if self._check_ollama() else "Not installed",
            "huggingface": "Ready (requires token)",
            "chatgpt": "Not configured",
            "mcp": "Not configured"
        }
        self._init_services()
        
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        session.verify = True
        session.timeout = REQUEST_TIMEOUT
        session.headers.update({
            'User-Agent': f'NexusAI/{VERSION}',
            'Accept': 'application/json'
        })
        return session
        
    def _init_services(self):
        # Gemini 2.0 Flash (Fixed API)
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if gemini_key and self.security.validate_api_key(gemini_key, "gemini"):
            try:
                genai.configure(api_key=gemini_key)
                self.gemini = genai.GenerativeModel("gemini-2.0-flash-exp")
                self.status["gemini"] = "✅ Ready"
                logging.info("Gemini 2.0 Flash initialized successfully")
            except Exception as e:
                self.status["gemini"] = f"❌ Error: {str(e)[:50]}..."
                logging.error(f"Gemini init failed: {str(e)}")
        elif gemini_key:
            self.status["gemini"] = "❌ Invalid API key format"
        
        # Groq Cloud
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key and self.security.validate_api_key(groq_key, "groq"):
            try:
                self.groq = Groq(api_key=groq_key)
                self.status["groq"] = "✅ Ready"
                logging.info("Groq service initialized")
            except Exception as e:
                self.status["groq"] = f"❌ Error: {str(e)[:50]}..."
                logging.error(f"Groq init failed: {str(e)}")
        elif groq_key:
            self.status["groq"] = "❌ Invalid API key format"
        
        # Ollama local
        if self.status["ollama"] == "Ready":
            models = self._get_ollama_models()
            self.status["ollama"] = f"✅ Ready ({models})" if models != "Unknown" else "❌ No models"
        else:
            self.status["ollama"] = "❌ Not installed"
        
        # ChatGPT (OpenAI)
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and self.security.validate_api_key(openai_key, "generic"):
            try:
                openai.api_key = openai_key
                self.status["chatgpt"] = "✅ Ready"
                logging.info("ChatGPT (OpenAI) initialized successfully")
            except Exception as e:
                self.status["chatgpt"] = f"❌ Error: {str(e)[:50]}..."
                logging.error(f"ChatGPT init failed: {str(e)}")
        elif openai_key:
            self.status["chatgpt"] = "❌ Invalid API key format"
        
        # MCP (Model Context Protocol)
        mcp_key = os.getenv("MCP_API_KEY")
        if mcp_key and self.security.validate_api_key(mcp_key, "generic"):
            self.status["mcp"] = "✅ Ready"
        elif mcp_key:
            self.status["mcp"] = "❌ Invalid API key format"
    
    def _check_ollama(self) -> bool:
        try:
            ollama.list()
            return True
        except:
            return False
    
    def _get_ollama_models(self) -> str:
        try:
            models = [m["name"] for m in ollama.list()["models"]]
            return ", ".join(models[:3]) + ("..." if len(models) > 3 else "")
        except:
            return "Unknown"
    
    def _query_huggingface(self, prompt: str) -> str:
        try:
            hf_token = os.getenv("HUGGINGFACE_TOKEN")
            if not hf_token or not self.security.validate_api_key(hf_token, "huggingface"):
                return "❌ HuggingFace token not configured or invalid"
            
            response = self.session.post(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                headers={"Authorization": f"Bearer {hf_token}"},
                json={"inputs": prompt[:1000]}
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and result:
                    return result[0].get("generated_text", "No response")[:2000]
            
            return f"❌ HuggingFace API Error: {response.status_code}"
        except Exception as e:
            return f"❌ HuggingFace unavailable: {str(e)[:50]}..."
    
    def query(self, model: str, prompt: str) -> str:
        if not prompt or len(prompt.strip()) == 0:
            return "❌ Empty prompt provided"
        
        try:
            clean_prompt = self.security.sanitize(prompt)
        except SecurityError as e:
            return f"🔒 Security error: {str(e)}"
        
        for attempt in range(MAX_RETRIES):
            try:
                if model == "gemini" and self.gemini:
                    response = self.gemini.generate_content(
                        clean_prompt,
                        generation_config=genai.types.GenerationConfig(
                            temperature=0.7,
                            max_output_tokens=1000
                        )
                    )
                    
                    if not response or not hasattr(response, 'text') or not response.text:
                        raise APIError("Invalid Gemini response")
                    
                    return response.text[:2000]
                
                elif model == "groq" and self.groq:
                    response = self.groq.chat.completions.create(
                        messages=[{"role": "user", "content": clean_prompt}],
                        model="mixtral-8x7b-32768",
                        max_tokens=1000
                    )
                    
                    if not response or not response.choices or not response.choices[0].message.content:
                        raise APIError("Invalid Groq response")
                    
                    return response.choices[0].message.content[:2000]
                
                elif model == "ollama" or model.startswith("ollama:"):
                    if not self._check_ollama():
                        return "❌ Ollama not available"
                    
                    # Extract specific model name if provided
                    if ":" in model:
                        ollama_model = model.split(":", 1)[1]
                    else:
                        ollama_model = "llama3"  # Default fallback
                    
                    try:
                        response = ollama.chat(
                            model=ollama_model,
                            messages=[{"role": "user", "content": clean_prompt}]
                        )
                        
                        if not isinstance(response, dict) or "message" not in response:
                            raise APIError("Invalid Ollama response")
                        
                        content = response["message"].get("content", "")
                        if not content:
                            raise APIError("Empty Ollama response")
                        
                        return content[:2000]
                    except Exception as e:
                        if "model not found" in str(e).lower():
                            return f"❌ Ollama model '{ollama_model}' not found.\n   Use /ollama-models to see available models"
                        else:
                            raise
                
                elif model == "huggingface":
                    return self._query_huggingface(clean_prompt)
                
                elif model == "chatgpt":
                    openai_key = os.getenv("OPENAI_API_KEY")
                    if not openai_key or not self.security.validate_api_key(openai_key, "generic"):
                        return "❌ OpenAI API key not configured or invalid"
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": clean_prompt}],
                        max_tokens=1000
                    )
                    if not response or not response.choices or not response.choices[0].message.content:
                        raise APIError("Invalid ChatGPT response")
                    return response.choices[0].message.content[:2000]
                
                elif model == "mcp":
                    mcp_key = os.getenv("MCP_API_KEY")
                    mcp_url = os.getenv("MCP_URL", "http://localhost:8080/api/v1/completions")
                    if not mcp_key:
                        return "❌ MCP API key not configured"
                    headers = {"Authorization": f"Bearer {mcp_key}", "Content-Type": "application/json"}
                    data = {"prompt": clean_prompt, "max_tokens": 1000}
                    try:
                        resp = self.session.post(mcp_url, headers=headers, json=data, timeout=REQUEST_TIMEOUT)
                        if resp.status_code == 200:
                            result = resp.json()
                            return result.get("text", "No response")[:2000]
                        return f"❌ MCP API Error: {resp.status_code}"
                    except Exception as e:
                        return f"❌ MCP unavailable: {str(e)[:50]}..."
                
                else:
                    return f"❌ Model '{model}' not available"
                
            except APIError as e:
                if attempt == MAX_RETRIES - 1:
                    return f"❌ {model} API error: {str(e)}"
                time.sleep(RATE_LIMIT_DELAY * (attempt + 1))
                
            except Exception as e:
                logging.warning(f"Attempt {attempt+1} failed for {model}: {str(e)}")
                if attempt == MAX_RETRIES - 1:
                    return f"❌ {model} error: {str(e)[:50]}..."
                time.sleep(RATE_LIMIT_DELAY * (attempt + 1))
        
        return f"❌ {model} unavailable after {MAX_RETRIES} attempts"

# --- User Management ---
class UserManager:
    def __init__(self):
        self.user_db = self._load_users()
        self.current_user = None
        self.chat_history = {}
        self.admins = set(["admin"])  # Default admin user
        self.last_active = {}
        self.activity_log = {}
        self.audit_log = []
        self.session_timeout = 900  # 15 minutes
        self._start_timeout_thread()

    def _load_users(self):
        if os.path.exists(USER_DB_PATH):
            with open(USER_DB_PATH, 'r') as f:
                return json.load(f)
        return {}

    def _save_users(self):
        os.makedirs(os.path.dirname(USER_DB_PATH), exist_ok=True)
        with open(USER_DB_PATH, 'w') as f:
            json.dump(self.user_db, f)
        os.chmod(USER_DB_PATH, 0o600)

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def signup(self, username, password, is_admin=False):
        if username in self.user_db:
            return False, "User already exists."
        self.user_db[username] = {
            "password": self.hash_password(password),
            "api_keys": {},
            "model": "gemini",
            "role": "admin" if is_admin else "user"
        }
        self._save_users()
        return True, "Signup successful."

    def login(self, username, password):
        user = self.user_db.get(username)
        if not user or user["password"] != self.hash_password(password):
            return False, "Invalid username or password."
        self.current_user = username
        return True, f"Welcome, {username}!"

    def set_api_key(self, provider, key):
        if not self.current_user:
            return False, "Not logged in."
        self.user_db[self.current_user]["api_keys"][provider] = key
        self._save_users()
        return True, f"API key for {provider} set."

    def get_api_key(self, provider):
        if not self.current_user:
            return None
        return self.user_db[self.current_user]["api_keys"].get(provider)

    def set_model(self, model):
        if not self.current_user:
            return False, "Not logged in."
        self.user_db[self.current_user]["model"] = model
        self._save_users()
        return True, f"Model set to {model}."

    def get_model(self):
        if not self.current_user:
            return "gemini"
        return self.user_db[self.current_user].get("model", "gemini")

    def is_admin(self, username=None):
        user = username or self.current_user
        if not user:
            return False
        return self.user_db.get(user, {}).get("role") == "admin"

    def reset_password(self, username, newpassword):
        if username not in self.user_db:
            return False, "User not found."
        self.user_db[username]["password"] = self.hash_password(newpassword)
        self._save_users()
        return True, "Password reset."

    def list_users(self):
        return list(self.user_db.keys())

    def add_history(self, username, message):
        if username not in self.chat_history:
            self.chat_history[username] = []
        self.chat_history[username].append(message)
        if len(self.chat_history[username]) > 50:
            self.chat_history[username] = self.chat_history[username][-50:]

    def get_history(self, username):
        return self.chat_history.get(username, [])

    def clear_history(self, username):
        self.chat_history[username] = []

    def _start_timeout_thread(self):
        def timeout_checker():
            while True:
                now = time.time()
                for user, last in list(self.last_active.items()):
                    if self.current_user == user and now - last > self.session_timeout:
                        self.current_user = None
                time.sleep(60)
        t = threading.Thread(target=timeout_checker, daemon=True)
        t.start()

    def update_activity(self, username, action):
        self.last_active[username] = time.time()
        if username not in self.activity_log:
            self.activity_log[username] = []
        self.activity_log[username].append((time.strftime('%Y-%m-%d %H:%M:%S'), action))
        if len(self.activity_log[username]) > 100:
            self.activity_log[username] = self.activity_log[username][-100:]
        self.audit_log.append((username, time.strftime('%Y-%m-%d %H:%M:%S'), action))
        if len(self.audit_log) > 500:
            self.audit_log = self.audit_log[-500:]

# --- Core Application ---
class NexusAI:
    def __init__(self):
        self.user_manager = UserManager()
        self.ai = AIManager()
        self.security = SecurityManager()
        self.current_model = self._load_config()
        self.allowed_commands = [
            'ls', 'pwd', 'whoami', 'date', 'uptime', 'echo', 'cat', 'head', 'tail', 'df', 'du', 'free', 'uname', 'id', 'git'
        ]
        
        # Initialize advanced modules
        self.context_ai = ContextAwareAI() if ContextAwareAI else None
        self.analytics = AnalyticsMonitor() if AnalyticsMonitor else None
        self.games = GamesLearning() if GamesLearning else None
        self.creative = CreativeTools() if CreativeTools else None
        self.adv_security = AdvancedSecurity() if AdvancedSecurity else None
        self.task_manager = TaskManager() if TaskManager else None
        self.theme_manager = ThemeManager() if ThemeManager else None
        self.code_reviewer = CodeReviewAssistant() if CodeReviewAssistant else None
        self.integration_hub = IntegrationHub() if IntegrationHub else None
        
        # Update console theme if theme manager is available
        if self.theme_manager:
            update_console_theme(self.theme_manager)
        
        self.show_banner()
    
    def _load_config(self) -> str:
        try:
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH) as f:
                    config = yaml.safe_load(f)
                    if isinstance(config, dict):
                        model = config.get("default_model", "gemini")
                        if model in ["gemini", "groq", "ollama", "huggingface"]:
                            return model
        except:
            pass
        return "gemini"
    
    def _save_config(self):
        try:
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, "w") as f:
                yaml.dump({"default_model": self.current_model}, f)
            # Restrict config file permissions (owner read/write only)
            os.chmod(CONFIG_PATH, 0o600)
        except Exception as e:
            logging.error(f"Config save error: {str(e)}")
    
    def show_banner(self):
        # Cool ASCII Banner
        banner_text = Text()
        banner_text.append("\n")
        banner_text.append("███   ██╗███████╗██╗  ██╗██╗   ██╗███████╗\n", style="bold cyan")
        banner_text.append("████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝\n", style="bold cyan")
        banner_text.append("██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗\n", style="bold blue")
        banner_text.append("██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║\n", style="bold blue")
        banner_text.append("██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║\n", style="bold magenta")
        banner_text.append("╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝\n", style="bold magenta")
        banner_text.append(f"\n🤖 AI TERMINAL ASSISTANT v{VERSION}\n", style="bold green")
        banner_text.append("⚡ Multi-Model • 🔒 Secure • 🚀 Enhanced\n", style="bold yellow")
        
        console.print(Panel(banner_text, border_style="bright_blue", padding=(1, 2)))
        
        # Status Table
        table = Table(title="🔧 AI Services Status", show_header=True, header_style="bold magenta")
        table.add_column("Service", style="cyan", width=15)
        table.add_column("Status", style="green", width=30)
        table.add_column("Description", style="white", width=40)
        
        descriptions = {
            "gemini": "Google's Gemini 2.0 Flash (Fixed API)",
            "groq": "Groq Cloud - Mixtral 8x7B",
            "ollama": "Local Ollama Models (Most Secure)",
            "huggingface": "HuggingFace Inference API",
            "chatgpt": "OpenAI's ChatGPT (API)",
            "mcp": "Model Context Protocol (API)"
        }
        
        for service, status in self.ai.status.items():
            table.add_row(service.upper(), status, descriptions.get(service, "AI Service"))
        
        console.print(table)
        console.print(f"\n🎯 Current Model: [bold yellow]{self.current_model.upper()}[/bold yellow]")
        console.print("\n💡 Type [bold cyan]/help[/bold cyan] for commands or start chatting!\n")
    
    def execute_command(self, cmd: str) -> str:
        try:
            clean_cmd = self.security.sanitize(cmd)
            if len(clean_cmd) > 500:
                return "❌ Command too long (max 500 characters)"
            # Only allow commands in the allowlist
            parts = shlex.split(clean_cmd)
            if not parts or parts[0] not in self.allowed_commands:
                return f"❌ Command '{parts[0] if parts else ''}' not allowed. Allowed: {', '.join(self.allowed_commands)}"
            # Block wildcards, path traversal, shell metacharacters in arguments
            forbidden_patterns = [r"[><|;&]", r"\*", r"\.\.", r"/etc", r"/var", r"/root", r"\\"]
            for arg in parts[1:]:
                for pat in forbidden_patterns:
                    if re.search(pat, arg):
                        return "❌ Command arguments contain forbidden patterns."
            # Restrict file arguments for file commands to current directory only
            file_cmds = {"cat", "head", "tail"}
            if parts[0] in file_cmds and len(parts) > 1:
                for arg in parts[1:]:
                    if not os.path.abspath(arg).startswith(os.getcwd()):
                        return "❌ Only files in the current directory are allowed."
            # Log only the command name for audit (not arguments)
            logging.info(f"Command executed: {parts[0]}")
            result = subprocess.run(
                parts, capture_output=True,
                text=True, timeout=15
            )
            output = (result.stdout or "")[:1000]
            error = (result.stderr or "")[:1000]
            return output if output else error or "Command executed"
        except subprocess.TimeoutExpired:
            return "❌ Command timed out (15s limit)"
        except Exception as e:
            return f"❌ Error: {str(e)[:100]}..."
    
    def execute_git_command(self, git_cmd: str) -> str:
        """Execute Git commands with enhanced formatting and error handling"""
        try:
            # Check if we're in a Git repository
            if not os.path.exists('.git') and not os.path.exists('../.git'):
                return "❌ Not a Git repository. Initialize with 'git init' or navigate to a Git repository."
            
            clean_cmd = self.security.sanitize(git_cmd)
            if len(clean_cmd) > 500:
                return "❌ Git command too long (max 500 characters)"
            
            # Parse the command
            parts = shlex.split(clean_cmd)
            if not parts or parts[0] != 'git':
                return "❌ Invalid Git command format"
            
            # Execute the Git command
            result = subprocess.run(
                parts, capture_output=True,
                text=True, timeout=30,  # Git commands can take longer
                cwd=os.getcwd()
            )
            
            # Format the output based on command type
            if result.returncode == 0:
                output = result.stdout.strip()
                if not output:
                    return "✅ Git command executed successfully"
                
                # Format specific commands
                if 'status' in git_cmd:
                    return self._format_git_status(output)
                elif 'log' in git_cmd:
                    return self._format_git_log(output)
                elif 'diff' in git_cmd:
                    return self._format_git_diff(output)
                elif 'branch' in git_cmd and '--list' not in git_cmd:
                    return self._format_git_branch(output)
                else:
                    return output[:2000]  # Limit output size
            else:
                error = result.stderr.strip()
                return f"❌ Git error: {error[:500]}"
                
        except subprocess.TimeoutExpired:
            return "❌ Git command timed out (30s limit)"
        except Exception as e:
            return f"❌ Git command failed: {str(e)[:100]}"
    
    def _format_git_status(self, output: str) -> str:
        """Format git status output with colors and structure"""
        if not output:
            return "📁 Repository is clean - no changes to commit"
        
        lines = output.split('\n')
        formatted = "📊 Git Status:\n\n"
        
        staged = []
        unstaged = []
        untracked = []
        
        for line in lines:
            if line.startswith('M '):
                staged.append(f"📝 Modified: {line[3:]}")
            elif line.startswith('A '):
                staged.append(f"➕ Added: {line[3:]}")
            elif line.startswith('D '):
                staged.append(f"🗑️  Deleted: {line[3:]}")
            elif line.startswith('R '):
                staged.append(f"📋 Renamed: {line[3:]}")
            elif line.startswith('C '):
                staged.append(f"📄 Copied: {line[3:]}")
            elif line.startswith('?? '):
                untracked.append(f"❓ Untracked: {line[3:]}")
            elif line.startswith(' M'):
                unstaged.append(f"📝 Modified: {line[3:]}")
            elif line.startswith(' D'):
                unstaged.append(f"🗑️  Deleted: {line[3:]}")
        
        if staged:
            formatted += "✅ Staged Changes:\n" + "\n".join(staged) + "\n\n"
        if unstaged:
            formatted += "📝 Unstaged Changes:\n" + "\n".join(unstaged) + "\n\n"
        if untracked:
            formatted += "❓ Untracked Files:\n" + "\n".join(untracked) + "\n\n"
        
        return formatted
    
    def _format_git_log(self, output: str) -> str:
        """Format git log output with better readability"""
        if not output:
            return "📜 No commits found"
        
        lines = output.split('\n')
        formatted = "📜 Commit History:\n\n"
        
        for i, line in enumerate(lines[:20]):  # Limit to 20 commits
            if line.strip():
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    commit_hash = parts[0][:8]
                    message = parts[1]
                    formatted += f"🔗 {commit_hash}: {message}\n"
        
        if len(lines) > 20:
            formatted += f"\n... and {len(lines) - 20} more commits"
        
        return formatted
    
    def _format_git_diff(self, output: str) -> str:
        """Format git diff output with syntax highlighting"""
        if not output:
            return "📄 No differences found"
        
        # For now, just return the raw diff with a header
        # In a more advanced implementation, this could include syntax highlighting
        return f"📄 Changes:\n\n{output[:3000]}"  # Limit size
    
    def _format_git_branch(self, output: str) -> str:
        """Format git branch output"""
        if not output:
            return "🌿 No branches found"
        
        lines = output.split('\n')
        formatted = "🌿 Branches:\n\n"
        
        for line in lines:
            if line.strip():
                if line.startswith('*'):
                    formatted += f"🔥 Current: {line[2:]}\n"
                else:
                    formatted += f"🌿 Branch: {line.strip()}\n"
        
        return formatted
    
    def process_input(self, user_input: str) -> str:
        try:
            clean_input = self.security.sanitize(user_input)
            if self.user_manager.current_user:
                self.user_manager.update_activity(self.user_manager.current_user, clean_input)
            
            # Track usage analytics
            if self.analytics:
                feature = "ai_chat" if not clean_input.startswith("/") else clean_input.split()[0][1:]
                self.analytics.track_usage(feature, self.user_manager.current_user or "anonymous")
            
            if clean_input.startswith("/"):
                return self.handle_command(clean_input)
            # AI features for logged-in users
            if self.user_manager.current_user:
                self.user_manager.add_history(self.user_manager.current_user, clean_input)
                if clean_input.startswith("summarize "):
                    return self.ai.query(self.current_model, f"Summarize: {clean_input[10:]}")
                if clean_input.startswith("translate "):
                    return self.ai.query(self.current_model, f"Translate: {clean_input[10:]}")
                if clean_input.startswith("explain "):
                    return self.ai.query(self.current_model, f"Explain: {clean_input[8:]}")
            return self.ai.query(self.current_model, clean_input)
        except SecurityError:
            # Track security errors
            if self.analytics:
                self.analytics.track_error("security_violation", "Input security violation")
            return "🔒 Security block: Input contains dangerous content"
        except Exception as e:
            # Track general errors
            if self.analytics:
                self.analytics.track_error("processing_error", str(e))
            logging.error(f"Processing error: {str(e)}")
            return "❌ System error - see logs for details"
    
    def handle_command(self, command: str) -> str:
        try:
            cmd = command[1:].strip().lower()
            # --- Session Timeout ---
            if cmd == "myactivity":
                if not self.user_manager.current_user:
                    return "Not logged in."
                log = self.user_manager.activity_log.get(self.user_manager.current_user, [])
                return "\n".join([f"{t}: {a}" for t, a in log]) or "No activity."
            if cmd == "auditlog":
                if not self.user_manager.is_admin():
                    return "Admin only."
                return "\n".join([f"{u} {t}: {a}" for u, t, a in self.user_manager.audit_log]) or "No audit log."
            # --- Advanced User Management ---
            if cmd.startswith("resetpw"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /resetpw [username] [newpassword]"
                if not self.user_manager.is_admin():
                    return "Admin only."
                ok, msg = self.user_manager.reset_password(parts[1], parts[2])
                return msg
            if cmd == "listusers":
                if not self.user_manager.is_admin():
                    return "Admin only."
                return "Users: " + ", ".join(self.user_manager.list_users())
            # --- Chat History ---
            if cmd == "history":
                if not self.user_manager.current_user:
                    return "Not logged in."
                hist = self.user_manager.get_history(self.user_manager.current_user)
                return "\n".join(hist) if hist else "No history."
            if cmd == "clearhistory":
                if not self.user_manager.current_user:
                    return "Not logged in."
                self.user_manager.clear_history(self.user_manager.current_user)
                return "History cleared."
            # --- Git Advanced ---
            if cmd.startswith("git create-branch"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /git create-branch [name]"
                return self.execute_git_command(f"git branch {parts[2]}")
            if cmd.startswith("git delete-branch"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /git delete-branch [name]"
                return self.execute_git_command(f"git branch -d {parts[2]}")
            
            # --- Advanced Git Commands ---
            if cmd == "git status":
                return self.execute_git_command("git status --porcelain")
            
            if cmd.startswith("git add"):
                parts = command.split(maxsplit=2)
                if len(parts) == 1:
                    return "Usage: /git add [files] or /git add . for all files"
                files = parts[1] if len(parts) > 1 else "."
                return self.execute_git_command(f"git add {files}")
            
            if cmd.startswith("git commit"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git commit [message] - Commit staged changes"
                message = parts[2]
                return self.execute_git_command(f"git commit -m \"{message}\"")
            
            if cmd == "git push":
                return self.execute_git_command("git push origin HEAD")
            
            if cmd == "git pull":
                return self.execute_git_command("git pull --rebase")
            
            if cmd.startswith("git log"):
                parts = command.split()
                limit = parts[1] if len(parts) > 1 and parts[1].isdigit() else "10"
                return self.execute_git_command(f"git log --oneline -{limit}")
            
            if cmd == "git diff":
                return self.execute_git_command("git diff")
            
            if cmd == "git diff --staged":
                return self.execute_git_command("git diff --staged")
            
            if cmd == "git branch":
                return self.execute_git_command("git branch -a")
            
            if cmd.startswith("git checkout"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git checkout [branch]"
                branch = parts[2]
                return self.execute_git_command(f"git checkout {branch}")
            
            if cmd.startswith("git merge"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git merge [branch]"
                branch = parts[2]
                return self.execute_git_command(f"git merge {branch}")
            
            if cmd == "git stash":
                return self.execute_git_command("git stash")
            
            if cmd == "git stash pop":
                return self.execute_git_command("git stash pop")
            
            if cmd.startswith("git reset"):
                parts = command.split(maxsplit=3)
                if len(parts) == 3 and parts[2] == "--hard":
                    return self.execute_git_command("git reset --hard HEAD")
                elif len(parts) >= 3:
                    file_path = parts[2]
                    return self.execute_git_command(f"git reset HEAD {file_path}")
                else:
                    return "Usage: /git reset [file] or /git reset --hard"
            
            if cmd == "git remote -v":
                return self.execute_git_command("git remote -v")
            
            if cmd.startswith("git blame"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git blame [file]"
                file_path = parts[2]
                return self.execute_git_command(f"git blame {file_path}")
            
            if cmd.startswith("git cherry-pick"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git cherry-pick [commit-hash]"
                commit_hash = parts[2]
                return self.execute_git_command(f"git cherry-pick {commit_hash}")
            
            if cmd.startswith("git rebase"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git rebase [branch]"
                branch = parts[2]
                return self.execute_git_command(f"git rebase {branch}")
            
            if cmd == "git bisect start":
                return self.execute_git_command("git bisect start")
            
            if cmd.startswith("git tag"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git tag [tag-name]"
                tag_name = parts[2]
                return self.execute_git_command(f"git tag {tag_name}")
            
            if cmd == "git reflog":
                return self.execute_git_command("git reflog --oneline -10")
            
            # --- Git Workflow Commands ---
            if cmd.startswith("git new-branch"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git new-branch [name] - Create and switch to new branch"
                branch_name = parts[2]
                # Create branch and switch to it
                create_result = self.execute_git_command(f"git checkout -b {branch_name}")
                return create_result
            
            if cmd == "git undo-last-commit":
                return self.execute_git_command("git reset --soft HEAD~1")
            
            if cmd.startswith("git amend"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git amend [message] - Amend last commit with new message"
                message = parts[2]
                return self.execute_git_command(f"git commit --amend -m \"{message}\"")
            
            if cmd == "git uncommit":
                return self.execute_git_command("git reset --soft HEAD~1")
            
            if cmd == "git discard":
                return self.execute_git_command("git checkout -- .")
            
            if cmd.startswith("git ignore"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git ignore [pattern] - Add pattern to .gitignore"
                pattern = parts[2]
                try:
                    with open('.gitignore', 'a') as f:
                        f.write(f"\n{pattern}")
                    return f"✅ Added '{pattern}' to .gitignore"
                except Exception as e:
                    return f"❌ Failed to update .gitignore: {str(e)}"
            
            if cmd == "git repo-info":
                # Get comprehensive repository information
                info = []
                
                # Basic repo info
                try:
                    result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        info.append(f"🌐 Remote URL: {result.stdout.strip()}")
                except:
                    pass
                
                # Current branch
                try:
                    result = subprocess.run(['git', 'branch', '--show-current'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        info.append(f"🌿 Current Branch: {result.stdout.strip()}")
                except:
                    pass
                
                # Last commit
                try:
                    result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        info.append(f"📝 Last Commit: {result.stdout.strip()}")
                except:
                    pass
                
                # Status summary
                try:
                    result = subprocess.run(['git', 'status', '--porcelain'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        staged = len([l for l in lines if l and not l.startswith(' ')])
                        unstaged = len([l for l in lines if l and l.startswith(' ')])
                        untracked = len([l for l in lines if l and l.startswith('??')])
                        info.append(f"📊 Changes: {staged} staged, {unstaged} unstaged, {untracked} untracked")
                except:
                    pass
                
                if info:
                    return "📋 Repository Information:\n" + "\n".join(info)
                else:
                    return "❌ Could not retrieve repository information"
            
            # --- Additional Git Commands ---
            if cmd == "git init":
                return self.execute_git_command("git init")
            
            if cmd.startswith("git clone"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git clone [url] - Clone a repository"
                url = parts[2]
                return self.execute_git_command(f"git clone {url}")
            
            if cmd == "git fetch":
                return self.execute_git_command("git fetch --all")
            
            if cmd.startswith("git pull-request"):
                return "💡 To create a pull request, push your branch and use your Git hosting service (GitHub, GitLab, etc.)"
            
            if cmd == "git contributors":
                return self.execute_git_command("git shortlog -sn --no-merges")
            
            if cmd == "git file-history":
                return "Usage: /git file-history [filename] - Show history of a specific file"
            
            if cmd.startswith("git file-history"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /git file-history [filename] - Show history of a specific file"
                filename = parts[2]
                return self.execute_git_command(f"git log --follow --oneline {filename}")
            
            if cmd == "git clean":
                return self.execute_git_command("git clean -fd")
            
            if cmd == "git stats":
                # Get repository statistics
                stats = []
                try:
                    # Total commits
                    result = subprocess.run(['git', 'rev-list', '--count', 'HEAD'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        stats.append(f"📊 Total Commits: {result.stdout.strip()}")
                except:
                    pass
                
                try:
                    # Contributors count
                    result = subprocess.run(['git', 'shortlog', '-sn', '--no-merges'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        stats.append(f"👥 Contributors: {len(lines)}")
                except:
                    pass
                
                try:
                    # Repository size
                    result = subprocess.run(['git', 'count-objects', '-vH'], 
                                          capture_output=True, text=True, timeout=10)
                    if result.returncode == 0:
                        for line in result.stdout.split('\n'):
                            if 'size-pack:' in line:
                                stats.append(f"💾 Repository Size: {line.split(':')[1].strip()}")
                                break
                except:
                    pass
                
                if stats:
                    return "📈 Repository Statistics:\n" + "\n".join(stats)
                else:
                    return "❌ Could not retrieve repository statistics"
            
            # --- AI Code Review ---
            if cmd.startswith("codereview"):
                parts = command.split()
                if len(parts) != 2:
                    return "Usage: /codereview [filename]"
                try:
                    with open(parts[1], 'r') as f:
                        code = f.read(2000)
                    return self.ai.query(self.current_model, f"Review this code for bugs and improvements:\n{code}")
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            # --- AI File Summarization ---
            if cmd.startswith("summarizefile"):
                parts = command.split()
                if len(parts) != 2:
                    return "Usage: /summarizefile [filename]"
                try:
                    with open(parts[1], 'r') as f:
                        content = f.read(2000)
                    return self.ai.query(self.current_model, f"Summarize this file:\n{content}")
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            # --- AI File Search ---
            if cmd.startswith("aifind"):
                parts = command.split()
                if len(parts) != 2:
                    return "Usage: /aifind [keyword]"
                matches = []
                for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        try:
                            with open(os.path.join(root, file), 'r', errors='ignore') as f:
                                for i, line in enumerate(f):
                                    if parts[1] in line:
                                        matches.append(f"{file}:{i+1}: {line.strip()}")
                                        if len(matches) > 10:
                                            break
                        except Exception:
                            continue
                if not matches:
                    return "No matches found."
                context = "\n".join(matches[:10])
                return self.ai.query(self.current_model, f"Explain the context of these code lines:\n{context}")
            # --- AI Commit Message Generator ---
            if cmd.startswith("git commitmsg"):
                parts = command.split()
                if len(parts) == 3:
                    try:
                        with open(parts[2], 'r') as f:
                            diff = f.read(2000)
                        return self.ai.query(self.current_model, f"Write a git commit message for this diff or file:\n{diff}")
                    except Exception as e:
                        return f"Error reading file: {str(e)}"
                return "Usage: /git commitmsg [diff or file]"
            # --- AI Bug Finder ---
            if cmd.startswith("findbugs"):
                parts = command.split()
                if len(parts) != 2:
                    return "Usage: /findbugs [filename]"
                try:
                    with open(parts[1], 'r') as f:
                        code = f.read(2000)
                    return self.ai.query(self.current_model, f"Find bugs in this code:\n{code}")
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            # --- AI Refactor ---
            if cmd.startswith("refactor"):
                parts = command.split(maxsplit=2)
                if len(parts) != 3:
                    return "Usage: /refactor [filename] [instruction]"
                try:
                    with open(parts[1], 'r') as f:
                        code = f.read(2000)
                    return self.ai.query(self.current_model, f"Refactor this code as per instruction '{parts[2]}':\n{code}")
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            # --- Project TODO Extractor ---
            if cmd == "todos":
                todos = []
                for root, dirs, files in os.walk(os.getcwd()):
                    for file in files:
                        try:
                            with open(os.path.join(root, file), 'r', errors='ignore') as f:
                                for i, line in enumerate(f):
                                    if 'TODO' in line or 'FIXME' in line:
                                        todos.append(f"{file}:{i+1}: {line.strip()}")
                                        if len(todos) > 20:
                                            break
                        except Exception:
                            continue
                if not todos:
                    return "No TODOs/FIXMEs found."
                return self.ai.query(self.current_model, f"Summarize these TODOs/FIXMEs:\n" + "\n".join(todos[:20]))
            # --- AI Documentation Generator ---
            if cmd.startswith("gendoc"):
                parts = command.split()
                if len(parts) != 2:
                    return "Usage: /gendoc [filename]"
                try:
                    with open(parts[1], 'r') as f:
                        code = f.read(2000)
                    return self.ai.query(self.current_model, f"Generate docstrings and comments for this code:\n{code}")
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            # --- AI Test Generator ---
            if cmd.startswith("gentest"):
                parts = command.split()
                if len(parts) != 2:
                    return "Usage: /gentest [filename]"
                try:
                    with open(parts[1], 'r') as f:
                        code = f.read(2000)
                    return self.ai.query(self.current_model, f"Write unit tests for this code:\n{code}")
                except Exception as e:
                    return f"Error reading file: {str(e)}"
            # --- Existing Commands ---
            if cmd == "help":
                try:
                    help_text = Text()
                    help_text.append(f"\n🚀 NEXUS AI TERMINAL v{VERSION} - COMMAND REFERENCE\n\n", style="bold cyan")
                    help_text.append("📋 BASIC COMMANDS:\n", style="bold yellow")
                    help_text.append("/help          - Show this help menu\n", style="white")
                    help_text.append("/status        - Show detailed service status\n", style="white")
                    help_text.append("/security      - Show security information\n", style="white")
                    help_text.append("/clear         - Clear the screen\n", style="white")
                    help_text.append("/exit          - Quit application\n\n", style="white")
                    help_text.append("🤖 AI MODEL COMMANDS:\n", style="bold yellow")
                    help_text.append("/switch gemini      - Switch to Gemini 2.0 Flash\n", style="white")
                    help_text.append("/switch groq        - Switch to Groq Mixtral\n", style="white")
                    help_text.append("/switch ollama      - Switch to Ollama (default model)\n", style="white")
                    help_text.append("/switch ollama [model] - Switch to specific Ollama model\n", style="white")
                    help_text.append("/switch huggingface - Switch to HuggingFace\n", style="white")
                    help_text.append("/switch chatgpt     - Switch to ChatGPT (OpenAI)\n", style="white")
                    help_text.append("/switch mcp         - Switch to MCP (Model Context Protocol)\n\n", style="white")
                    help_text.append("⚙️ SYSTEM COMMANDS:\n", style="bold yellow")
                    help_text.append("/run [command]      - Execute safe system commands (ls, pwd, whoami, date, etc.)\n", style="white")
                    help_text.append("/models             - List available AI models\n", style="white")
                    help_text.append("/ollama-models      - Show detailed list of available Ollama models\n", style="white")
                    help_text.append("/current-model      - Show currently active AI model\n", style="white")
                    help_text.append("/config             - Show configuration\n", style="white")
                    help_text.append("/sysinfo            - Display system information and resources\n", style="white")
                    help_text.append("/calc [expression]  - Calculate mathematical expressions\n", style="white")
                    help_text.append("/explore            - Interactive file explorer for current directory\n", style="white")
                    help_text.append("/websearch [query]  - Search the web using DuckDuckGo\n", style="white")
                    help_text.append("/weather [city]     - Get current weather information\n", style="white")
                    help_text.append("/note [text]        - Save a quick note\n", style="white")
                    help_text.append("/notes              - View your saved notes\n", style="white")
                    help_text.append("/timer [seconds]    - Start a countdown timer\n", style="white")
                    help_text.append("/convert [val] [from] [to] - Unit converter (temp, weight, data)\n", style="white")
                    help_text.append("/joke               - Get a random joke\n", style="white")
                    help_text.append("/password [length]  - Generate a secure password\n", style="white")
                    help_text.append("/tip                - Get a random productivity tip\n", style="white")
                    help_text.append("/clear              - Clear the screen\n\n", style="white")
                    
                    help_text.append("🔀 GIT VERSION CONTROL:\n", style="bold yellow")
                    help_text.append("/git status            - Show repository status\n", style="white")
                    help_text.append("/git add [files]       - Stage files for commit\n", style="white")
                    help_text.append("/git commit [message]  - Commit staged changes\n", style="white")
                    help_text.append("/git push              - Push commits to remote\n", style="white")
                    help_text.append("/git pull              - Pull changes from remote\n", style="white")
                    help_text.append("/git log [n]           - Show commit history\n", style="white")
                    help_text.append("/git diff              - Show unstaged changes\n", style="white")
                    help_text.append("/git diff --staged     - Show staged changes\n", style="white")
                    help_text.append("/git branch            - List branches\n", style="white")
                    help_text.append("/git checkout [branch] - Switch to branch\n", style="white")
                    help_text.append("/git merge [branch]    - Merge branch into current\n", style="white")
                    help_text.append("/git stash             - Stash current changes\n", style="white")
                    help_text.append("/git stash pop         - Apply stashed changes\n", style="white")
                    help_text.append("/git reset [file]      - Unstage file\n", style="white")
                    help_text.append("/git reset --hard      - Reset to last commit\n", style="white")
                    help_text.append("/git remote -v         - Show remote repositories\n", style="white")
                    help_text.append("/git blame [file]      - Show who changed each line\n", style="white")
                    help_text.append("/git cherry-pick [hash] - Apply specific commit\n", style="white")
                    help_text.append("/git rebase [branch]   - Rebase current branch\n", style="white")
                    help_text.append("/git bisect start      - Start binary search for bugs\n", style="white")
                    help_text.append("/git tag [name]        - Create a tag\n", style="white")
                    help_text.append("/git reflog            - Show reference log\n", style="white")
                    help_text.append("/git new-branch [name] - Create and switch to new branch\n", style="white")
                    help_text.append("/git undo-last-commit  - Undo last commit (keep changes)\n", style="white")
                    help_text.append("/git amend [message]   - Amend last commit message\n", style="white")
                    help_text.append("/git uncommit          - Uncommit but keep changes staged\n", style="white")
                    help_text.append("/git discard           - Discard all unstaged changes\n", style="white")
                    help_text.append("/git ignore [pattern]  - Add pattern to .gitignore\n", style="white")
                    help_text.append("/git repo-info         - Show comprehensive repo information\n", style="white")
                    help_text.append("/git init              - Initialize a new Git repository\n", style="white")
                    help_text.append("/git clone [url]       - Clone a repository\n", style="white")
                    help_text.append("/git fetch             - Fetch all branches from remote\n", style="white")
                    help_text.append("/git contributors      - Show contributors by commit count\n", style="white")
                    help_text.append("/git file-history [f]  - Show history of a specific file\n", style="white")
                    help_text.append("/git clean             - Remove untracked files\n", style="white")
                    help_text.append("/git stats             - Show repository statistics\n\n", style="white")

                    help_text.append("💡 EXAMPLES:\n", style="bold green")
                    help_text.append("• Write a Python function to sort a list\n", style="cyan")
                    help_text.append("• /switch ollama llama2:13b\n", style="cyan")
                    help_text.append("• /ollama-models\n", style="cyan")
                    help_text.append("• /run ls -la\n", style="cyan")
                    help_text.append("• Explain quantum computing\n\n", style="cyan")

                    # Add new advanced features section
                    help_text.append("🚀 ADVANCED FEATURES:\n", style="bold magenta")
                    
                    help_text.append("🤖 CONTEXT-AWARE AI:\n", style="bold yellow")
                    help_text.append("/learn [topic]          - Teach AI about technologies\n", style="white")
                    help_text.append("/remind [task]          - Set task reminders\n", style="white")
                    help_text.append("/reminders              - View active reminders\n", style="white")
                    help_text.append("/complete-reminder [n]  - Mark reminder as complete\n\n", style="white")

                    help_text.append("📊 ANALYTICS & MONITORING:\n", style="bold yellow")
                    help_text.append("/analytics              - View usage statistics\n", style="white")
                    help_text.append("/error-analytics        - View error analytics\n", style="white")
                    help_text.append("/start-monitoring       - Start system monitoring\n", style="white")
                    help_text.append("/stop-monitoring        - Stop system monitoring\n", style="white")
                    help_text.append("/net-diag               - Network diagnostics\n", style="white")
                    help_text.append("/analyze-logs           - Analyze log files\n", style="white")
                    help_text.append("/health                 - System health check\n\n", style="white")

                    help_text.append("🎮 GAMES & LEARNING:\n", style="bold yellow")
                    help_text.append("/challenge [difficulty] - Get coding challenge\n", style="white")
                    help_text.append("/submit-challenge [id] [pid] [code] - Submit solution\n", style="white")
                    help_text.append("/tutorial [topic]       - Start interactive tutorial\n", style="white")
                    help_text.append("/tutorial-section [id] [num] - Get tutorial section\n", style="white")
                    help_text.append("/quiz [topic]           - Take interactive quiz\n", style="white")
                    help_text.append("/answer-quiz [id] [num] - Answer quiz question\n", style="white")
                    help_text.append("/user-stats             - View learning statistics\n\n", style="white")

                    help_text.append("🎨 CREATIVE TOOLS:\n", style="bold yellow")
                    help_text.append("/ascii [text]           - Generate ASCII art\n", style="white")
                    help_text.append("/colors [type] [base]   - Generate color schemes\n", style="white")
                    help_text.append("/music [mood] [length]  - Generate music patterns\n", style="white")
                    help_text.append("/story [genre] [length] - Generate creative stories\n\n", style="white")

                    help_text.append("🔒 ADVANCED SECURITY:\n", style="bold yellow")
                    help_text.append("/encrypt [message]      - Encrypt messages\n", style="white")
                    help_text.append("/decrypt [message]      - Decrypt messages\n", style="white")
                    help_text.append("/rotate-key [service] [key] - Rotate API keys\n", style="white")
                    help_text.append("/biometric-auth [data]  - Biometric authentication\n", style="white")
                    help_text.append("/secure-password [len]  - Generate secure passwords\n", style="white")
                    help_text.append("/security-report        - View security report\n", style="white")
                    help_text.append("/threat-scan [text]     - Scan for security threats\n\n", style="white")

                    help_text.append("🎨 THEME MANAGEMENT:\n", style="bold yellow")
                    help_text.append("/themes                  - List all available themes\n", style="white")
                    help_text.append("/theme set [name]        - Switch to a theme\n", style="white")
                    help_text.append("/theme current           - Show current theme\n", style="white")
                    help_text.append("/theme preview [name]    - Preview a theme\n", style="white")
                    help_text.append("/theme create [name] [base] - Create custom theme\n", style="white")
                    help_text.append("/theme delete [name]     - Delete custom theme\n", style="white")
                    help_text.append("/theme export [name] [fmt] - Export theme (json/python)\n", style="white")
                    help_text.append("/theme stats             - Show theme statistics\n", style="white")
                    help_text.append("/theme reset             - Reset to default theme\n\n", style="white")

                    help_text.append("� CODE REVIEW ASSISTANT:\n", style="bold yellow")
                    help_text.append("/review analyze [file]   - Full code analysis\n", style="white")
                    help_text.append("/review security [file]  - Security analysis only\n", style="white")
                    help_text.append("/review performance [file] - Performance analysis only\n", style="white")
                    help_text.append("/review quality [file]   - Quality metrics only\n", style="white")
                    help_text.append("/review compare [f1] [f2] - Compare two files\n", style="white")
                    help_text.append("/review suggest [file]   - AI improvement suggestions\n", style="white")
                    help_text.append("/review language [file]  - Detect programming language\n", style="white")
                    help_text.append("/review history          - Recent review history\n", style="white")
                    help_text.append("/review stats            - Review statistics\n\n", style="white")

                    help_text.append("�📝 TASK MANAGEMENT:\n", style="bold yellow")
                    help_text.append("/task add [title]       - Add a new task\n", style="white")
                    help_text.append("/task create [title]    - Create a new task\n", style="white")
                    help_text.append("/tasks                  - List all pending tasks\n", style="white")
                    help_text.append("/task show [id]         - Show task details\n", style="white")
                    help_text.append("/task complete [id]     - Mark task as completed\n", style="white")
                    help_text.append("/task delete [id]       - Delete a task\n", style="white")
                    help_text.append("/task update [id] [field] [value] - Update task field\n", style="white")
                    help_text.append("/task priority [id] [priority] - Set priority (low/medium/high/urgent)\n", style="white")
                    help_text.append("/task category [id] [category] - Set task category\n", style="white")
                    help_text.append("/task due [id] [date]   - Set due date (YYYY-MM-DD)\n", style="white")
                    help_text.append("/task subtask add [task_id] [title] - Add subtask\n", style="white")
                    help_text.append("/task subtask complete [task_id] [subtask_id] - Complete subtask\n", style="white")
                    help_text.append("/task stats             - Show task statistics\n", style="white")
                    help_text.append("/task search [query]    - Search tasks\n", style="white")
                    help_text.append("/task overdue           - Show overdue tasks\n", style="white")
                    help_text.append("/task export [format]   - Export tasks (json/csv)\n\n", style="white")

                    console.print(Panel(help_text, border_style="bright_green", padding=(1, 2)))
                    return ""
                except Exception as e:
                    return f"❌ Error displaying help: {str(e)}"
            
            elif cmd.startswith("setkey"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /setkey [provider] [key]"
                ok, msg = self.user_manager.set_api_key(parts[1], parts[2])
                # Set environment variable for session
                if ok:
                    if parts[1] == "openai":
                        os.environ["OPENAI_API_KEY"] = parts[2]
                    if parts[1] == "mcp":
                        os.environ["MCP_API_KEY"] = parts[2]
                return msg
            
            elif cmd.startswith("switch"):
                parts = cmd.split()
                if len(parts) < 2:
                    return "❌ Usage: /switch [model] [optional: specific_model]\n   Examples: /switch ollama, /switch ollama llama2:13b, /switch gemini"
                
                new_model = parts[1]
                valid_models = ["gemini", "groq", "ollama", "huggingface", "chatgpt", "mcp"]
                
                if new_model == "ollama":
                    # Handle Ollama model switching
                    if len(parts) >= 3:
                        # User specified a specific Ollama model
                        specific_model = parts[2]
                        try:
                            # Check if the model exists
                            ollama_models = ollama.list()["models"]
                            model_names = [m["name"] for m in ollama_models]
                            
                            if specific_model in model_names:
                                self.current_model = f"ollama:{specific_model}"
                                self._save_config()
                                return f"✅ Switched to Ollama model: {specific_model}"
                            else:
                                available = ", ".join(model_names[:5])  # Show first 5
                                return f"❌ Model '{specific_model}' not found.\n   Available: {available}{'...' if len(model_names) > 5 else ''}\n   Use /ollama-models to see all available models"
                        except Exception as e:
                            return f"❌ Error checking Ollama models: {str(e)}\n   Make sure Ollama is running"
                    else:
                        # Just switch to Ollama (default model)
                        self.current_model = "ollama"
                        self._save_config()
                        return "✅ Switched to Ollama (default model)"
                
                elif new_model in valid_models:
                    self.current_model = new_model
                    self._save_config()
                    return f"✅ Switched to {new_model.upper()}"
                
                return f"❌ Invalid model. Choose from: {', '.join(valid_models)}\n   For Ollama: /switch ollama [model_name]"
            # --- Web Search ---
            if cmd.startswith("websearch"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /websearch [query] - Search the web using DuckDuckGo"
                query = parts[1]
                try:
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[bold blue]🔍 Searching the web..."),
                        transient=True
                    ) as progress:
                        progress.add_task("search", total=None)

                        resp = self.ai.session.get(
                            f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}",
                            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
                            timeout=15
                        )

                    if resp.status_code == 200:
                        # Enhanced result extraction
                        import re
                        results = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', resp.text)

                        if not results:
                            return "🔍 No search results found. Try different keywords."

                        # Create a nice table for results
                        search_table = Table(title=f"🔍 Web Search Results for: '{query}'", show_header=True, header_style="bold blue")
                        search_table.add_column("#", style="cyan", width=3)
                        search_table.add_column("Title", style="white", min_width=40)
                        search_table.add_column("URL", style="green", min_width=30)

                        for i, (url, title) in enumerate(results[:8]):  # Show more results
                            clean_title = re.sub('<.*?>', '', title).strip()
                            if len(clean_title) > 60:
                                clean_title = clean_title[:57] + "..."

                            # Clean up URL
                            if url.startswith('//'):
                                url = 'https:' + url
                            elif url.startswith('/'):
                                url = 'https://duckduckgo.com' + url

                            search_table.add_row(str(i+1), clean_title, url)

                        console.print(search_table)
                        console.print(f"\n📊 Found {len(results)} results (showing top 8)")
                        console.print("💡 Click on URLs to visit the pages")
                        return ""

                    return f"❌ Web search error: HTTP {resp.status_code}"

                except requests.exceptions.Timeout:
                    return "❌ Web search timed out. Try again later."
                except requests.exceptions.ConnectionError:
                    return "❌ No internet connection. Check your network."
                except Exception as e:
                    return f"❌ Web search failed: {str(e)[:100]}"
            # --- Voice Input Command ---
            try:
                import speech_recognition as sr
            except ImportError:
                sr = None

            def listen_voice():
                if not sr:
                    return "SpeechRecognition not installed. Please install it to use voice input."
                recognizer = sr.Recognizer()
                with sr.Microphone() as source:
                    print("🎤 Speak now...")
                    audio = recognizer.listen(source, timeout=5)
                try:
                    text = recognizer.recognize_google(audio)
                    print(f"You said: {text}")
                    return text
                except Exception as e:
                    return f"Voice recognition failed: {str(e)}"

            if cmd.startswith("voice"):
                return listen_voice()

            # === NEW ADVANCED FEATURES ===

            # --- Context-Aware AI ---
            if cmd.startswith("learn"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /learn [topic] - Teach AI about a technology/framework"
                if not self.context_ai:
                    return "❌ Context-Aware AI module not available"
                topic, content = parts[1], f"User is learning about {parts[1]}"
                return self.context_ai.learn_topic(topic, content)

            if cmd == "remind":
                return "Usage: /remind [task] - Set a reminder (optional: deadline)"

            if cmd.startswith("remind "):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /remind [task] - Set a reminder"
                if not self.context_ai:
                    return "❌ Context-Aware AI module not available"
                return self.context_ai.remind_task(parts[1])

            if cmd == "reminders":
                if not self.context_ai:
                    return "❌ Context-Aware AI module not available"
                reminders = self.context_ai.get_reminders()
                if not reminders:
                    return "📝 No active reminders"
                output = "📝 Your Reminders:\n"
                for i, reminder in enumerate(reminders):
                    output += f"{i+1}. {reminder['task']}"
                    if reminder.get('deadline'):
                        output += f" (Due: {reminder['deadline']})"
                    output += "\n"
                return output

            if cmd.startswith("complete-reminder"):
                parts = command.split()
                if len(parts) != 2:
                    return "Usage: /complete-reminder [number]"
                if not self.context_ai:
                    return "❌ Context-Aware AI module not available"
                try:
                    index = int(parts[1]) - 1
                    return self.context_ai.complete_reminder(index)
                except ValueError:
                    return "❌ Invalid reminder number"

            # --- Theme Management ---
            if cmd == "themes":
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                return self.theme_manager.list_themes()

            if cmd.startswith("theme set"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /theme set [theme_name] - Switch to a theme"
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                result = self.theme_manager.set_current_theme(parts[2])
                # Update console theme immediately
                update_console_theme(self.theme_manager)
                return result

            if cmd == "theme current":
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                theme = self.theme_manager.get_current_theme()
                return f"🎨 Current Theme: {theme['name']} - {theme['description']}"

            if cmd.startswith("theme preview"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /theme preview [theme_name] - Preview a theme"
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                return self.theme_manager.preview_theme(parts[2])

            if cmd.startswith("theme create"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /theme create [name] [base_theme] - Create custom theme"
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                return self.theme_manager.create_custom_theme(parts[2], parts[3] if len(parts) > 3 else "dark")

            if cmd.startswith("theme delete"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /theme delete [theme_name] - Delete custom theme"
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                return self.theme_manager.delete_custom_theme(parts[2])

            if cmd.startswith("theme export"):
                parts = command.split()
                format_type = parts[2] if len(parts) > 2 else "json"
                if len(parts) < 3:
                    return "Usage: /theme export [theme_name] [format] - Export theme (json/python)"
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                return self.theme_manager.export_theme(parts[2], format_type)

            if cmd == "theme stats":
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                return self.theme_manager.get_theme_stats()

            if cmd == "theme reset":
                if not self.theme_manager:
                    return "❌ Theme Manager module not available"
                result = self.theme_manager.reset_to_default()
                # Update console theme immediately
                update_console_theme(self.theme_manager)
                return result

            # --- Code Review Assistant ---
            if cmd.startswith("review analyze"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /review analyze [file] - Analyze code quality"
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                analysis = self.code_reviewer.analyze_file(parts[2])
                return self.code_reviewer.generate_review_report(analysis)

            if cmd.startswith("review security"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /review security [file] - Security analysis only"
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                analysis = self.code_reviewer.analyze_file(parts[2], "security")
                return self.code_reviewer.generate_review_report(analysis)

            if cmd.startswith("review performance"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /review performance [file] - Performance analysis only"
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                analysis = self.code_reviewer.analyze_file(parts[2], "performance")
                return self.code_reviewer.generate_review_report(analysis)

            if cmd.startswith("review quality"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /review quality [file] - Quality metrics only"
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                analysis = self.code_reviewer.analyze_file(parts[2], "quality")
                return self.code_reviewer.generate_review_report(analysis)

            if cmd.startswith("review compare"):
                parts = command.split()
                if len(parts) != 4:
                    return "Usage: /review compare [file1] [file2] - Compare two files"
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                comparison = self.code_reviewer.compare_files(parts[2], parts[3])
                if "error" in comparison:
                    return f"❌ {comparison['error']}"
                output = f"📊 File Comparison Results:\n\n"
                output += f"📁 File 1: {comparison['file1']}\n"
                output += f"📁 File 2: {comparison['file2']}\n"
                output += f"📏 Lines: {comparison['file1_lines']} → {comparison['file2_lines']}\n"
                output += f"📈 Difference: {comparison['line_difference']} lines\n"
                output += f"🔗 Similarity: {comparison['similarity_score']}%\n"
                return output

            if cmd == "review history":
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                history = self.code_reviewer.get_review_history(10)
                if not history:
                    return "📝 No review history found"
                output = "📋 Recent Code Reviews:\n\n"
                for i, review in enumerate(history[-10:], 1):
                    output += f"{i}. 📁 {review['file_path']}\n"
                    output += f"   🗣️ {review['language']} | 📅 {review['timestamp'][:10]}\n"
                    if "quality_metrics" in review and "quality_score" in review["quality_metrics"]:
                        score = review["quality_metrics"]["quality_score"]
                        output += f"   📊 Quality: {score}/100\n"
                    output += "\n"
                return output

            if cmd == "review stats":
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                stats = self.code_reviewer.get_review_stats()
                output = "📊 Code Review Statistics:\n\n"
                output += f"📝 Total Reviews: {stats['total_reviews']}\n"
                output += f"🗣️ Languages: {', '.join(stats.get('languages_reviewed', []))}\n"
                output += f"📊 Avg Quality Score: {stats.get('avg_quality_score', 0)}/100\n"
                output += f"🔒 Security Issues Found: {stats.get('security_issues_found', 0)}\n"
                output += f"⚡ Performance Suggestions: {stats.get('performance_suggestions', 0)}\n"
                return output

            if cmd.startswith("review suggest"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /review suggest [file] - Get AI-powered improvement suggestions"
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                if not os.path.exists(parts[1]):
                    return f"❌ File not found: {parts[1]}"
                try:
                    with open(parts[1], 'r') as f:
                        code = f.read(2000)  # Limit to 2000 chars for AI processing
                    return self.ai.query(self.current_model, f"Review this code and provide improvement suggestions:\n\n```{self.code_reviewer.detect_language(parts[1])}\n{code}\n```")
                except Exception as e:
                    return f"❌ Error reading file: {str(e)}"

            if cmd.startswith("review language"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /review language [file] - Detect programming language"
                if not self.code_reviewer:
                    return "❌ Code Review Assistant module not available"
                language = self.code_reviewer.detect_language(parts[2])
                if language:
                    return f"🗣️ Detected Language: {language.upper()}"
                else:
                    return f"❓ Could not detect language for: {parts[2]}"

            # --- Integration Hub ---
            if cmd == "integrate":
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                return "🔗 Integration Hub Commands:\n" \
                       "• /integrate list - List configured services\n" \
                       "• /integrate supported - List supported services\n" \
                       "• /integrate add [service] - Add a service\n" \
                       "• /integrate remove [service] - Remove a service\n" \
                       "• /integrate test [service] - Test connection\n" \
                       "• /integrate info [service] - Service information\n" \
                       "• /integrate action [service] [action] - Execute action"

            if cmd == "integrate list":
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                return self.integration_hub.list_services()

            if cmd == "integrate supported":
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                return self.integration_hub.list_supported_services()

            if cmd.startswith("integrate add"):
                parts = command.split(maxsplit=2)
                if len(parts) < 3:
                    return "Usage: /integrate add [service] [config_json] - Add service integration"
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                try:
                    config = json.loads(parts[2])
                    return self.integration_hub.add_service(parts[1], config)
                except json.JSONDecodeError:
                    return "❌ Invalid JSON configuration"

            if cmd.startswith("integrate remove"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /integrate remove [service] - Remove service integration"
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                return self.integration_hub.remove_service(parts[2])

            if cmd.startswith("integrate test"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /integrate test [service] - Test service connection"
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                return self.integration_hub.test_connection(parts[2])

            if cmd.startswith("integrate info"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /integrate info [service] - Get service information"
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                return self.integration_hub.get_service_info(parts[2])

            if cmd.startswith("integrate action"):
                parts = command.split(maxsplit=3)
                if len(parts) < 4:
                    return "Usage: /integrate action [service] [action] [params_json] - Execute service action"
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                try:
                    params = json.loads(parts[3]) if len(parts) > 3 else {}
                    return self.integration_hub.execute_service_action(parts[1], parts[2], **params)
                except json.JSONDecodeError:
                    return "❌ Invalid JSON parameters"

            if cmd == "integrate stats":
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                stats = self.integration_hub.get_integration_stats()
                output = "📊 Integration Statistics:\n\n"
                output += f"🔗 Configured Services: {stats['total_services']}\n"
                output += f"🚀 Supported Services: {stats['supported_services']}\n"
                output += f"🟢 Connected Services: {stats['connected_services']}\n"
                output += f"🔴 Failed Connections: {stats['failed_connections']}\n"
                output += f"🪝 Total Webhooks: {stats['total_webhooks']}\n"
                output += f"✅ Active Webhooks: {stats['active_webhooks']}\n"
                return output

            if cmd == "webhooks":
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                return self.integration_hub.list_webhooks()

            if cmd.startswith("webhook add"):
                parts = command.split(maxsplit=3)
                if len(parts) < 4:
                    return "Usage: /webhook add [service] [url] [events_json] - Add webhook"
                if not self.integration_hub:
                    return "❌ Integration Hub module not available"
                try:
                    events = json.loads(parts[3])
                    return self.integration_hub.setup_webhook(parts[1], parts[2], events)
                except json.JSONDecodeError:
                    return "❌ Invalid JSON events list"

            # --- Task Management ---
            if cmd.startswith("task add"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /task add [title] - Add a new task"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.create_task(parts[1])

            if cmd.startswith("task create"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /task create [title] - Create a new task"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.create_task(parts[1])

            if cmd == "tasks":
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                tasks = self.task_manager.get_tasks(status="pending", limit=20)
                if not tasks:
                    return "📝 No pending tasks found"
                output = "📋 Your Tasks:\n\n"
                for i, task in enumerate(tasks, 1):
                    priority_icon = {"low": "🟢", "medium": "🟡", "high": "🔴", "urgent": "🟣"}.get(task["priority"], "⚪")
                    category_icon = self.task_manager.categories.get(task["category"], {}).get("icon", "📝")
                    output += f"{i}. {priority_icon} {category_icon} {task['title']}\n"
                    if task.get("due_date"):
                        due_date = datetime.fromtimestamp(float(task["due_date"])).strftime("%Y-%m-%d")
                        output += f"   📅 Due: {due_date}\n"
                    output += "\n"
                return output

            if cmd.startswith("task show"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /task show [id] - Show task details"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                task = self.task_manager.get_task_by_id(parts[2])
                if not task:
                    return f"❌ Task not found: {parts[2]}"
                output = f"📝 Task Details: {task['title']}\n\n"
                output += f"ID: {task['id']}\n"
                output += f"Status: {task['status'].upper()}\n"
                output += f"Priority: {task['priority'].upper()}\n"
                output += f"Category: {task['category'].title()}\n"
                if task.get("description"):
                    output += f"Description: {task['description']}\n"
                if task.get("due_date"):
                    due_date = datetime.fromtimestamp(float(task["due_date"])).strftime("%Y-%m-%d %H:%M")
                    output += f"Due Date: {due_date}\n"
                if task.get("tags"):
                    output += f"Tags: {', '.join(task['tags'])}\n"
                if task.get("subtasks"):
                    output += "Subtasks:\n"
                    for subtask in task["subtasks"]:
                        status = "✅" if subtask["completed"] else "❌"
                        output += f"  {status} {subtask['title']}\n"
                return output

            if cmd.startswith("task complete"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /task complete [id] - Mark task as completed"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.complete_task(parts[2])

            if cmd.startswith("task delete"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /task delete [id] - Delete a task"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.delete_task(parts[2])

            if cmd.startswith("task update"):
                parts = command.split(maxsplit=3)
                if len(parts) < 4:
                    return "Usage: /task update [id] [field] [value] - Update task field"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                task_id, field, value = parts[2], parts[3], " ".join(parts[4:])
                return self.task_manager.update_task(task_id, **{field: value})

            if cmd.startswith("task priority"):
                parts = command.split()
                if len(parts) != 4:
                    return "Usage: /task priority [id] [priority] - Set task priority (low/medium/high/urgent)"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.update_task(parts[2], priority=parts[3])

            if cmd.startswith("task category"):
                parts = command.split()
                if len(parts) != 4:
                    return "Usage: /task category [id] [category] - Set task category"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.update_task(parts[2], category=parts[3])

            if cmd.startswith("task due"):
                parts = command.split()
                if len(parts) != 4:
                    return "Usage: /task due [id] [date] - Set due date (YYYY-MM-DD)"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                try:
                    due_timestamp = datetime.strptime(parts[3], "%Y-%m-%d").timestamp()
                    return self.task_manager.update_task(parts[2], due_date=due_timestamp)
                except ValueError:
                    return "❌ Invalid date format. Use YYYY-MM-DD"

            if cmd.startswith("task subtask add"):
                parts = command.split(maxsplit=3)
                if len(parts) < 4:
                    return "Usage: /task subtask add [task_id] [title] - Add subtask"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.add_subtask(parts[3], " ".join(parts[4:]))

            if cmd.startswith("task subtask complete"):
                parts = command.split()
                if len(parts) != 5:
                    return "Usage: /task subtask complete [task_id] [subtask_id] - Complete subtask"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                return self.task_manager.complete_subtask(parts[3], parts[4])

            if cmd == "task stats":
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                stats = self.task_manager.get_task_stats()
                if "error" in stats:
                    return f"❌ {stats['error']}"
                output = "📊 Task Statistics:\n\n"
                output += f"Total Tasks: {stats['total_tasks']}\n"
                output += f"Completed: {stats['completed_tasks']}\n"
                output += f"Pending: {stats['pending_tasks']}\n"
                output += ".1f"
                output += "\nPriority Breakdown:\n"
                for priority, count in stats['priority_breakdown'].items():
                    output += f"  {priority.title()}: {count}\n"
                output += "\nCategory Breakdown:\n"
                for category, count in stats['category_breakdown'].items():
                    output += f"  {category.title()}: {count}\n"
                return output

            if cmd.startswith("task search"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /task search [query] - Search tasks"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                results = self.task_manager.search_tasks(parts[1])
                if not results:
                    return f"🔍 No tasks found matching: {parts[1]}"
                output = f"🔍 Search Results for '{parts[1]}':\n\n"
                for task in results[:10]:
                    output += f"📝 {task['title']} (ID: {task['id']})\n"
                    output += f"   Status: {task['status']} | Priority: {task['priority']}\n\n"
                return output

            if cmd == "task overdue":
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                overdue = self.task_manager.get_overdue_tasks()
                if not overdue:
                    return "✅ No overdue tasks!"
                output = "⚠️ Overdue Tasks:\n\n"
                for task in overdue:
                    due_date = datetime.fromtimestamp(float(task["due_date"])).strftime("%Y-%m-%d")
                    output += f"📝 {task['title']} (ID: {task['id']})\n"
                    output += f"   Was due: {due_date}\n\n"
                return output

            if cmd.startswith("task export"):
                parts = command.split()
                format_type = parts[1] if len(parts) > 1 else "json"
                if not self.task_manager:
                    return "❌ Task Manager module not available"
                export_data = self.task_manager.export_tasks(format_type)
                if format_type == "json":
                    return f"📄 JSON Export:\n{export_data}"
                else:
                    return f"📄 CSV Export:\n{export_data}"

            # --- Analytics & Monitoring ---
            if cmd == "analytics":
                if not self.analytics:
                    return "❌ Analytics module not available"
                stats = self.analytics.get_usage_stats()
                output = "📊 Usage Analytics:\n"
                output += f"Total Interactions: {stats['total_interactions']}\n"
                output += "Feature Usage:\n"
                for feature, count in stats['feature_usage'].items():
                    output += f"  {feature}: {count}\n"
                return output

            if cmd == "error-analytics":
                if not self.analytics:
                    return "❌ Analytics module not available"
                errors = self.analytics.get_error_analytics()
                output = "❌ Error Analytics:\n"
                output += f"Total Errors: {errors['total_errors']}\n"
                output += "Error Types:\n"
                for error_type, count in errors['error_types'].items():
                    output += f"  {error_type}: {count}\n"
                return output

            if cmd == "start-monitoring":
                if not self.analytics:
                    return "❌ Analytics module not available"
                return self.analytics.start_monitoring()

            if cmd == "stop-monitoring":
                if not self.analytics:
                    return "❌ Analytics module not available"
                return self.analytics.stop_monitoring()

            if cmd == "net-diag":
                if not self.analytics:
                    return "❌ Analytics module not available"
                diag = self.analytics.network_diagnostics()
                if "error" in diag:
                    return f"❌ {diag['error']}"
                output = "🌐 Network Diagnostics:\n"
                for service, status in diag['connectivity'].items():
                    output += f"{service}: {'✅' if status.get('status') == 'reachable' else '❌'} "
                    if 'latency_ms' in status:
                        output += f"({status['latency_ms']}ms)"
                    output += "\n"
                return output

            if cmd == "analyze-logs":
                if not self.analytics:
                    return "❌ Analytics module not available"
                analysis = self.analytics.analyze_logs()
                if "error" in analysis:
                    return f"❌ {analysis['error']}"
                output = "📋 Log Analysis:\n"
                output += f"Files Analyzed: {analysis['files_analyzed']}\n"
                output += f"Total Lines: {analysis['total_lines']}\n"
                output += f"Errors: {analysis['error_count']}\n"
                output += f"Warnings: {analysis['warning_count']}\n"
                return output

            if cmd == "health":
                if not self.analytics:
                    return "❌ Analytics module not available"
                health = self.analytics.health_check()
                if "error" in health:
                    return f"❌ {health['error']}"
                output = "🏥 System Health Check:\n"
                output += f"Overall Status: {health['overall_status'].upper()}\n"
                for component, check in health['checks'].items():
                    status_icon = "✅" if check['status'] == "good" else "⚠️" if check['status'] == "warning" else "❌"
                    output += f"{component.title()}: {status_icon} {check['message']}\n"
                if health.get('recommendations'):
                    output += "\n💡 Recommendations:\n"
                    for rec in health['recommendations']:
                        output += f"• {rec}\n"
                return output

            # --- Games & Learning ---
            if cmd.startswith("challenge"):
                parts = command.split()
                difficulty = parts[1] if len(parts) > 1 else "easy"
                if not self.games:
                    return "❌ Games & Learning module not available"
                challenge = self.games.get_coding_challenge(difficulty)
                if "error" in challenge:
                    return f"❌ {challenge['error']}"
                output = f"🎯 {challenge['title']}\n"
                output += f"Difficulty: {challenge['difficulty'].upper()}\n"
                output += f"Problem: {challenge['problem']['question']}\n"
                output += f"Starter Code:\n{challenge['problem']['starter_code']}\n"
                return output

            if cmd.startswith("submit-challenge"):
                parts = command.split(maxsplit=3)
                if len(parts) < 4:
                    return "Usage: /submit-challenge [challenge_id] [problem_id] [solution]"
                if not self.games:
                    return "❌ Games & Learning module not available"
                result = self.games.submit_challenge_solution(parts[1], parts[2], parts[3])
                if "error" in result:
                    return f"❌ {result['error']}"
                output = f"📊 Challenge Result:\n"
                output += f"Score: {result['score']}%\n"
                output += f"Tests Passed: {result['passed']}/{result['total_tests']}\n"
                if result.get('achievements'):
                    output += f"Achievements: {', '.join(result['achievements'])}\n"
                return output

            if cmd.startswith("tutorial"):
                parts = command.split()
                tutorial_id = parts[1] if len(parts) > 1 else "python_intro"
                if not self.games:
                    return "❌ Games & Learning module not available"
                tutorial = self.games.start_tutorial(tutorial_id)
                if "error" in tutorial:
                    return f"❌ {tutorial['error']}"
                output = f"📚 {tutorial['title']}\n"
                output += f"Description: {tutorial['description']}\n"
                output += f"Sections: {tutorial['total_sections']}\n"
                return output

            if cmd.startswith("tutorial-section"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /tutorial-section [tutorial_id] [section_number]"
                if not self.games:
                    return "❌ Games & Learning module not available"
                try:
                    section_num = int(parts[2]) - 1
                    section = self.games.get_tutorial_section(parts[1], section_num)
                    if "error" in section:
                        return f"❌ {section['error']}"
                    output = f"📖 Section {section['section_index'] + 1}: {section['title']}\n\n"
                    output += f"{section['content']}\n\n"
                    output += "Examples:\n"
                    for example in section['examples']:
                        output += f"  {example}\n"
                    return output
                except ValueError:
                    return "❌ Invalid section number"

            if cmd.startswith("quiz"):
                parts = command.split()
                quiz_id = parts[1] if len(parts) > 1 else "python_fundamentals"
                if not self.games:
                    return "❌ Games & Learning module not available"
                quiz = self.games.take_quiz(quiz_id)
                if "error" in quiz:
                    return f"❌ {quiz['error']}"
                if quiz.get('completed'):
                    return f"🎉 Quiz Completed!\nFinal Score: {quiz['final_score']}%\nCorrect: {quiz['correct_answers']}/{quiz['total_questions']}"
                output = f"❓ Question {quiz['question_number']}/{quiz['total_questions']}\n"
                output += f"{quiz['question']}\n\n"
                for i, option in enumerate(quiz['options']):
                    output += f"{i+1}. {option}\n"
                return output

            if cmd.startswith("answer-quiz"):
                parts = command.split(maxsplit=2)
                if len(parts) != 3:
                    return "Usage: /answer-quiz [quiz_id] [answer_number]"
                if not self.games:
                    return "❌ Games & Learning module not available"
                try:
                    answer_num = int(parts[2]) - 1
                    if 0 <= answer_num < 4:  # Assuming 4 options max
                        answer = ["A", "B", "C", "D"][answer_num]
                        result = self.games.submit_quiz_answer(parts[1], answer)
                        if "error" in result:
                            return f"❌ {result['error']}"
                        correctness = "✅ Correct!" if result['correct'] else "❌ Incorrect"
                        output = f"{correctness}\n"
                        output += f"Explanation: {result['explanation']}\n"
                        if result.get('next_question'):
                            output += f"Next question ready. Use /quiz {parts[1]} to continue."
                        return output
                    else:
                        return "❌ Invalid answer number (1-4)"
                except ValueError:
                    return "❌ Invalid answer number"

            if cmd == "user-stats":
                if not self.games:
                    return "❌ Games & Learning module not available"
                stats = self.games.get_user_stats()
                if "error" in stats:
                    return f"❌ {stats['error']}"
                output = "🏆 Your Stats:\n"
                output += f"Challenges Completed: {stats['challenges_completed']}\n"
                output += f"Average Score: {stats['average_score']:.1f}%\n"
                output += f"Achievements: {stats['achievement_count']}\n"
                return output

            # --- Creative Tools ---
            if cmd.startswith("ascii"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /ascii [text] - Generate ASCII art"
                if not self.creative:
                    return "❌ Creative Tools module not available"
                art = self.creative.generate_ascii_art(parts[1])
                return f"🎨 ASCII Art:\n{art}"

            if cmd.startswith("colors"):
                parts = command.split()
                scheme_type = parts[1] if len(parts) > 1 else "complementary"
                base_color = parts[2] if len(parts) > 2 else None
                if not self.creative:
                    return "❌ Creative Tools module not available"
                scheme = self.creative.generate_color_scheme(base_color, scheme_type)
                if "error" in scheme:
                    return f"❌ {scheme['error']}"
                output = f"🎨 Color Scheme ({scheme['type']}):\n"
                for i, color in enumerate(scheme['colors']):
                    output += f"Color {i+1}: {color}\n"
                return output

            if cmd.startswith("music"):
                parts = command.split()
                mood = parts[1] if len(parts) > 1 else "happy"
                length = int(parts[2]) if len(parts) > 2 else 8
                if not self.creative:
                    return "❌ Creative Tools module not available"
                music = self.creative.generate_music(mood, length)
                if "error" in music:
                    return f"❌ {music['error']}"
                output = f"🎵 {music['description']}\n"
                output += f"Notes: {music['notation']}\n"
                return output

            if cmd.startswith("story"):
                parts = command.split()
                genre = parts[1] if len(parts) > 1 else "fantasy"
                length = parts[2] if len(parts) > 2 else "short"
                if not self.creative:
                    return "❌ Creative Tools module not available"
                story = self.creative.generate_story(genre, length)
                if "error" in story:
                    return f"❌ {story['error']}"
                output = f"📖 {story['title']}\n\n"
                output += f"{story['story']}\n"
                return output

            # --- Advanced Security ---
            if cmd.startswith("encrypt"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /encrypt [message] - Encrypt a message"
                if not self.adv_security:
                    return "❌ Advanced Security module not available"
                encrypted = self.adv_security.encrypt_message(parts[1])
                return f"🔐 Encrypted: {encrypted}"

            if cmd.startswith("decrypt"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /decrypt [encrypted_message] - Decrypt a message"
                if not self.adv_security:
                    return "❌ Advanced Security module not available"
                decrypted = self.adv_security.decrypt_message(parts[1])
                return f"🔓 Decrypted: {decrypted}"

            if cmd.startswith("rotate-key"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /rotate-key [service] [current_key] - Rotate API key"
                if not self.adv_security:
                    return "❌ Advanced Security module not available"
                result = self.adv_security.rotate_api_key(parts[1], parts[2])
                if "error" in result:
                    return f"❌ {result['error']}"
                return f"🔄 Key rotated for {result['service']}\nNew Key: {result['new_key']}"

            if cmd.startswith("biometric-auth"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /biometric-auth [biometric_data] - Authenticate with biometrics"
                if not self.adv_security:
                    return "❌ Advanced Security module not available"
                user = self.user_manager.current_user or "anonymous"
                result = self.adv_security.biometric_authenticate(user, parts[1])
                if "error" in result:
                    return f"❌ {result['error']}"
                status = "✅" if result['authenticated'] else "❌"
                return f"{status} {result['message']}"

            if cmd.startswith("secure-password"):
                parts = command.split()
                length = int(parts[1]) if len(parts) > 1 else 16
                if not self.adv_security:
                    return "❌ Advanced Security module not available"
                password = self.adv_security.generate_secure_password(length)
                return f"🔐 Secure Password: {password}"

            if cmd == "security-report":
                if not self.adv_security:
                    return "❌ Advanced Security module not available"
                report = self.adv_security.get_security_report()
                if "error" in report:
                    return f"❌ {report['error']}"
                output = "🔒 Security Report:\n"
                output += f"Period: {report['period_days']} days\n"
                output += f"Total Events: {report['total_events']}\n"
                output += f"Threats Detected: {report['threats_detected']}\n"
                output += f"Auth Attempts: {report['auth_attempts']}\n"
                return output

            if cmd == "threat-scan":
                return "Usage: /threat-scan [text] - Scan text for security threats"

            if cmd.startswith("threat-scan"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /threat-scan [text] - Scan text for security threats"
                if not self.adv_security:
                    return "❌ Advanced Security module not available"
                threats = self.adv_security.detect_threats(parts[1])
                if not threats:
                    return "✅ No threats detected"
                output = "🚨 Threats Detected:\n"
                for threat in threats:
                    output += f"Pattern: {threat['pattern'][:50]}...\n"
                    output += f"Severity: {threat['severity'].upper()}\n"
                    output += f"Matches: {len(threat['matches'])}\n\n"
                return output

            if cmd == "run":
                return "Usage: /run [command] - Execute system commands like 'ls', 'pwd', 'whoami', etc."

            if cmd.startswith("run "):
                parts = cmd.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /run [command]"
                return self.execute_command(parts[1])

            # Handle unrecognized commands
            else:
                return f"❌ Unknown command: /{cmd}. Type /help for available commands."

        except Exception as e:
            logging.error(f"Command handling error: {str(e)}")
            return "❌ Command processing error"

# --- Main Loop ---
if __name__ == "__main__":
    try:
        console.print("[bold green]🚀 Starting Nexus AI Terminal...[/bold green]")
        ai = NexusAI()
        
        while True:
            try:
                model_display = ai.current_model.upper() if ai.current_model else "UNKNOWN"
                prompt = input(f"\n[{model_display}] 🚀 > ").strip()
                
                if prompt.lower() in ["exit", "/exit", "quit", "/quit"]:
                    console.print("\n[bold green]👋 Thanks for using Nexus AI Terminal![/bold green]")
                    console.print("[bold cyan]🚀 Keep innovating![/bold cyan]\n")
                    break
                
                if not prompt:
                    continue
                
                # Show thinking indicator for AI responses
                if not prompt.startswith("/"):
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[bold blue]🤖 AI is thinking..."),
                        transient=True
                    ) as progress:
                        progress.add_task("thinking", total=None)
                        response = ai.process_input(prompt)
                else:
                    response = ai.process_input(prompt)
                
                # Ensure response is always a string
                if response is None:
                    response = "❌ Error: Command returned no response"
                
                if response and isinstance(response, str) and response.strip():
                    console.print(f"\n[bold cyan]🤖 AI:[/bold cyan] {response}")
                elif response:
                    console.print(f"\n[bold cyan]🤖 AI:[/bold cyan] {response}")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]💡 Use '/exit' to quit gracefully[/yellow]")
                
    except Exception as e:
        logging.critical(f"Fatal error: {str(e)}")
        console.print(f"[bold red]💥 Critical error:[/bold red] {str(e)}")
        console.print("[yellow]Check ai_assistant.log for details[/yellow]")
        sys.exit(1)
    
    # Example: Using Gemini 2.5 Flash with google-generativeai
    import google.generativeai as genai
    import os
    
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("No Gemini API key found in environment variables.")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content("Explain how AI works in a few words")
        print(response.text)