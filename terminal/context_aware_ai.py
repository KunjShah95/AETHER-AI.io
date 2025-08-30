#!/usr/bin/env python3
"""
Context-Aware AI Module for NEXUS AI Terminal
Provides learning capabilities, project context awareness, and intelligent suggestions
"""

import os
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import hashlib
import re

class ContextAwareAI:
    """Manages project context, learning, and intelligent suggestions"""

    def __init__(self):
        self.context_db_path = os.path.expanduser("~/.nexus/context.db")
        self.learning_db_path = os.path.expanduser("~/.nexus/learning.db")
        self.project_patterns = {}
        self.user_knowledge = {}
        self.command_history = []
        self._load_context()
        self._load_learning()

    def _load_context(self):
        """Load project context database"""
        try:
            if os.path.exists(self.context_db_path):
                with open(self.context_db_path, 'r') as f:
                    self.project_patterns = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load context database: {e}")
            self.project_patterns = {}

    def _save_context(self):
        """Save project context database"""
        try:
            os.makedirs(os.path.dirname(self.context_db_path), exist_ok=True)
            with open(self.context_db_path, 'w') as f:
                json.dump(self.project_patterns, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save context database: {e}")

    def _load_learning(self):
        """Load learning database"""
        try:
            if os.path.exists(self.learning_db_path):
                with open(self.learning_db_path, 'r') as f:
                    self.user_knowledge = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load learning database: {e}")
            self.user_knowledge = {}

    def _save_learning(self):
        """Save learning database"""
        try:
            os.makedirs(os.path.dirname(self.learning_db_path), exist_ok=True)
            with open(self.learning_db_path, 'w') as f:
                json.dump(self.user_knowledge, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save learning database: {e}")

    def analyze_project_structure(self, project_path: str = ".") -> Dict:
        """Analyze project structure and extract patterns"""
        try:
            project_path = Path(project_path)
            if not project_path.exists():
                return {"error": "Project path does not exist"}

            structure = {
                "languages": [],
                "frameworks": [],
                "config_files": [],
                "dependencies": [],
                "structure": {},
                "patterns": []
            }

            # Analyze files and directories
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(project_path)

                    # Detect languages
                    if file.endswith(('.py', '.pyc')):
                        if 'python' not in structure["languages"]:
                            structure["languages"].append("python")
                    elif file.endswith(('.js', '.ts', '.jsx', '.tsx')):
                        if 'javascript' not in structure["languages"]:
                            structure["languages"].append("javascript")
                        if file.endswith(('.ts', '.tsx')):
                            if 'typescript' not in structure["languages"]:
                                structure["languages"].append("typescript")
                    elif file.endswith(('.java', '.class')):
                        if 'java' not in structure["languages"]:
                            structure["languages"].append("java")
                    elif file.endswith(('.cpp', '.cc', '.cxx', '.c++', '.hpp', '.h')):
                        if 'cpp' not in structure["languages"]:
                            structure["languages"].append("cpp")

                    # Detect frameworks and config files
                    if file in ['package.json']:
                        structure["frameworks"].append("node.js")
                        structure["config_files"].append(str(relative_path))
                    elif file in ['requirements.txt', 'setup.py', 'Pipfile']:
                        structure["frameworks"].append("python")
                        structure["config_files"].append(str(relative_path))
                    elif file in ['pom.xml', 'build.gradle']:
                        structure["frameworks"].append("java")
                        structure["config_files"].append(str(relative_path))
                    elif file in ['Cargo.toml']:
                        structure["frameworks"].append("rust")
                        structure["config_files"].append(str(relative_path))

            # Store patterns for this project
            project_hash = hashlib.md5(str(project_path).encode()).hexdigest()[:8]
            self.project_patterns[project_hash] = {
                "path": str(project_path),
                "structure": structure,
                "last_analyzed": time.time()
            }
            self._save_context()

            return structure

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    def learn_topic(self, topic: str, content: str) -> str:
        """Learn about a specific technology or framework"""
        try:
            if topic not in self.user_knowledge:
                self.user_knowledge[topic] = {
                    "content": [],
                    "learned_at": [],
                    "usage_count": 0
                }

            self.user_knowledge[topic]["content"].append(content)
            self.user_knowledge[topic]["learned_at"].append(time.time())
            self.user_knowledge[topic]["usage_count"] += 1

            self._save_learning()

            return f"✅ Learned about '{topic}'. Knowledge stored for future reference."

        except Exception as e:
            return f"❌ Learning failed: {str(e)}"

    def get_learning_suggestions(self, current_context: str) -> List[str]:
        """Get learning suggestions based on current context"""
        suggestions = []

        # Analyze current project context
        project_info = self.analyze_project_structure()

        if "python" in project_info.get("languages", []):
            if "django" not in self.user_knowledge:
                suggestions.append("Learn Django framework for Python web development")
            if "fastapi" not in self.user_knowledge:
                suggestions.append("Learn FastAPI for modern Python APIs")

        if "javascript" in project_info.get("languages", []):
            if "react" not in self.user_knowledge:
                suggestions.append("Learn React for modern web development")
            if "node.js" not in self.user_knowledge:
                suggestions.append("Learn Node.js for server-side JavaScript")

        # General suggestions based on usage patterns
        if len(self.command_history) > 10:
            recent_commands = self.command_history[-10:]
            if any("git" in cmd for cmd in recent_commands):
                if "git" not in self.user_knowledge:
                    suggestions.append("Learn advanced Git workflows and branching strategies")

        return suggestions[:5]  # Limit to 5 suggestions

    def suggest_commands(self, current_input: str, project_context: Dict) -> List[str]:
        """Suggest relevant commands based on context"""
        suggestions = []

        # Analyze input and context
        input_lower = current_input.lower()

        if "error" in input_lower or "bug" in input_lower:
            suggestions.extend([
                "/findbugs [file] - Find bugs in code",
                "/security-scan [file] - Scan for security vulnerabilities",
                "/lint [file] - Check code style and issues"
            ])

        if "test" in input_lower:
            suggestions.extend([
                "/test [file] - Run unit tests",
                "/gentest [file] - Generate unit tests"
            ])

        if "deploy" in input_lower or "build" in input_lower:
            suggestions.extend([
                "/create-project [type] - Create project templates",
                "/generate-code [lang] [desc] - Generate code"
            ])

        # Project-specific suggestions
        languages = project_context.get("languages", [])
        if "python" in languages:
            suggestions.extend([
                "/run-python [code] - Execute Python code",
                "/profile [file] - Profile Python performance"
            ])

        return suggestions[:3]  # Limit to 3 suggestions

    def recognize_patterns(self, code: str) -> List[str]:
        """Recognize common design patterns in code"""
        patterns = []

        # Singleton pattern
        if re.search(r'__instance\s*=\s*None', code) and re.search(r'@classmethod', code):
            patterns.append("Singleton Pattern")

        # Factory pattern
        if re.search(r'class.*Factory', code, re.IGNORECASE) and re.search(r'def create', code):
            patterns.append("Factory Pattern")

        # Observer pattern
        if re.search(r'add_observer|register|subscribe', code, re.IGNORECASE):
            patterns.append("Observer Pattern")

        # MVC pattern indicators
        if re.search(r'class.*Controller', code) and re.search(r'class.*Model', code):
            patterns.append("MVC Pattern")

        # Decorator pattern
        if re.search(r'@.*\ndef.*\(.*\):', code) and re.search(r'functools\.wraps', code):
            patterns.append("Decorator Pattern")

        return patterns

    def remind_task(self, task: str, deadline: Optional[str] = None) -> str:
        """Set a reminder for a task"""
        try:
            if "reminders" not in self.user_knowledge:
                self.user_knowledge["reminders"] = []

            reminder = {
                "task": task,
                "created_at": time.time(),
                "deadline": deadline,
                "completed": False
            }

            self.user_knowledge["reminders"].append(reminder)
            self._save_learning()

            response = f"✅ Reminder set: {task}"
            if deadline:
                response += f" (Deadline: {deadline})"

            return response

        except Exception as e:
            return f"❌ Failed to set reminder: {str(e)}"

    def get_reminders(self) -> List[Dict]:
        """Get active reminders"""
        if "reminders" not in self.user_knowledge:
            return []

        active_reminders = [
            r for r in self.user_knowledge["reminders"]
            if not r.get("completed", False)
        ]

        return active_reminders

    def complete_reminder(self, task_index: int) -> str:
        """Mark a reminder as completed"""
        try:
            if "reminders" not in self.user_knowledge:
                return "❌ No reminders found"

            reminders = self.user_knowledge["reminders"]
            if 0 <= task_index < len(reminders):
                reminders[task_index]["completed"] = True
                self._save_learning()
                return f"✅ Task completed: {reminders[task_index]['task']}"
            else:
                return "❌ Invalid task index"

        except Exception as e:
            return f"❌ Failed to complete task: {str(e)}"
