# Service API Specifications

This document provides detailed API specifications for each microservice in the AETHER-AI system.

## Table of Contents

1. [AI Gateway Service](#1-ai-gateway-service)
2. [Code Assistant Service](#2-code-assistant-service)
3. [Task Manager Service](#3-task-manager-service)
4. [Analytics Service](#4-analytics-service)
5. [Integration Hub Service](#5-integration-hub-service)
6. [Security Service](#6-security-service)
7. [Common Patterns](#7-common-patterns)

---

## 1. AI Gateway Service

### Overview
The AI Gateway Service orchestrates requests to multiple AI model providers (Gemini, Groq, Ollama, HuggingFace, ChatGPT, MCP) and manages context, caching, and rate limiting.

### Base URL
`/api/v1/ai`

### Authentication
Bearer token (JWT) required in Authorization header

### Endpoints

#### POST /chat
Send a message to an AI model and receive a response.

**Request:**
```json
{
  "model": "gemini",
  "message": "Explain quantum computing in simple terms",
  "context": [
    {
      "role": "user",
      "content": "Previous message"
    },
    {
      "role": "assistant",
      "content": "Previous response"
    }
  ],
  "options": {
    "temperature": 0.7,
    "max_tokens": 1000,
    "stream": false
  }
}
```

**Response (200 OK):**
```json
{
  "response": "Quantum computing is a revolutionary approach...",
  "model": "gemini-pro",
  "tokens": {
    "input": 45,
    "output": 320,
    "total": 365
  },
  "latency_ms": 1250,
  "request_id": "req-abc123",
  "cached": false
}
```

**Error Responses:**
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Missing or invalid authentication
- `429 Too Many Requests`: Rate limit exceeded
- `503 Service Unavailable`: AI provider unavailable

#### GET /models
List all available AI models and their current status.

**Response (200 OK):**
```json
{
  "models": [
    {
      "id": "gemini-pro",
      "name": "Gemini Pro",
      "provider": "google",
      "status": "available",
      "capabilities": ["chat", "code", "reasoning"],
      "max_tokens": 32000,
      "rate_limit": {
        "requests_per_minute": 60,
        "tokens_per_minute": 100000
      }
    },
    {
      "id": "llama3:8b",
      "name": "Llama 3 (8B)",
      "provider": "ollama",
      "status": "available",
      "capabilities": ["chat", "code"],
      "max_tokens": 8192,
      "local": true
    }
  ]
}
```

#### POST /switch
Switch the active default model for the user.

**Request:**
```json
{
  "model": "groq"
}
```

**Response (200 OK):**
```json
{
  "current_model": "groq-llama3",
  "previous_model": "gemini-pro",
  "status": "success",
  "message": "Model switched successfully"
}
```

#### GET /usage
Get AI usage statistics for the authenticated user.

**Query Parameters:**
- `start_date` (optional): ISO 8601 date
- `end_date` (optional): ISO 8601 date
- `model` (optional): Filter by specific model

**Response (200 OK):**
```json
{
  "period": {
    "start": "2025-11-01T00:00:00Z",
    "end": "2025-11-24T23:59:59Z"
  },
  "total_requests": 1543,
  "total_tokens": 245670,
  "by_model": {
    "gemini-pro": {
      "requests": 890,
      "tokens": 145230
    },
    "groq-llama3": {
      "requests": 653,
      "tokens": 100440
    }
  },
  "cost_estimate_usd": 12.45
}
```

#### POST /embeddings
Generate vector embeddings for text (for RAG/semantic search).

**Request:**
```json
{
  "text": "The quick brown fox jumps over the lazy dog",
  "model": "sentence-transformers"
}
```

**Response (200 OK):**
```json
{
  "embedding": [0.123, -0.456, 0.789, ...],
  "dimensions": 384,
  "model": "all-MiniLM-L6-v2",
  "tokens": 10
}
```

### WebSocket Endpoint

#### WS /chat/stream
Stream AI responses in real-time.

**Connect:**
```
ws://api.example.com/api/v1/ai/chat/stream?token=<jwt_token>
```

**Send Message:**
```json
{
  "type": "message",
  "model": "gemini",
  "message": "Write a short story",
  "options": {
    "temperature": 0.8,
    "stream": true
  }
}
```

**Receive Chunks:**
```json
{
  "type": "chunk",
  "content": "Once upon a time",
  "request_id": "req-xyz789"
}
```

```json
{
  "type": "done",
  "tokens": {
    "input": 10,
    "output": 250
  },
  "latency_ms": 3200
}
```

---

## 2. Code Assistant Service

### Overview
Provides code review, refactoring, test generation, and test execution capabilities.

### Base URL
`/api/v1/code`

### Endpoints

#### POST /review
Analyze code and provide feedback on quality, security, and best practices.

**Request:**
```json
{
  "code": "def calculate_sum(a, b):\n    return a + b",
  "language": "python",
  "context": "This is a utility function in a math module"
}
```

**Response (200 OK):**
```json
{
  "issues": [
    {
      "severity": "low",
      "line": 1,
      "column": 0,
      "message": "Missing docstring",
      "rule": "PEP257",
      "suggestion": "Add a docstring explaining the function purpose"
    }
  ],
  "suggestions": [
    "Consider adding type hints for better code clarity",
    "Add input validation for non-numeric types"
  ],
  "score": 85,
  "security_issues": [],
  "complexity": {
    "cyclomatic": 1,
    "cognitive": 0
  }
}
```

#### POST /refactor
Refactor code based on an instruction.

**Request:**
```json
{
  "code": "def calc(x,y):\n  z=x+y\n  return z",
  "instruction": "Improve code style and add type hints",
  "language": "python"
}
```

**Response (200 OK):**
```json
{
  "refactored_code": "def calculate(x: int, y: int) -> int:\n    \"\"\"Calculate the sum of two integers.\"\"\"\n    result = x + y\n    return result",
  "changes": [
    "Renamed function from 'calc' to 'calculate' for clarity",
    "Added type hints for parameters and return value",
    "Added docstring",
    "Improved variable naming (z -> result)",
    "Fixed spacing according to PEP 8"
  ],
  "explanation": "The refactored code follows Python best practices..."
}
```

#### POST /test/generate
Generate unit tests for the provided code.

**Request:**
```json
{
  "code": "def divide(a: float, b: float) -> float:\n    return a / b",
  "language": "python",
  "framework": "pytest"
}
```

**Response (200 OK):**
```json
{
  "tests": "import pytest\n\ndef test_divide_positive_numbers():\n    assert divide(10, 2) == 5\n\ndef test_divide_negative_numbers():\n    assert divide(-10, 2) == -5\n\ndef test_divide_by_zero():\n    with pytest.raises(ZeroDivisionError):\n        divide(10, 0)",
  "test_count": 3,
  "coverage_estimate": 85,
  "framework": "pytest"
}
```

#### POST /test/run
Execute tests and return results.

**Request:**
```json
{
  "test_command": "pytest tests/",
  "working_dir": "/path/to/project",
  "environment": {
    "PYTHONPATH": "/path/to/project"
  }
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "output": "============================= test session starts ==============================\ncollected 15 items\n\ntests/test_utils.py ........                                             [ 53%]\ntests/test_models.py .......                                             [100%]\n\n============================== 15 passed in 0.82s ===============================",
  "duration_ms": 820,
  "summary": {
    "passed": 15,
    "failed": 0,
    "skipped": 0,
    "total": 15
  }
}
```

#### POST /analyze/complexity
Analyze code complexity metrics.

**Request:**
```json
{
  "code": "def complex_function(data):\n    result = []\n    for item in data:\n        if item > 0:\n            if item % 2 == 0:\n                result.append(item * 2)\n            else:\n                result.append(item)\n    return result",
  "language": "python"
}
```

**Response (200 OK):**
```json
{
  "cyclomatic_complexity": 4,
  "cognitive_complexity": 5,
  "maintainability_index": 68,
  "lines_of_code": 8,
  "complexity_level": "moderate",
  "recommendations": [
    "Consider breaking down nested conditions",
    "Use list comprehension for simpler logic"
  ]
}
```

---

## 3. Task Manager Service

### Overview
Manages tasks with CRUD operations, scheduling, priorities, and notifications.

### Base URL
`/api/v1/tasks`

### Endpoints

#### POST /
Create a new task.

**Request:**
```json
{
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API",
  "priority": "high",
  "category": "backend",
  "due_date": "2025-12-01T00:00:00Z",
  "tags": ["security", "api"],
  "assignee": "user-123",
  "estimated_hours": 8
}
```

**Response (201 Created):**
```json
{
  "id": "task-abc123",
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API",
  "priority": "high",
  "status": "pending",
  "category": "backend",
  "due_date": "2025-12-01T00:00:00Z",
  "tags": ["security", "api"],
  "assignee": "user-123",
  "estimated_hours": 8,
  "created_at": "2025-11-24T10:30:00Z",
  "created_by": "user-456",
  "updated_at": "2025-11-24T10:30:00Z"
}
```

#### GET /
List tasks with filtering and pagination.

**Query Parameters:**
- `status`: pending | in_progress | completed | blocked
- `priority`: low | medium | high | urgent
- `category`: string
- `assignee`: user_id
- `tags`: comma-separated list
- `due_before`: ISO 8601 date
- `page`: page number (default: 1)
- `limit`: items per page (default: 20, max: 100)
- `sort`: field to sort by (default: created_at)
- `order`: asc | desc (default: desc)

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "task-abc123",
      "title": "Implement user authentication",
      "priority": "high",
      "status": "in_progress",
      "due_date": "2025-12-01T00:00:00Z",
      "assignee": "user-123",
      "progress": 60
    }
  ],
  "pagination": {
    "total": 145,
    "page": 1,
    "limit": 20,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

#### GET /{id}
Get detailed information about a specific task.

**Response (200 OK):**
```json
{
  "id": "task-abc123",
  "title": "Implement user authentication",
  "description": "Add JWT-based authentication to the API",
  "priority": "high",
  "status": "in_progress",
  "category": "backend",
  "due_date": "2025-12-01T00:00:00Z",
  "tags": ["security", "api"],
  "assignee": "user-123",
  "estimated_hours": 8,
  "actual_hours": 5,
  "progress": 60,
  "created_at": "2025-11-24T10:30:00Z",
  "created_by": "user-456",
  "updated_at": "2025-11-24T15:45:00Z",
  "comments": [
    {
      "id": "comment-1",
      "user_id": "user-123",
      "text": "Started implementing JWT middleware",
      "created_at": "2025-11-24T11:00:00Z"
    }
  ],
  "history": [
    {
      "action": "status_changed",
      "from": "pending",
      "to": "in_progress",
      "user_id": "user-123",
      "timestamp": "2025-11-24T11:00:00Z"
    }
  ]
}
```

#### PUT /{id}
Update an existing task.

**Request:**
```json
{
  "status": "completed",
  "actual_hours": 7,
  "progress": 100
}
```

**Response (200 OK):**
```json
{
  "id": "task-abc123",
  "title": "Implement user authentication",
  "status": "completed",
  "progress": 100,
  "actual_hours": 7,
  "updated_at": "2025-11-24T18:30:00Z"
}
```

#### DELETE /{id}
Delete a task.

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Task deleted successfully",
  "id": "task-abc123"
}
```

#### POST /{id}/complete
Mark a task as complete.

**Response (200 OK):**
```json
{
  "id": "task-abc123",
  "status": "completed",
  "completed_at": "2025-11-24T18:30:00Z",
  "completed_by": "user-123",
  "actual_hours": 7
}
```

#### POST /{id}/comments
Add a comment to a task.

**Request:**
```json
{
  "text": "Completed JWT implementation and added tests"
}
```

**Response (201 Created):**
```json
{
  "id": "comment-2",
  "task_id": "task-abc123",
  "user_id": "user-123",
  "text": "Completed JWT implementation and added tests",
  "created_at": "2025-11-24T18:35:00Z"
}
```

#### GET /stats
Get task statistics.

**Query Parameters:**
- `user_id` (optional): Filter by user
- `start_date` (optional): Start of date range
- `end_date` (optional): End of date range

**Response (200 OK):**
```json
{
  "total": 145,
  "by_status": {
    "pending": 32,
    "in_progress": 45,
    "completed": 60,
    "blocked": 8
  },
  "by_priority": {
    "low": 25,
    "medium": 68,
    "high": 40,
    "urgent": 12
  },
  "completion_rate": 0.65,
  "average_completion_time_hours": 12.5,
  "overdue": 7
}
```

---

## 4. Analytics Service

### Overview
Collects and analyzes usage metrics, system health, and business intelligence.

### Base URL
`/api/v1/analytics`

### Endpoints

#### POST /events
Log an analytics event.

**Request:**
```json
{
  "event_type": "task_created",
  "user_id": "user-123",
  "metadata": {
    "task_id": "task-abc123",
    "priority": "high",
    "category": "backend"
  },
  "timestamp": "2025-11-24T10:30:00Z"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "event_id": "event-xyz789"
}
```

#### GET /usage
Get usage statistics.

**Query Parameters:**
- `start_date`: ISO 8601 date (required)
- `end_date`: ISO 8601 date (required)
- `granularity`: hour | day | week | month (default: day)
- `metric`: specific metric name (optional)

**Response (200 OK):**
```json
{
  "period": {
    "start": "2025-11-01T00:00:00Z",
    "end": "2025-11-24T23:59:59Z",
    "granularity": "day"
  },
  "metrics": [
    {
      "date": "2025-11-24",
      "task_created": 45,
      "task_completed": 38,
      "ai_requests": 234,
      "code_reviews": 12,
      "active_users": 67
    }
  ]
}
```

#### GET /errors
Get error analytics.

**Query Parameters:**
- `start_date`: ISO 8601 date
- `end_date`: ISO 8601 date
- `severity`: error | warning | critical
- `service`: filter by service name

**Response (200 OK):**
```json
{
  "summary": {
    "total_errors": 127,
    "by_severity": {
      "critical": 3,
      "error": 45,
      "warning": 79
    },
    "by_service": {
      "ai-gateway": 23,
      "task-manager": 12,
      "code-assistant": 8
    }
  },
  "errors": [
    {
      "id": "error-1",
      "timestamp": "2025-11-24T15:30:00Z",
      "severity": "error",
      "service": "ai-gateway",
      "message": "Rate limit exceeded for provider",
      "count": 15,
      "first_seen": "2025-11-24T15:30:00Z",
      "last_seen": "2025-11-24T15:45:00Z"
    }
  ]
}
```

#### GET /health
Get system health metrics.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "timestamp": "2025-11-24T16:00:00Z",
  "metrics": {
    "cpu": 45.2,
    "memory": 68.5,
    "disk": 42.1
  },
  "services": [
    {
      "name": "ai-gateway",
      "status": "healthy",
      "latency_ms": 125,
      "uptime_seconds": 345600,
      "last_check": "2025-11-24T16:00:00Z"
    },
    {
      "name": "task-manager",
      "status": "healthy",
      "latency_ms": 45,
      "uptime_seconds": 345600,
      "last_check": "2025-11-24T16:00:00Z"
    }
  ]
}
```

#### GET /dashboard
Get dashboard summary data.

**Response (200 OK):**
```json
{
  "timestamp": "2025-11-24T16:00:00Z",
  "summary": {
    "active_users_today": 67,
    "tasks_created_today": 45,
    "tasks_completed_today": 38,
    "ai_requests_today": 234,
    "system_health": "healthy"
  },
  "trends": {
    "tasks_trend": 12.5,
    "users_trend": -5.2,
    "ai_usage_trend": 23.8
  },
  "top_users": [
    {
      "user_id": "user-123",
      "tasks_completed": 15,
      "ai_requests": 45
    }
  ]
}
```

---

## 5. Integration Hub Service

### Overview
Manages integrations with external services (GitHub, Slack, Discord, etc.).

### Base URL
`/api/v1/integrations`

### Endpoints

#### GET /
List all configured integrations.

**Response (200 OK):**
```json
{
  "integrations": [
    {
      "id": "int-github-1",
      "name": "GitHub - Main Repo",
      "type": "github",
      "status": "connected",
      "created_at": "2025-11-01T10:00:00Z",
      "last_sync": "2025-11-24T15:30:00Z"
    },
    {
      "id": "int-slack-1",
      "name": "Slack - Engineering Channel",
      "type": "slack",
      "status": "connected",
      "created_at": "2025-11-02T14:00:00Z"
    }
  ]
}
```

#### POST /connect
Connect a new integration.

**Request (GitHub):**
```json
{
  "service": "github",
  "credentials": {
    "token": "ghp_xxxxxxxxxxxx"
  },
  "config": {
    "owner": "KunjShah95",
    "repo": "AETHER-AI"
  }
}
```

**Response (201 Created):**
```json
{
  "integration_id": "int-github-1",
  "status": "connected",
  "message": "GitHub integration created successfully"
}
```

#### POST /{integration_id}/webhook
Handle incoming webhook from external service.

**Request (GitHub webhook):**
```json
{
  "action": "opened",
  "pull_request": {
    "id": 123,
    "title": "Fix authentication bug",
    "user": {
      "login": "developer1"
    }
  }
}
```

**Response (200 OK):**
```json
{
  "received": true,
  "processed": true,
  "actions_taken": [
    "Created task from PR",
    "Notified team via Slack"
  ]
}
```

#### POST /github/repos
List GitHub repositories for an integration.

**Request:**
```json
{
  "integration_id": "int-github-1"
}
```

**Response (200 OK):**
```json
{
  "repos": [
    {
      "id": 12345,
      "name": "AETHER-AI",
      "full_name": "KunjShah95/AETHER-AI",
      "private": false,
      "stars": 156,
      "forks": 23
    }
  ]
}
```

#### POST /slack/message
Send a message to Slack.

**Request:**
```json
{
  "integration_id": "int-slack-1",
  "channel": "#engineering",
  "message": "Deploy completed successfully! 🚀"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message_id": "msg-xyz789",
  "channel": "#engineering",
  "timestamp": "2025-11-24T16:30:00Z"
}
```

---

## 6. Security Service

### Overview
Handles authentication, authorization, and security validation.

### Base URL
`/api/v1/auth`

### Endpoints

#### POST /login
Authenticate user and receive JWT token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "name": "John Doe",
    "roles": ["user", "developer"]
  }
}
```

#### POST /refresh
Refresh access token using refresh token.

**Request:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 3600
}
```

#### POST /validate
Validate JWT token.

**Request:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "valid": true,
  "user_id": "user-123",
  "roles": ["user", "developer"],
  "expires_at": "2025-11-24T17:30:00Z"
}
```

#### POST /register
Register a new user.

**Request:**
```json
{
  "email": "newuser@example.com",
  "password": "SecurePass123!",
  "name": "Jane Smith"
}
```

**Response (201 Created):**
```json
{
  "user_id": "user-789",
  "email": "newuser@example.com",
  "message": "User registered successfully"
}
```

---

## 7. Common Patterns

### Error Response Format

All services follow a consistent error response format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "details": [
      {
        "field": "priority",
        "message": "Must be one of: low, medium, high, urgent"
      }
    ],
    "request_id": "req-abc123",
    "timestamp": "2025-11-24T16:00:00Z"
  }
}
```

### Pagination

All list endpoints support pagination:

**Query Parameters:**
- `page`: Page number (default: 1)
- `limit`: Items per page (default: 20, max: 100)

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "total": 145,
    "page": 1,
    "limit": 20,
    "total_pages": 8,
    "has_next": true,
    "has_prev": false
  }
}
```

### Rate Limiting

All API endpoints are rate-limited. Rate limit information is returned in response headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 998
X-RateLimit-Reset: 1700838000
```

When rate limit is exceeded:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "retry_after": 60
  }
}
```

### Authentication

All endpoints (except `/auth/login` and `/auth/register`) require authentication:

**Header:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### API Versioning

All APIs are versioned using URL path versioning: `/api/v1/...`

When a breaking change is needed, a new version will be released: `/api/v2/...`

### CORS

All services support CORS with the following configuration:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

---

**Last Updated:** 2025-11-24  
**API Version:** 1.0  
**Maintained by:** AETHER-AI Architecture Team
