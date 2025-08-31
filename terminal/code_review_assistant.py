"""
NEXUS AI Terminal - Code Review Assistant
Advanced code analysis, review, and improvement suggestions
"""

import os
import re
import json
import ast
import subprocess
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pathlib import Path
import hashlib
import tempfile

class CodeReviewAssistant:
    """Advanced code review and analysis assistant"""

    def __init__(self):
        self.supported_languages = {
            'python': ['.py', '.pyx', '.pyw'],
            'javascript': ['.js', '.jsx', '.ts', '.tsx'],
            'java': ['.java'],
            'cpp': ['.cpp', '.cc', '.cxx', '.c++', '.hpp', '.h'],
            'c': ['.c', '.h'],
            'csharp': ['.cs'],
            'php': ['.php'],
            'ruby': ['.rb'],
            'go': ['.go'],
            'rust': ['.rs'],
            'swift': ['.swift'],
            'kotlin': ['.kt'],
            'scala': ['.scala'],
            'html': ['.html', '.htm'],
            'css': ['.css', '.scss', '.sass'],
            'sql': ['.sql'],
            'yaml': ['.yaml', '.yml'],
            'json': ['.json'],
            'xml': ['.xml'],
            'markdown': ['.md', '.markdown']
        }

        self.quality_metrics = {
            'complexity': self._analyze_complexity,
            'maintainability': self._analyze_maintainability,
            'security': self._analyze_security,
            'performance': self._analyze_performance,
            'best_practices': self._analyze_best_practices
        }

        self.review_history = []
        self.load_review_history()

    def load_review_history(self):
        """Load review history from file"""
        try:
            if os.path.exists('code_reviews.json'):
                with open('code_reviews.json', 'r') as f:
                    self.review_history = json.load(f)
        except Exception:
            self.review_history = []

    def save_review_history(self):
        """Save review history to file"""
        try:
            with open('code_reviews.json', 'w') as f:
                json.dump(self.review_history[-100:], f, indent=2)  # Keep last 100 reviews
        except Exception:
            pass

    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension"""
        if not os.path.exists(file_path):
            return None

        _, ext = os.path.splitext(file_path.lower())
        for lang, extensions in self.supported_languages.items():
            if ext in extensions:
                return lang
        return None

    def analyze_file(self, file_path: str, analysis_type: str = "full") -> Dict:
        """Perform comprehensive code analysis"""
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}

        language = self.detect_language(file_path)
        if not language:
            return {"error": f"Unsupported file type: {file_path}"}

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            return {"error": f"Error reading file: {str(e)}"}

        analysis = {
            "file_path": file_path,
            "language": language,
            "timestamp": datetime.now().isoformat(),
            "file_size": len(code),
            "line_count": len(code.splitlines()),
            "analysis_type": analysis_type
        }

        # Perform different types of analysis
        if analysis_type in ["full", "quality"]:
            analysis["quality_metrics"] = self._run_quality_analysis(code, language)

        if analysis_type in ["full", "security"]:
            analysis["security_issues"] = self._run_security_analysis(code, language)

        if analysis_type in ["full", "performance"]:
            analysis["performance_suggestions"] = self._run_performance_analysis(code, language)

        if analysis_type in ["full", "best_practices"]:
            analysis["best_practices"] = self._run_best_practices_analysis(code, language)

        # Store in history
        self.review_history.append(analysis)
        self.save_review_history()

        return analysis

    def _run_quality_analysis(self, code: str, language: str) -> Dict:
        """Run quality analysis on code"""
        metrics = {}

        # Basic metrics
        lines = code.splitlines()
        metrics["total_lines"] = len(lines)
        metrics["code_lines"] = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        metrics["comment_lines"] = len([line for line in lines if line.strip().startswith('#')])
        metrics["empty_lines"] = len([line for line in lines if not line.strip()])

        # Language-specific analysis
        if language == "python":
            metrics.update(self._analyze_python_quality(code))
        elif language == "javascript":
            metrics.update(self._analyze_javascript_quality(code))

        # Calculate overall quality score
        metrics["quality_score"] = self._calculate_quality_score(metrics)

        return metrics

    def _analyze_python_quality(self, code: str) -> Dict:
        """Analyze Python code quality"""
        metrics = {}

        try:
            tree = ast.parse(code)

            # Count functions, classes, etc.
            functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = [node for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom))]

            metrics["function_count"] = len(functions)
            metrics["class_count"] = len(classes)
            metrics["import_count"] = len(imports)

            # Calculate average function length
            if functions:
                avg_func_length = sum(len(func.body) for func in functions) / len(functions)
                metrics["avg_function_length"] = round(avg_func_length, 2)

            # Check for docstrings
            documented_functions = sum(1 for func in functions if func.body and isinstance(func.body[0], ast.Expr) and isinstance(func.body[0].value, ast.Str))
            metrics["documented_functions"] = documented_functions
            metrics["documentation_coverage"] = round((documented_functions / len(functions)) * 100, 2) if functions else 0

        except SyntaxError:
            metrics["syntax_errors"] = True
        except Exception:
            metrics["parse_errors"] = True

        return metrics

    def _analyze_javascript_quality(self, code: str) -> Dict:
        """Analyze JavaScript code quality"""
        metrics = {}

        # Basic JavaScript analysis
        functions = len(re.findall(r'function\s+\w+\s*\(', code))
        arrow_functions = len(re.findall(r'=>\s*{', code))
        classes = len(re.findall(r'class\s+\w+', code))

        metrics["function_count"] = functions + arrow_functions
        metrics["class_count"] = classes
        metrics["arrow_functions"] = arrow_functions

        # Check for console.log statements (potential debugging code)
        console_logs = len(re.findall(r'console\.log', code))
        metrics["console_logs"] = console_logs

        return metrics

    def _calculate_quality_score(self, metrics: Dict) -> float:
        """Calculate overall quality score"""
        score = 100.0

        # Deduct points for various issues
        if metrics.get("syntax_errors"):
            score -= 50
        if metrics.get("parse_errors"):
            score -= 30

        # Documentation coverage
        doc_coverage = metrics.get("documentation_coverage", 0)
        if doc_coverage < 50:
            score -= (50 - doc_coverage) * 0.5

        # Function length
        avg_func_length = metrics.get("avg_function_length", 0)
        if avg_func_length > 30:
            score -= min(20, (avg_func_length - 30) * 0.5)

        # Console logs in JS
        console_logs = metrics.get("console_logs", 0)
        if console_logs > 5:
            score -= min(15, console_logs - 5)

        return max(0, round(score, 2))

    def _run_security_analysis(self, code: str, language: str) -> List[Dict]:
        """Run security analysis"""
        issues = []

        if language == "python":
            issues.extend(self._analyze_python_security(code))
        elif language == "javascript":
            issues.extend(self._analyze_javascript_security(code))
        elif language == "php":
            issues.extend(self._analyze_php_security(code))

        # Generic security checks
        issues.extend(self._analyze_generic_security(code))

        return issues

    def _analyze_python_security(self, code: str) -> List[Dict]:
        """Analyze Python code for security issues"""
        issues = []

        # Check for dangerous functions
        dangerous_patterns = [
            (r'eval\s*\(', "Use of eval() - potential code injection"),
            (r'exec\s*\(', "Use of exec() - potential code injection"),
            (r'input\s*\(', "Use of input() in Python 2 - potential security risk"),
            (r'os\.system\s*\(', "Use of os.system() - command injection risk"),
            (r'subprocess\.call\s*\(', "Use of subprocess.call() without shell=False"),
        ]

        for pattern, description in dangerous_patterns:
            if re.search(pattern, code):
                issues.append({
                    "severity": "high",
                    "type": "security",
                    "description": description,
                    "line": self._find_line_number(code, pattern)
                })

        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']*["\']',
            r'secret\s*=\s*["\'][^"\']*["\']',
            r'api_key\s*=\s*["\'][^"\']*["\']',
            r'token\s*=\s*["\'][^"\']*["\']'
        ]

        for pattern in secret_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    "severity": "medium",
                    "type": "security",
                    "description": "Potential hardcoded secret detected",
                    "line": self._find_line_number(code, pattern)
                })

        return issues

    def _analyze_javascript_security(self, code: str) -> List[Dict]:
        """Analyze JavaScript code for security issues"""
        issues = []

        dangerous_patterns = [
            (r'eval\s*\(', "Use of eval() - potential code injection"),
            (r'document\.write\s*\(', "Use of document.write() - XSS risk"),
            (r'innerHTML\s*=\s*', "Direct innerHTML assignment - XSS risk"),
            (r'localStorage\.setItem\s*\([^,]+,\s*[^)]+\)', "Potential sensitive data in localStorage"),
        ]

        for pattern, description in dangerous_patterns:
            if re.search(pattern, code):
                issues.append({
                    "severity": "high",
                    "type": "security",
                    "description": description,
                    "line": self._find_line_number(code, pattern)
                })

        return issues

    def _analyze_php_security(self, code: str) -> List[Dict]:
        """Analyze PHP code for security issues"""
        issues = []

        dangerous_patterns = [
            (r'\$_(GET|POST|REQUEST)\s*\[', "Direct use of superglobal - potential injection"),
            (r'mysql_query\s*\(', "Use of deprecated mysql_query()"),
            (r'eval\s*\(', "Use of eval() - code injection risk"),
            (r'include\s*\(', "Use of include() without validation"),
        ]

        for pattern, description in dangerous_patterns:
            if re.search(pattern, code):
                issues.append({
                    "severity": "high",
                    "type": "security",
                    "description": description,
                    "line": self._find_line_number(code, pattern)
                })

        return issues

    def _analyze_generic_security(self, code: str) -> List[Dict]:
        """Generic security analysis"""
        issues = []

        # Check for SQL injection patterns
        sql_patterns = [
            r'SELECT.*WHERE.*\+',
            r'INSERT.*VALUES.*\+',
            r'UPDATE.*SET.*\+',
            r'DELETE.*WHERE.*\+'
        ]

        for pattern in sql_patterns:
            if re.search(pattern, code, re.IGNORECASE):
                issues.append({
                    "severity": "high",
                    "type": "security",
                    "description": "Potential SQL injection vulnerability",
                    "line": self._find_line_number(code, pattern)
                })

        return issues

    def _run_performance_analysis(self, code: str, language: str) -> List[Dict]:
        """Run performance analysis"""
        suggestions = []

        if language == "python":
            suggestions.extend(self._analyze_python_performance(code))
        elif language == "javascript":
            suggestions.extend(self._analyze_javascript_performance(code))

        return suggestions

    def _analyze_python_performance(self, code: str) -> List[Dict]:
        """Analyze Python code for performance issues"""
        suggestions = []

        # Check for inefficient patterns
        patterns = [
            (r'for.*in.*range\(len\(.*\)\)', "Use enumerate() instead of range(len())"),
            (r'\.append\(.*\) inside loop', "Consider using list comprehension"),
            (r'\+=.*string.*loop', "Use join() for string concatenation in loops"),
            (r'import \*', "Avoid wildcard imports for better performance"),
        ]

        for pattern, suggestion in patterns:
            if re.search(pattern, code):
                suggestions.append({
                    "type": "performance",
                    "description": suggestion,
                    "line": self._find_line_number(code, pattern)
                })

        return suggestions

    def _analyze_javascript_performance(self, code: str) -> List[Dict]:
        """Analyze JavaScript code for performance issues"""
        suggestions = []

        patterns = [
            (r'for\s*\([^;]*;\s*[^;]*;\s*[^)]*\)', "Consider using forEach() or map()"),
            (r'document\.getElementById.*loop', "Cache DOM queries outside loops"),
            (r'console\.log.*production', "Remove console.log statements in production"),
        ]

        for pattern, suggestion in patterns:
            if re.search(pattern, code):
                suggestions.append({
                    "type": "performance",
                    "description": suggestion,
                    "line": self._find_line_number(code, pattern)
                })

        return suggestions

    def _run_best_practices_analysis(self, code: str, language: str) -> List[Dict]:
        """Run best practices analysis"""
        suggestions = []

        if language == "python":
            suggestions.extend(self._analyze_python_best_practices(code))
        elif language == "javascript":
            suggestions.extend(self._analyze_javascript_best_practices(code))

        return suggestions

    def _analyze_python_best_practices(self, code: str) -> List[Dict]:
        """Analyze Python code for best practices"""
        suggestions = []

        # Check for PEP 8 compliance and best practices
        issues = [
            (r'^\s{5,}', "Indentation should be 4 spaces"),
            (r'^\t', "Use spaces instead of tabs"),
            (r'class\s+[a-z]', "Class names should be CamelCase"),
            (r'^\s*def\s+[A-Z]', "Function names should be snake_case"),
            (r'^\s*import\s+os\s*,\s*sys', "Import one module per line"),
        ]

        for pattern, suggestion in issues:
            if re.search(pattern, code, re.MULTILINE):
                suggestions.append({
                    "type": "best_practice",
                    "description": suggestion,
                    "line": self._find_line_number(code, pattern)
                })

        return suggestions

    def _analyze_javascript_best_practices(self, code: str) -> List[Dict]:
        """Analyze JavaScript code for best practices"""
        suggestions = []

        issues = [
            (r'var\s+', "Use let/const instead of var"),
            (r'==\s*[^=]', "Use === instead of == for comparison"),
            (r'function\s+\w+\s*\([^)]*\)\s*{', "Consider using arrow functions"),
        ]

        for pattern, suggestion in issues:
            if re.search(pattern, code):
                suggestions.append({
                    "type": "best_practice",
                    "description": suggestion,
                    "line": self._find_line_number(code, pattern)
                })

        return suggestions

    def _find_line_number(self, code: str, pattern: str) -> Optional[int]:
        """Find line number of a pattern in code"""
        lines = code.splitlines()
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                return i
        return None

    def generate_review_report(self, analysis: Dict) -> str:
        """Generate a comprehensive review report"""
        if "error" in analysis:
            return f"❌ Review Error: {analysis['error']}"

        report = f"""
