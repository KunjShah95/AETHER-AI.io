#!/usr/bin/env python3
"""
Task Management System for NEXUS AI Terminal
Provides comprehensive task management with priorities, categories, and AI assistance
"""

import os
import json
import time
import uuid
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from pathlib import Path
import re

class TaskManager:
    """Comprehensive task management system"""

    def __init__(self):
        self.tasks_db_path = os.path.expanduser("~/.nexus/tasks.db")
        self.tasks = {}
        self.categories = {}
        self.priorities = {
            "low": {"color": "green", "weight": 1},
            "medium": {"color": "yellow", "weight": 2},
            "high": {"color": "red", "weight": 3},
            "urgent": {"color": "magenta", "weight": 4}
        }
        self._load_tasks()
        self._initialize_categories()

    def _load_tasks(self):
        """Load tasks database"""
        try:
            if os.path.exists(self.tasks_db_path):
                with open(self.tasks_db_path, 'r') as f:
                    data = json.load(f)
                    self.tasks = data.get("tasks", {})
                    self.categories = data.get("categories", {})
        except Exception as e:
            print(f"Warning: Could not load tasks database: {e}")
            self.tasks = {}
            self.categories = {}

    def _save_tasks(self):
        """Save tasks database"""
        try:
            os.makedirs(os.path.dirname(self.tasks_db_path), exist_ok=True)
            data = {
                "tasks": self.tasks,
                "categories": self.categories,
                "last_updated": time.time()
            }
            with open(self.tasks_db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save tasks database: {e}")

    def _initialize_categories(self):
        """Initialize default categories"""
        default_categories = {
            "work": {"name": "Work", "color": "blue", "icon": "💼"},
            "personal": {"name": "Personal", "color": "green", "icon": "🏠"},
            "learning": {"name": "Learning", "color": "yellow", "icon": "📚"},
            "health": {"name": "Health", "color": "red", "icon": "🏥"},
            "projects": {"name": "Projects", "color": "purple", "icon": "🚀"},
            "shopping": {"name": "Shopping", "color": "cyan", "icon": "🛒"}
        }

        for cat_id, cat_data in default_categories.items():
            if cat_id not in self.categories:
                self.categories[cat_id] = cat_data

    def create_task(self, title: str, description: str = "", priority: str = "medium",
                   category: str = "personal", due_date: Optional[str] = None,
                   tags: List[str] = None) -> str:
        """Create a new task"""
        try:
            if priority not in self.priorities:
                return f"❌ Invalid priority. Choose from: {', '.join(self.priorities.keys())}"

            if category not in self.categories:
                return f"❌ Invalid category. Choose from: {', '.join(self.categories.keys())}"

            task_id = str(uuid.uuid4())[:8]

            task = {
                "id": task_id,
                "title": title,
                "description": description,
                "priority": priority,
                "category": category,
                "status": "pending",
                "created_at": time.time(),
                "updated_at": time.time(),
                "due_date": due_date,
                "tags": tags or [],
                "subtasks": [],
                "time_estimate": None,
                "time_spent": 0,
                "dependencies": [],
                "notes": []
            }

            self.tasks[task_id] = task
            self._save_tasks()

            return f"✅ Task created: {title} (ID: {task_id})"

        except Exception as e:
            return f"❌ Failed to create task: {str(e)}"

    def update_task(self, task_id: str, **updates) -> str:
        """Update an existing task"""
        try:
            if task_id not in self.tasks:
                return f"❌ Task not found: {task_id}"

            task = self.tasks[task_id]

            # Validate updates
            if "priority" in updates and updates["priority"] not in self.priorities:
                return f"❌ Invalid priority: {updates['priority']}"

            if "category" in updates and updates["category"] not in self.categories:
                return f"❌ Invalid category: {updates['category']}"

            # Apply updates
            for key, value in updates.items():
                if key in task:
                    task[key] = value

            task["updated_at"] = time.time()
            self._save_tasks()

            return f"✅ Task updated: {task['title']}"

        except Exception as e:
            return f"❌ Failed to update task: {str(e)}"

    def delete_task(self, task_id: str) -> str:
        """Delete a task"""
        try:
            if task_id not in self.tasks:
                return f"❌ Task not found: {task_id}"

            task_title = self.tasks[task_id]["title"]
            del self.tasks[task_id]
            self._save_tasks()

            return f"✅ Task deleted: {task_title}"

        except Exception as e:
            return f"❌ Failed to delete task: {str(e)}"

    def complete_task(self, task_id: str) -> str:
        """Mark a task as completed"""
        try:
            if task_id not in self.tasks:
                return f"❌ Task not found: {task_id}"

            task = self.tasks[task_id]
            task["status"] = "completed"
            task["completed_at"] = time.time()
            task["updated_at"] = time.time()

            self._save_tasks()

            return f"✅ Task completed: {task['title']}"

        except Exception as e:
            return f"❌ Failed to complete task: {str(e)}"

    def get_tasks(self, status: str = "all", category: str = None,
                 priority: str = None, limit: int = 50) -> List[Dict]:
        """Get tasks with optional filtering"""
        try:
            tasks = list(self.tasks.values())

            # Apply filters
            if status != "all":
                tasks = [t for t in tasks if t["status"] == status]

            if category:
                tasks = [t for t in tasks if t["category"] == category]

            if priority:
                tasks = [t for t in tasks if t["priority"] == priority]

            # Sort by priority (urgent first) then by creation date
            def sort_key(task):
                priority_weight = self.priorities[task["priority"]]["weight"]
                return (-priority_weight, task["created_at"])

            tasks.sort(key=sort_key)

            return tasks[:limit]

        except Exception as e:
            return [{"error": f"Failed to get tasks: {str(e)}"}]

    def get_task_by_id(self, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID"""
        return self.tasks.get(task_id)

    def add_subtask(self, task_id: str, title: str) -> str:
        """Add a subtask to an existing task"""
        try:
            if task_id not in self.tasks:
                return f"❌ Task not found: {task_id}"

            subtask = {
                "id": str(uuid.uuid4())[:8],
                "title": title,
                "completed": False,
                "created_at": time.time()
            }

            self.tasks[task_id]["subtasks"].append(subtask)
            self.tasks[task_id]["updated_at"] = time.time()
            self._save_tasks()

            return f"✅ Subtask added: {title}"

        except Exception as e:
            return f"❌ Failed to add subtask: {str(e)}"

    def complete_subtask(self, task_id: str, subtask_id: str) -> str:
        """Mark a subtask as completed"""
        try:
            if task_id not in self.tasks:
                return f"❌ Task not found: {task_id}"

            task = self.tasks[task_id]
            for subtask in task["subtasks"]:
                if subtask["id"] == subtask_id:
                    subtask["completed"] = True
                    subtask["completed_at"] = time.time()
                    task["updated_at"] = time.time()
                    self._save_tasks()
                    return f"✅ Subtask completed: {subtask['title']}"

            return f"❌ Subtask not found: {subtask_id}"

        except Exception as e:
            return f"❌ Failed to complete subtask: {str(e)}"

    def get_task_stats(self) -> Dict:
        """Get task statistics"""
        try:
            total_tasks = len(self.tasks)
            completed_tasks = len([t for t in self.tasks.values() if t["status"] == "completed"])
            pending_tasks = len([t for t in self.tasks.values() if t["status"] == "pending"])

            # Priority breakdown
            priority_stats = {}
            for priority in self.priorities.keys():
                priority_stats[priority] = len([t for t in self.tasks.values()
                                              if t["priority"] == priority])

            # Category breakdown
            category_stats = {}
            for category in self.categories.keys():
                category_stats[category] = len([t for t in self.tasks.values()
                                              if t["category"] == category])

            return {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
                "priority_breakdown": priority_stats,
                "category_breakdown": category_stats
            }

        except Exception as e:
            return {"error": f"Failed to get stats: {str(e)}"}

    def search_tasks(self, query: str) -> List[Dict]:
        """Search tasks by title, description, or tags"""
        try:
            query_lower = query.lower()
            matching_tasks = []

            for task in self.tasks.values():
                # Search in title, description, and tags
                searchable_text = f"{task['title']} {task['description']} {' '.join(task['tags'])}".lower()

                if query_lower in searchable_text:
                    matching_tasks.append(task)

            return matching_tasks

        except Exception as e:
            return [{"error": f"Search failed: {str(e)}"}]

    def get_overdue_tasks(self) -> List[Dict]:
        """Get tasks that are overdue"""
        try:
            current_time = time.time()
            overdue_tasks = []

            for task in self.tasks.values():
                if (task["status"] == "pending" and
                    task["due_date"] and
                    task["due_date"] < current_time):
                    overdue_tasks.append(task)

            return overdue_tasks

        except Exception as e:
            return [{"error": f"Failed to get overdue tasks: {str(e)}"}]

    def export_tasks(self, format_type: str = "json") -> str:
        """Export tasks in various formats"""
        try:
            if format_type == "json":
                return json.dumps(self.tasks, indent=2)
            elif format_type == "csv":
                # Simple CSV export
                lines = ["ID,Title,Description,Priority,Category,Status,Created,Due Date"]
                for task in self.tasks.values():
                    created = datetime.fromtimestamp(task["created_at"]).strftime("%Y-%m-%d")
                    due_date = task["due_date"] or ""
                    if due_date:
                        due_date = datetime.fromtimestamp(float(due_date)).strftime("%Y-%m-%d")

                    line = f"{task['id']},{task['title']},{task['description']},{task['priority']},{task['category']},{task['status']},{created},{due_date}"
                    lines.append(line)

                return "\n".join(lines)
            else:
                return "❌ Unsupported export format. Use 'json' or 'csv'"

        except Exception as e:
            return f"❌ Export failed: {str(e)}"
