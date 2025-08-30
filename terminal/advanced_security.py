#!/usr/bin/env python3
"""
Advanced Security Module for NEXUS AI Terminal
Provides biometric authentication, encrypted chat, API key rotation, and threat detection
"""

import os
import json
import time
import hashlib
import secrets
import base64
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import hmac
import threading
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class AdvancedSecurity:
    """Manages advanced security features"""

    def __init__(self):
        self.security_db_path = os.path.expanduser("~/.nexus/security.db")
        self.encryption_keys = {}
        self.api_keys = {}
        self.threat_patterns = []
        self.audit_log = []
        self.biometric_data = {}
        self.session_keys = {}
        self._load_security_data()
        self._initialize_security()

    def _load_security_data(self):
        """Load security database"""
        try:
            if os.path.exists(self.security_db_path):
                with open(self.security_db_path, 'r') as f:
                    data = json.load(f)
                    self.api_keys = data.get("api_keys", {})
                    self.audit_log = data.get("audit_log", [])
                    self.threat_patterns = data.get("threat_patterns", [])
        except Exception as e:
            print(f"Warning: Could not load security database: {e}")

    def _save_security_data(self):
        """Save security database"""
        try:
            os.makedirs(os.path.dirname(self.security_db_path), exist_ok=True)
            data = {
                "api_keys": self.api_keys,
                "audit_log": self.audit_log[-1000:],  # Keep last 1000 entries
                "threat_patterns": self.threat_patterns,
                "last_updated": time.time()
            }
            with open(self.security_db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save security database: {str(e)}")

    def _initialize_security(self):
        """Initialize security components"""
        self.threat_patterns = [
            r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?[a-zA-Z0-9]{6,}['\"]?",
            r"(?i)(api[_-]?key|apikey|token)\s*[:=]\s*['\"]?[a-zA-Z0-9_-]{20,}['\"]?",
            r"(?i)(select|union|drop|delete|update|insert).*from.*where",
            r"(?i)(eval|exec|system|shell_exec|passthru)\s*\(",
            r"(?i)<script[^>]*>.*?</script>",
            r"(?i)(javascript|vbscript|onload|onerror)\s*:",
            r"(?i)(base64_decode|base64_encode|gzinflate|gzdeflate)\s*\(",
            r"(?i)(chmod|chown|unlink|rmdir)\s*\("
        ]

    def generate_encryption_key(self) -> str:
        """Generate a new encryption key"""
        try:
            key = Fernet.generate_key()
            key_id = f"key_{int(time.time())}_{secrets.token_hex(4)}"
            self.encryption_keys[key_id] = {
                "key": key.decode(),
                "created": time.time(),
                "active": True
            }
            return key_id
        except Exception as e:
            return f"Error generating key: {str(e)}"

    def encrypt_message(self, message: str, key_id: str = None) -> str:
        """Encrypt a message"""
        try:
            if not key_id or key_id not in self.encryption_keys:
                key_id = self.generate_encryption_key()
                if "Error" in key_id:
                    return key_id

            key_data = self.encryption_keys[key_id]
            if not key_data["active"]:
                return "❌ Encryption key is inactive"

            fernet = Fernet(key_data["key"].encode())
            encrypted = fernet.encrypt(message.encode())
            return f"{key_id}:{encrypted.decode()}"

        except Exception as e:
            return f"❌ Encryption failed: {str(e)}"

    def decrypt_message(self, encrypted_message: str) -> str:
        """Decrypt a message"""
        try:
            if ":" not in encrypted_message:
                return "❌ Invalid encrypted message format"

            key_id, encrypted_data = encrypted_message.split(":", 1)

            if key_id not in self.encryption_keys:
                return "❌ Encryption key not found"

            key_data = self.encryption_keys[key_id]
            if not key_data["active"]:
                return "❌ Encryption key is inactive"

            fernet = Fernet(key_data["key"].encode())
            decrypted = fernet.decrypt(encrypted_data.encode())
            return decrypted.decode()

        except Exception as e:
            return f"❌ Decryption failed: {str(e)}"

    def rotate_api_key(self, service: str, current_key: str) -> Dict:
        """Rotate an API key for a service"""
        try:
            if service not in self.api_keys:
                self.api_keys[service] = {
                    "current": current_key,
                    "previous": [],
                    "last_rotated": time.time(),
                    "rotation_count": 0
                }

            # Generate new key (simplified - in reality, this would call the service's API)
            new_key = secrets.token_hex(32)

            # Store current key as previous
            key_data = self.api_keys[service]
            key_data["previous"].append({
                "key": key_data["current"],
                "rotated_at": time.time()
            })

            # Update with new key
            key_data["current"] = new_key
            key_data["last_rotated"] = time.time()
            key_data["rotation_count"] += 1

            # Keep only last 5 previous keys
            key_data["previous"] = key_data["previous"][-5:]

            self._save_security_data()

            return {
                "service": service,
                "new_key": new_key,
                "rotated_at": datetime.fromtimestamp(key_data["last_rotated"]).isoformat(),
                "rotation_count": key_data["rotation_count"]
            }

        except Exception as e:
            return {"error": f"Failed to rotate API key: {str(e)}"}

    def detect_threats(self, input_text: str) -> List[Dict]:
        """Detect potential security threats in input"""
        threats_detected = []

        try:
            for pattern in self.threat_patterns:
                import re
                matches = re.findall(pattern, input_text, re.IGNORECASE)
                if matches:
                    threats_detected.append({
                        "pattern": pattern,
                        "matches": matches[:5],  # Limit matches shown
                        "severity": self._assess_threat_severity(pattern),
                        "detected_at": time.time()
                    })

            # Log threats
            if threats_detected:
                self.audit_log.append({
                    "type": "threat_detected",
                    "threats": threats_detected,
                    "input_length": len(input_text),
                    "timestamp": time.time()
                })
                self._save_security_data()

        except Exception as e:
            threats_detected.append({
                "error": f"Threat detection failed: {str(e)}",
                "severity": "unknown"
            })

        return threats_detected

    def _assess_threat_severity(self, pattern: str) -> str:
        """Assess the severity of a detected threat pattern"""
        high_severity_patterns = [
            r"(?i)(select|union|drop|delete).*from",
            r"(?i)(eval|exec|system)",
            r"(?i)<script[^>]*>",
            r"(?i)(chmod|chown|unlink)"
        ]

        medium_severity_patterns = [
            r"(?i)(password|passwd|pwd)\s*[:=]",
            r"(?i)(api[_-]?key|apikey|token)\s*[:=]",
            r"(?i)(base64_decode|base64_encode)"
        ]

        for high_pattern in high_severity_patterns:
            if high_pattern in pattern:
                return "high"

        for medium_pattern in medium_severity_patterns:
            if medium_pattern in pattern:
                return "medium"

        return "low"

    def biometric_authenticate(self, user_id: str, biometric_data: str) -> Dict:
        """Simulate biometric authentication (fingerprint/face recognition)"""
        try:
            # In a real implementation, this would interface with biometric hardware
            # For simulation, we'll use a hash-based approach

            if user_id not in self.biometric_data:
                # First-time enrollment
                bio_hash = hashlib.sha256(biometric_data.encode()).hexdigest()
                self.biometric_data[user_id] = {
                    "biometric_hash": bio_hash,
                    "enrolled_at": time.time(),
                    "auth_attempts": 0,
                    "last_auth": None
                }
                self._save_security_data()
                return {
                    "authenticated": True,
                    "message": "Biometric data enrolled successfully",
                    "first_time": True
                }

            # Verify biometric data
            stored_hash = self.biometric_data[user_id]["biometric_hash"]
            input_hash = hashlib.sha256(biometric_data.encode()).hexdigest()

            authenticated = hmac.compare_digest(stored_hash, input_hash)

            self.biometric_data[user_id]["auth_attempts"] += 1
            self.biometric_data[user_id]["last_auth"] = time.time()

            if authenticated:
                self.biometric_data[user_id]["auth_attempts"] = 0  # Reset on success

            self._save_security_data()

            return {
                "authenticated": authenticated,
                "message": "Authentication successful" if authenticated else "Authentication failed",
                "attempts": self.biometric_data[user_id]["auth_attempts"]
            }

        except Exception as e:
            return {"error": f"Biometric authentication failed: {str(e)}"}

    def generate_secure_password(self, length: int = 16) -> str:
        """Generate a cryptographically secure password"""
        try:
            if length < 8 or length > 128:
                return "❌ Password length must be between 8-128 characters"

            # Character sets
            lowercase = "abcdefghijklmnopqrstuvwxyz"
            uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            digits = "0123456789"
            symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"

            # Ensure at least one character from each set
            password = [
                secrets.choice(lowercase),
                secrets.choice(uppercase),
                secrets.choice(digits),
                secrets.choice(symbols)
            ]

            # Fill the rest randomly
            all_chars = lowercase + uppercase + digits + symbols
            password.extend(secrets.choice(all_chars) for _ in range(length - 4))

            # Shuffle the password
            secrets.SystemRandom().shuffle(password)

            return "".join(password)

        except Exception as e:
            return f"❌ Failed to generate password: {str(e)}"

    def audit_log_event(self, event_type: str, user: str, details: Dict) -> None:
        """Log security events for auditing"""
        try:
            audit_entry = {
                "event_type": event_type,
                "user": user,
                "details": details,
                "timestamp": time.time(),
                "ip_address": "127.0.0.1",  # Would be actual IP in real implementation
                "user_agent": "NEXUS-AI-Terminal"
            }

            self.audit_log.append(audit_entry)
            self._save_security_data()

        except Exception as e:
            print(f"Warning: Failed to log audit event: {e}")

    def get_security_report(self, days: int = 7) -> Dict:
        """Generate a security report"""
        try:
            cutoff_time = time.time() - (days * 24 * 60 * 60)

            # Filter recent audit logs
            recent_logs = [
                log for log in self.audit_log
                if log.get("timestamp", 0) > cutoff_time
            ]

            # Analyze threats
            threats = [log for log in recent_logs if log.get("event_type") == "threat_detected"]
            auth_attempts = [log for log in recent_logs if "auth" in log.get("event_type", "")]

            # Group events by type
            event_types = {}
            for log in recent_logs:
                event_type = log.get("event_type", "unknown")
                if event_type not in event_types:
                    event_types[event_type] = 0
                event_types[event_type] += 1

            return {
                "period_days": days,
                "total_events": len(recent_logs),
                "threats_detected": len(threats),
                "auth_attempts": len(auth_attempts),
                "event_types": event_types,
                "most_common_event": max(event_types.items(), key=lambda x: x[1]) if event_types else None,
                "generated_at": time.time()
            }

        except Exception as e:
            return {"error": f"Failed to generate security report: {str(e)}"}

    def create_secure_session(self, user: str) -> str:
        """Create a secure session with encrypted communication"""
        try:
            session_id = f"session_{secrets.token_hex(16)}"
            session_key = secrets.token_hex(32)

            self.session_keys[session_id] = {
                "user": user,
                "key": session_key,
                "created": time.time(),
                "active": True,
                "messages": []
            }

            # Auto-cleanup old sessions
            self._cleanup_old_sessions()

            return session_id

        except Exception as e:
            return f"Error creating session: {str(e)}"

    def _cleanup_old_sessions(self):
        """Clean up expired sessions"""
        try:
            current_time = time.time()
            expired_sessions = []

            for session_id, session_data in self.session_keys.items():
                if current_time - session_data["created"] > 3600:  # 1 hour
                    expired_sessions.append(session_id)

            for session_id in expired_sessions:
                del self.session_keys[session_id]

        except Exception as e:
            print(f"Warning: Failed to cleanup sessions: {e}")

    def validate_session(self, session_id: str) -> bool:
        """Validate if a session is active"""
        try:
            if session_id not in self.session_keys:
                return False

            session = self.session_keys[session_id]
            if not session["active"]:
                return False

            # Check if session expired (1 hour)
            if time.time() - session["created"] > 3600:
                session["active"] = False
                return False

            return True

        except Exception as e:
            return False

    def get_active_sessions(self) -> List[Dict]:
        """Get list of active sessions"""
        try:
            active_sessions = []
            current_time = time.time()

            for session_id, session_data in self.session_keys.items():
                if session_data["active"] and current_time - session_data["created"] < 3600:
                    active_sessions.append({
                        "session_id": session_id,
                        "user": session_data["user"],
                        "created": session_data["created"],
                        "age_minutes": (current_time - session_data["created"]) / 60
                    })

            return active_sessions

        except Exception as e:
            return [{"error": f"Failed to get sessions: {str(e)}"}]