📋 CODE REVIEW REPORT
═══════════════════════════════════════════════

📁 File: {analysis['file_path']}
🗣️ Language: {analysis['language'].upper()}
📅 Reviewed: {analysis['timestamp']}
📏 Size: {analysis['file_size']} chars, {analysis['line_count']} lines

"""

        if "quality_metrics" in analysis:
            metrics = analysis["quality_metrics"]
            report += f"""
🔍 QUALITY METRICS
───────────────────────────────────────────────
• Quality Score: {metrics.get('quality_score', 'N/A')}/100
• Total Lines: {metrics.get('total_lines', 0)}
• Code Lines: {metrics.get('code_lines', 0)}
• Comment Lines: {metrics.get('comment_lines', 0)}
• Documentation Coverage: {metrics.get('documentation_coverage', 0)}%
"""

            if analysis['language'] == 'python':
                report += f"""• Functions: {metrics.get('function_count', 0)}
• Classes: {metrics.get('class_count', 0)}
• Average Function Length: {metrics.get('avg_function_length', 0)} lines
"""

        if "security_issues" in analysis and analysis["security_issues"]:
            report += f"""
🔒 SECURITY ISSUES
───────────────────────────────────────────────
"""
            for issue in analysis["security_issues"][:10]:  # Show first 10
                severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(issue["severity"], "⚪")
                report += f"{severity_icon} {issue['description']}\n"
                if issue.get("line"):
                    report += f"   📍 Line {issue['line']}\n"

        if "performance_suggestions" in analysis and analysis["performance_suggestions"]:
            report += f"""
