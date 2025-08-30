#!/usr/bin/env python3
"""
Games & Learning Module for NEXUS AI Terminal
Provides interactive coding challenges, tutorials, quizzes, and gamification
"""

import os
import json
import random
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class GamesLearning:
    """Manages games, challenges, tutorials, and learning features"""

    def __init__(self):
        self.games_db_path = os.path.expanduser("~/.nexus/games.db")
        self.user_progress = {}
        self.challenges = {}
        self.tutorials = {}
        self.quizzes = {}
        self.achievements = {}
        self._load_games_data()
        self._initialize_content()

    def _load_games_data(self):
        """Load games and learning data"""
        try:
            if os.path.exists(self.games_db_path):
                with open(self.games_db_path, 'r') as f:
                    data = json.load(f)
                    self.user_progress = data.get("progress", {})
                    self.achievements = data.get("achievements", {})
        except Exception as e:
            print(f"Warning: Could not load games database: {e}")

    def _save_games_data(self):
        """Save games and learning data"""
        try:
            os.makedirs(os.path.dirname(self.games_db_path), exist_ok=True)
            data = {
                "progress": self.user_progress,
                "achievements": self.achievements,
                "last_updated": time.time()
            }
            with open(self.games_db_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save games database: {e}")

    def _initialize_content(self):
        """Initialize challenges, tutorials, and quizzes"""
        self.challenges = {
            "python_basics": {
                "title": "Python Basics Challenge",
                "difficulty": "easy",
                "description": "Solve basic Python programming problems",
                "problems": [
                    {
                        "id": "pb1",
                        "question": "Write a function that returns the sum of two numbers",
                        "starter_code": "def add_numbers(a, b):\n    # Your code here\n    pass",
                        "test_cases": [(2, 3, 5), (10, 15, 25), (-5, 10, 5)],
                        "hints": ["Use the + operator", "Return the result"]
                    },
                    {
                        "id": "pb2",
                        "question": "Write a function that checks if a number is even",
                        "starter_code": "def is_even(n):\n    # Your code here\n    pass",
                        "test_cases": [(2, True), (3, False), (10, True), (15, False)],
                        "hints": ["Use modulo operator %", "Check if n % 2 == 0"]
                    }
                ]
            },
            "algorithm_puzzles": {
                "title": "Algorithm Puzzles",
                "difficulty": "medium",
                "description": "Solve algorithmic challenges",
                "problems": [
                    {
                        "id": "ap1",
                        "question": "Write a function to reverse a string",
                        "starter_code": "def reverse_string(s):\n    # Your code here\n    pass",
                        "test_cases": [("hello", "olleh"), ("world", "dlrow"), ("", "")],
                        "hints": ["Use string slicing", "s[::-1] reverses a string"]
                    }
                ]
            },
            "web_development": {
                "title": "Web Development Challenge",
                "difficulty": "medium",
                "description": "Build simple web applications",
                "problems": [
                    {
                        "id": "wd1",
                        "question": "Create an HTML page with a heading and paragraph",
                        "starter_code": "<!DOCTYPE html>\n<html>\n<head>\n    <title>My Page</title>\n</head>\n<body>\n    <!-- Your code here -->\n</body>\n</html>",
                        "test_cases": [],  # Manual review
                        "hints": ["Use <h1> for heading", "Use <p> for paragraph"]
                    }
                ]
            }
        }

        self.tutorials = {
            "python_intro": {
                "title": "Python Programming Introduction",
                "description": "Learn the basics of Python programming",
                "sections": [
                    {
                        "title": "Variables and Data Types",
                        "content": "Python variables can store different types of data...",
                        "examples": ["x = 5", "name = 'Alice'", "is_active = True"],
                        "quiz": [
                            {"question": "What is the data type of x = 5?", "options": ["int", "str", "bool"], "answer": "int"}
                        ]
                    },
                    {
                        "title": "Control Structures",
                        "content": "Control structures allow you to control the flow of your program...",
                        "examples": ["if x > 0:", "for i in range(5):", "while condition:"],
                        "quiz": [
                            {"question": "Which keyword is used for conditional execution?", "options": ["for", "if", "while"], "answer": "if"}
                        ]
                    }
                ]
            },
            "git_basics": {
                "title": "Git Version Control",
                "description": "Learn the fundamentals of Git",
                "sections": [
                    {
                        "title": "Basic Commands",
                        "content": "Git is a distributed version control system...",
                        "examples": ["git init", "git add .", "git commit -m 'message'"],
                        "quiz": [
                            {"question": "Which command stages all changes?", "options": ["git init", "git add .", "git commit"], "answer": "git add ."}
                        ]
                    }
                ]
            }
        }

        self.quizzes = {
            "python_fundamentals": {
                "title": "Python Fundamentals Quiz",
                "questions": [
                    {
                        "question": "What is the output of print(2 + 3)?",
                        "options": ["23", "5", "Error"],
                        "answer": "5",
                        "explanation": "The + operator performs addition on numbers"
                    },
                    {
                        "question": "Which of these is a valid Python variable name?",
                        "options": ["2variable", "variable_2", "variable-name"],
                        "answer": "variable_2",
                        "explanation": "Variable names cannot start with numbers or contain hyphens"
                    }
                ]
            }
        }

    def get_coding_challenge(self, difficulty: str = "easy", topic: str = None) -> Dict:
        """Get a coding challenge"""
        try:
            available_challenges = []

            for challenge_id, challenge in self.challenges.items():
                if challenge["difficulty"] == difficulty:
                    if topic is None or topic.lower() in challenge_id:
                        available_challenges.append((challenge_id, challenge))

            if not available_challenges:
                return {"error": f"No {difficulty} challenges found"}

            challenge_id, challenge = random.choice(available_challenges)
            problem = random.choice(challenge["problems"])

            return {
                "challenge_id": challenge_id,
                "title": challenge["title"],
                "difficulty": challenge["difficulty"],
                "problem": problem,
                "time_limit": 30  # minutes
            }

        except Exception as e:
            return {"error": f"Failed to get challenge: {str(e)}"}

    def submit_challenge_solution(self, challenge_id: str, problem_id: str, solution: str, user: str = "anonymous") -> Dict:
        """Submit and evaluate a challenge solution"""
        try:
            if challenge_id not in self.challenges:
                return {"error": "Invalid challenge ID"}

            challenge = self.challenges[challenge_id]
            problem = None

            for p in challenge["problems"]:
                if p["id"] == problem_id:
                    problem = p
                    break

            if not problem:
                return {"error": "Invalid problem ID"}

            # Basic evaluation (in a real implementation, this would be more sophisticated)
            test_results = []
            passed = 0

            for test_case in problem["test_cases"]:
                try:
                    # This is a simplified evaluation - real implementation would sandbox the code
                    if len(test_case) == 3:  # Function with two inputs and expected output
                        # For now, just check if the solution contains basic patterns
                        if "def" in solution and "return" in solution:
                            test_results.append({"passed": True, "input": test_case[:2], "expected": test_case[2], "actual": "simulated"})
                            passed += 1
                        else:
                            test_results.append({"passed": False, "input": test_case[:2], "expected": test_case[2], "actual": "incorrect"})
                except Exception as e:
                    test_results.append({"passed": False, "error": str(e)})

            # Calculate score
            score = (passed / len(problem["test_cases"])) * 100 if problem["test_cases"] else 0

            # Update user progress
            if user not in self.user_progress:
                self.user_progress[user] = {"challenges_completed": 0, "total_score": 0, "achievements": []}

            self.user_progress[user]["challenges_completed"] += 1
            self.user_progress[user]["total_score"] += score

            # Check for achievements
            achievements_earned = self._check_achievements(user)

            self._save_games_data()

            return {
                "score": score,
                "passed": passed,
                "total_tests": len(problem["test_cases"]),
                "test_results": test_results,
                "achievements": achievements_earned
            }

        except Exception as e:
            return {"error": f"Failed to evaluate solution: {str(e)}"}

    def _check_achievements(self, user: str) -> List[str]:
        """Check and award achievements"""
        achievements_earned = []
        progress = self.user_progress[user]

        # First Challenge
        if progress["challenges_completed"] == 1 and "first_challenge" not in self.achievements.get(user, []):
            achievements_earned.append("First Challenge Completed! 🏆")
            if user not in self.achievements:
                self.achievements[user] = []
            self.achievements[user].append("first_challenge")

        # Perfect Score
        if progress.get("perfect_scores", 0) >= 1 and "perfect_solver" not in self.achievements.get(user, []):
            achievements_earned.append("Perfect Solver! 🎯")
            self.achievements[user].append("perfect_solver")

        # Speed Demon (solve within 5 minutes)
        if progress.get("fast_solutions", 0) >= 1 and "speed_demon" not in self.achievements.get(user, []):
            achievements_earned.append("Speed Demon! ⚡")
            self.achievements[user].append("speed_demon")

        return achievements_earned

    def start_tutorial(self, tutorial_id: str) -> Dict:
        """Start an interactive tutorial"""
        try:
            if tutorial_id not in self.tutorials:
                return {"error": "Tutorial not found"}

            tutorial = self.tutorials[tutorial_id]
            return {
                "tutorial_id": tutorial_id,
                "title": tutorial["title"],
                "description": tutorial["description"],
                "total_sections": len(tutorial["sections"]),
                "current_section": 0,
                "progress": 0
            }

        except Exception as e:
            return {"error": f"Failed to start tutorial: {str(e)}"}

    def get_tutorial_section(self, tutorial_id: str, section_index: int) -> Dict:
        """Get a specific tutorial section"""
        try:
            if tutorial_id not in self.tutorials:
                return {"error": "Tutorial not found"}

            tutorial = self.tutorials[tutorial_id]
            if section_index >= len(tutorial["sections"]):
                return {"error": "Section not found"}

            section = tutorial["sections"][section_index]
            return {
                "section_index": section_index,
                "title": section["title"],
                "content": section["content"],
                "examples": section["examples"],
                "has_quiz": "quiz" in section
            }

        except Exception as e:
            return {"error": f"Failed to get tutorial section: {str(e)}"}

    def take_quiz(self, quiz_id: str, user: str = "anonymous") -> Dict:
        """Start or continue a quiz"""
        try:
            if quiz_id not in self.quizzes:
                return {"error": "Quiz not found"}

            quiz = self.quizzes[quiz_id]

            # Initialize quiz progress for user
            quiz_key = f"{user}:{quiz_id}"
            if quiz_key not in self.user_progress:
                self.user_progress[quiz_key] = {
                    "current_question": 0,
                    "score": 0,
                    "answers": [],
                    "completed": False
                }

            progress = self.user_progress[quiz_key]

            if progress["completed"]:
                return {"error": "Quiz already completed"}

            if progress["current_question"] >= len(quiz["questions"]):
                # Quiz completed
                progress["completed"] = True
                final_score = (progress["score"] / len(quiz["questions"])) * 100
                self._save_games_data()

                return {
                    "completed": True,
                    "final_score": final_score,
                    "total_questions": len(quiz["questions"]),
                    "correct_answers": progress["score"]
                }

            # Return current question
            question = quiz["questions"][progress["current_question"]]
            return {
                "question_number": progress["current_question"] + 1,
                "total_questions": len(quiz["questions"]),
                "question": question["question"],
                "options": question["options"],
                "progress": f"{progress['current_question'] + 1}/{len(quiz['questions'])}"
            }

        except Exception as e:
            return {"error": f"Failed to take quiz: {str(e)}"}

    def submit_quiz_answer(self, quiz_id: str, answer: str, user: str = "anonymous") -> Dict:
        """Submit an answer for the current quiz question"""
        try:
            if quiz_id not in self.quizzes:
                return {"error": "Quiz not found"}

            quiz = self.quizzes[quiz_id]
            quiz_key = f"{user}:{quiz_id}"

            if quiz_key not in self.user_progress:
                return {"error": "Quiz not started"}

            progress = self.user_progress[quiz_key]

            if progress["current_question"] >= len(quiz["questions"]):
                return {"error": "Quiz already completed"}

            question = quiz["questions"][progress["current_question"]]
            correct_answer = question["answer"]

            is_correct = answer.lower() == correct_answer.lower()
            if is_correct:
                progress["score"] += 1

            # Record answer
            progress["answers"].append({
                "question": progress["current_question"],
                "user_answer": answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })

            progress["current_question"] += 1
            self._save_games_data()

            return {
                "correct": is_correct,
                "explanation": question.get("explanation", ""),
                "current_score": progress["score"],
                "next_question": progress["current_question"] + 1 if progress["current_question"] < len(quiz["questions"]) else None
            }

        except Exception as e:
            return {"error": f"Failed to submit answer: {str(e)}"}

    def get_user_stats(self, user: str = "anonymous") -> Dict:
        """Get user statistics and achievements"""
        try:
            progress = self.user_progress.get(user, {
                "challenges_completed": 0,
                "total_score": 0,
                "achievements": []
            })

            achievements = self.achievements.get(user, [])

            return {
                "challenges_completed": progress["challenges_completed"],
                "total_score": progress["total_score"],
                "average_score": progress["total_score"] / max(progress["challenges_completed"], 1),
                "achievements": achievements,
                "achievement_count": len(achievements)
            }

        except Exception as e:
            return {"error": f"Failed to get user stats: {str(e)}"}

    def get_random_tip(self) -> str:
        """Get a random productivity tip"""
        tips = [
            "💡 Use version control for all your projects",
            "💡 Write tests for your code to ensure reliability",
            "💡 Use meaningful variable names in your code",
            "💡 Comment your code to explain complex logic",
            "💡 Break large functions into smaller, focused ones",
            "💡 Use keyboard shortcuts to speed up your workflow",
            "💡 Take regular breaks to maintain productivity",
            "💡 Learn one new programming concept each week",
            "💡 Review and refactor code regularly",
            "💡 Use debugging tools to troubleshoot issues efficiently"
        ]
        return random.choice(tips)