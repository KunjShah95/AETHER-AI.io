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

# --- Configuration ---
load_dotenv()
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
            r"sudo\\s", r"rm\\s+-[rf]", r"chmod\\s+777",
            r"wget\\s", r"curl\\s", r"\\|\\s*sh",
            r">\\s*/dev", r"nohup", r"fork\\(\\)",
            r"eval\\(", r"base64_decode", r"UNION\\s+SELECT",
            r"DROP\\s+TABLE", r"<script", r"javascript:"
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
                
                elif model == "ollama":
                    if not self._check_ollama():
                        return "❌ Ollama not available"
                    
                    response = ollama.chat(
                        model="llama3",
                        messages=[{"role": "user", "content": clean_prompt}]
                    )
                    
                    if not isinstance(response, dict) or "message" not in response:
                        raise APIError("Invalid Ollama response")
                    
                    content = response["message"].get("content", "")
                    if not content:
                        raise APIError("Empty Ollama response")
                    
                    return content[:2000]
                
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
            'ls', 'pwd', 'whoami', 'date', 'uptime', 'echo', 'cat', 'head', 'tail', 'df', 'du', 'free', 'uname', 'id'
        ]
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
    
    def process_input(self, user_input: str) -> str:
        try:
            clean_input = self.security.sanitize(user_input)
            if self.user_manager.current_user:
                self.user_manager.update_activity(self.user_manager.current_user, clean_input)
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
            return "🔒 Security block: Input contains dangerous content"
        except Exception as e:
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
                return self.execute_command(f"git branch {parts[2]}")
            if cmd.startswith("git delete-branch"):
                parts = command.split()
                if len(parts) != 3:
                    return "Usage: /git delete-branch [name]"
                return self.execute_command(f"git branch -d {parts[2]}")
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
                help_text.append("/switch ollama      - Switch to Ollama (local)\n", style="white")
                help_text.append("/switch huggingface - Switch to HuggingFace\n", style="white")
                help_text.append("/switch chatgpt     - Switch to ChatGPT (OpenAI)\n", style="white")
                help_text.append("/switch mcp         - Switch to MCP (Model Context Protocol)\n\n", style="white")
                help_text.append("⚙️ SYSTEM COMMANDS:\n", style="bold yellow")
                help_text.append("/run [command]      - Execute system command\n", style="white")
                help_text.append("/models             - List available models\n", style="white")
                help_text.append("/config             - Show configuration\n\n", style="white")
                help_text.append("💡 EXAMPLES:\n", style="bold green")
                help_text.append("• Write a Python function to sort a list\n", style="cyan")
                help_text.append("• /switch ollama\n", style="cyan")
                help_text.append("• /run ls -la\n", style="cyan")
                help_text.append("• Explain quantum computing\n\n", style="cyan")
                
                console.print(Panel(help_text, border_style="bright_green", padding=(1, 2)))
                return ""
            
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
                    return "❌ Usage: /switch [model]. Available: gemini, groq, ollama, huggingface, chatgpt, mcp"
                
                new_model = parts[1]
                valid_models = ["gemini", "groq", "ollama", "huggingface", "chatgpt", "mcp"]
                
                if new_model in valid_models:
                    self.current_model = new_model
                    self._save_config()
                    return f"✅ Switched to {new_model.upper()}"
                return f"❌ Invalid model. Choose from: {', '.join(valid_models)}"
            # --- Web Search ---
            if cmd.startswith("websearch"):
                parts = command.split(maxsplit=1)
                if len(parts) != 2:
                    return "Usage: /websearch [query]"
                query = parts[1]
                try:
                    resp = self.ai.session.get(
                        f"https://duckduckgo.com/html/?q={requests.utils.quote(query)}",
                        headers={"User-Agent": "Mozilla/5.0"}, timeout=10
                    )
                    if resp.status_code == 200:
                        # Simple extraction of results
                        import re
                        results = re.findall(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', resp.text)
                        if not results:
                            return "No results found."
                        summary = "\n".join([f"{i+1}. {re.sub('<.*?>', '', title)}\n{url}" for i, (url, title) in enumerate(results[:3])])
                        return summary
                    return f"Web search error: {resp.status_code}"
                except Exception as e:
                    return f"Web search failed: {str(e)[:100]}"
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
                prompt = input(f"\n[{ai.current_model.upper()}] 🚀 > ").strip()
                
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
                
                if response.strip():
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