⚡ PERFORMANCE SUGGESTIONS
───────────────────────────────────────────────
"""
            for suggestion in analysis["performance_suggestions"][:10]:
                report += f"💡 {suggestion['description']}\n"
                if suggestion.get("line"):
                    report += f"   📍 Line {suggestion['line']}\n"

        if "best_practices" in analysis and analysis["best_practices"]:
            report += f"""
✨ BEST PRACTICES
───────────────────────────────────────────────
"""
            for practice in analysis["best_practices"][:10]:
                report += f"📝 {practice['description']}\n"
                if practice.get("line"):
                    report += f"   📍 Line {practice['line']}\n"

        report += f"""
═══════════════════════════════════════════════
💡 Use /review suggest [file] for AI-powered improvement suggestions
"""

        return report

    def get_review_history(self, limit: int = 10) -> List[Dict]:
        """Get recent review history"""
        return self.review_history[-limit:]

    def get_review_stats(self) -> Dict:
        """Get review statistics"""
        if not self.review_history:
            return {"total_reviews": 0}

        stats = {
            "total_reviews": len(self.review_history),
            "languages_reviewed": set(),
            "avg_quality_score": 0,
            "security_issues_found": 0,
            "performance_suggestions": 0
        }

        quality_scores = []
        for review in self.review_history:
            if review.get("language"):
                stats["languages_reviewed"].add(review["language"])

            if "quality_metrics" in review and "quality_score" in review["quality_metrics"]:
                quality_scores.append(review["quality_metrics"]["quality_score"])

            if "security_issues" in review:
                stats["security_issues_found"] += len(review["security_issues"])

            if "performance_suggestions" in review:
                stats["performance_suggestions"] += len(review["performance_suggestions"])

        if quality_scores:
            stats["avg_quality_score"] = round(sum(quality_scores) / len(quality_scores), 2)

        stats["languages_reviewed"] = list(stats["languages_reviewed"])

        return stats

    def compare_files(self, file1: str, file2: str) -> Dict:
        """Compare two files for differences"""
        if not os.path.exists(file1) or not os.path.exists(file2):
            return {"error": "One or both files not found"}

        try:
            with open(file1, 'r') as f1, open(file2, 'r') as f2:
                content1 = f1.read()
                content2 = f2.read()

            # Simple diff analysis
            lines1 = content1.splitlines()
            lines2 = content2.splitlines()

            comparison = {
                "file1": file1,
                "file2": file2,
                "file1_lines": len(lines1),
                "file2_lines": len(lines2),
                "line_difference": len(lines2) - len(lines1),
                "similarity_score": self._calculate_similarity(content1, content2)
            }

            return comparison

        except Exception as e:
            return {"error": f"Error comparing files: {str(e)}"}

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        # Simple Jaccard similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())

        intersection = words1.intersection(words2)
        union = words1.union(words2)

        if not union:
            return 0.0

        return round(len(intersection) / len(union) * 100, 2)
