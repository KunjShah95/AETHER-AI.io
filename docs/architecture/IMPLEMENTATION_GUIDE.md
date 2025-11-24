# Implementation Guide for Microservices Migration

This guide provides practical steps and code examples for implementing the microservices architecture outlined in the refactor plan.

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Development Environment Setup](#2-development-environment-setup)
3. [Phase 1: Infrastructure Setup](#3-phase-1-infrastructure-setup)
4. [Phase 2: First Service Extraction](#4-phase-2-first-service-extraction)
5. [Testing Strategy](#5-testing-strategy)
6. [Deployment Guide](#6-deployment-guide)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Prerequisites

### Required Software

- **Docker** 24.0+ and Docker Compose 2.20+
- **Kubernetes** 1.28+ (via minikube, kind, or cloud provider)
- **kubectl** 1.28+
- **Python** 3.11+
- **Node.js** 18+ (for any Node services)
- **Git** 2.40+

### Required Knowledge

- Python/FastAPI development
- Docker containerization
- Kubernetes basics
- REST API design
- Message queues (RabbitMQ)
- SQL and NoSQL databases

### Cloud Accounts (if deploying to cloud)

- AWS/GCP/Azure account with appropriate permissions
- Container registry access (ECR, GCR, Docker Hub)

---

## 2. Development Environment Setup

### 2.1 Repository Structure

Create a new repository structure to support microservices:

```
aether-ai-microservices/
├── services/
│   ├── ai-gateway/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── routes/
│   │   │   └── services/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── task-manager/
│   ├── code-assistant/
│   ├── analytics/
│   ├── integration-hub/
│   └── security/
├── infrastructure/
│   ├── docker-compose.yml
│   ├── kubernetes/
│   │   ├── namespaces/
│   │   ├── deployments/
│   │   ├── services/
│   │   └── ingress/
│   └── terraform/
├── shared/
│   ├── proto/  # gRPC definitions
│   ├── events/  # Event schemas
│   └── utils/   # Shared utilities
├── gateway/
│   ├── kong.yml
│   └── traefik.yml
└── monitoring/
    ├── prometheus/
    ├── grafana/
    └── jaeger/
```

### 2.2 Local Development Docker Compose

Create `infrastructure/docker-compose.dev.yml`:

```yaml
version: '3.8'

services:
  # Message Bus
  rabbitmq:
    image: rabbitmq:3.12-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq

  # Databases
  postgres:
    image: postgres:16-alpine
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: aether
      POSTGRES_PASSWORD: aether_dev
      POSTGRES_DB: aether
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mongodb:
    image: mongo:7-jammy
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: admin
    volumes:
      - mongo_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
    volumes:
      - grafana_data:/var/lib/grafana

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "6831:6831/udp"
      - "16686:16686"
    environment:
      COLLECTOR_OTLP_ENABLED: true

volumes:
  rabbitmq_data:
  postgres_data:
  mongo_data:
  redis_data:
  prometheus_data:
  grafana_data:
```

Start infrastructure:

```bash
cd infrastructure
docker-compose -f docker-compose.dev.yml up -d
```

---

## 3. Phase 1: Infrastructure Setup

### 3.1 Set Up API Gateway (Kong)

Install Kong using Helm:

```bash
helm repo add kong https://charts.konghq.com
helm repo update
helm install kong kong/kong \
  --namespace kong \
  --create-namespace \
  --set ingressController.installCRDs=false \
  --set proxy.type=LoadBalancer
```

Create Kong configuration `gateway/kong.yml`:

```yaml
_format_version: "3.0"

services:
  - name: task-manager
    url: http://task-manager.aether-ai.svc.cluster.local:80
    routes:
      - name: task-manager-route
        paths:
          - /api/v1/tasks
        methods:
          - GET
          - POST
          - PUT
          - DELETE
    plugins:
      - name: rate-limiting
        config:
          minute: 60
          policy: local
      - name: jwt
        config:
          key_claim_name: iss

  - name: ai-gateway
    url: http://ai-gateway.aether-ai.svc.cluster.local:80
    routes:
      - name: ai-gateway-route
        paths:
          - /api/v1/ai
    plugins:
      - name: rate-limiting
        config:
          minute: 30
          policy: local
```

### 3.2 Set Up Message Bus (RabbitMQ)

Create RabbitMQ configuration:

```python
# shared/messaging/rabbitmq.py
import pika
from typing import Callable
import json

class MessageBus:
    def __init__(self, host='localhost', port=5672, username='admin', password='admin'):
        self.credentials = pika.PlainCredentials(username, password)
        self.parameters = pika.ConnectionParameters(
            host=host,
            port=port,
            credentials=self.credentials
        )
        self.connection = None
        self.channel = None

    def connect(self):
        """Establish connection to RabbitMQ"""
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def publish(self, exchange: str, routing_key: str, message: dict):
        """Publish a message to an exchange"""
        if not self.channel:
            self.connect()
        
        self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Persistent
                content_type='application/json'
            )
        )

    def subscribe(self, queue: str, callback: Callable):
        """Subscribe to a queue"""
        if not self.channel:
            self.connect()
        
        self.channel.queue_declare(queue=queue, durable=True)
        
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_consume(
            queue=queue,
            on_message_callback=wrapper
        )
        
        self.channel.start_consuming()

    def close(self):
        """Close connection"""
        if self.connection:
            self.connection.close()
```

### 3.3 Set Up Monitoring

Create Prometheus configuration `monitoring/prometheus/prometheus.yml`:

```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'task-manager'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - aether-ai
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: task-manager
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

  - job_name: 'ai-gateway'
    kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
            - aether-ai
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        action: keep
        regex: ai-gateway
```

---

## 4. Phase 2: First Service Extraction

### 4.1 Extract Security Service

#### Step 1: Create Service Structure

```bash
mkdir -p services/security/app/{routes,services,models}
cd services/security
```

#### Step 2: Define Models

`app/models.py`:

```python
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class User(BaseModel):
    id: str
    email: EmailStr
    name: str
    roles: List[str]
    created_at: datetime

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    user: User

class TokenValidationRequest(BaseModel):
    token: str

class TokenValidationResponse(BaseModel):
    valid: bool
    user_id: Optional[str] = None
    roles: Optional[List[str]] = None
    expires_at: Optional[datetime] = None
```

#### Step 3: Implement Authentication Service

`app/services/auth_service.py`:

```python
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict
import os

class AuthService:
    def __init__(self):
        self.secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
        self.algorithm = 'HS256'
        self.access_token_expire_minutes = 60
        self.refresh_token_expire_days = 30

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against a hash"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    def create_access_token(self, data: Dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        
        to_encode.update({
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'access'
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_refresh_token(self, data: Dict) -> str:
        """Create a JWT refresh token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        
        to_encode.update({
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        })
        
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def validate_token(self, token: str) -> Optional[Dict]:
        """Validate and decode a JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def get_current_user(self, token: str) -> Optional[Dict]:
        """Get current user from token"""
        payload = self.validate_token(token)
        if payload is None:
            return None
        
        return {
            'user_id': payload.get('sub'),
            'email': payload.get('email'),
            'roles': payload.get('roles', [])
        }
```

#### Step 4: Create API Routes

`app/routes/auth.py`:

```python
from fastapi import APIRouter, HTTPException, Depends, Header
from app.models import LoginRequest, LoginResponse, TokenValidationRequest, TokenValidationResponse
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])
auth_service = AuthService()
user_service = UserService()

@router.post('/login', response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user and return JWT tokens"""
    # Verify user credentials
    user = await user_service.get_user_by_email(request.email)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    if not auth_service.verify_password(request.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    
    # Create tokens
    token_data = {
        'sub': user['id'],
        'email': user['email'],
        'roles': user['roles']
    }
    
    access_token = auth_service.create_access_token(token_data)
    refresh_token = auth_service.create_refresh_token(token_data)
    
    return LoginResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=3600,
        user={
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'roles': user['roles'],
            'created_at': user['created_at']
        }
    )

@router.post('/validate', response_model=TokenValidationResponse)
async def validate_token(request: TokenValidationRequest):
    """Validate a JWT token"""
    payload = auth_service.validate_token(request.token)
    
    if payload is None:
        return TokenValidationResponse(valid=False)
    
    return TokenValidationResponse(
        valid=True,
        user_id=payload.get('sub'),
        roles=payload.get('roles'),
        expires_at=payload.get('exp')
    )

@router.post('/refresh')
async def refresh_token(refresh_token: str):
    """Refresh access token using refresh token"""
    payload = auth_service.validate_token(refresh_token)
    
    if payload is None or payload.get('type') != 'refresh':
        raise HTTPException(status_code=401, detail='Invalid refresh token')
    
    # Create new access token
    token_data = {
        'sub': payload['sub'],
        'email': payload['email'],
        'roles': payload['roles']
    }
    
    access_token = auth_service.create_access_token(token_data)
    
    return {
        'access_token': access_token,
        'expires_in': 3600
    }

@router.get('/me')
async def get_current_user(authorization: str = Header(...)):
    """Get current authenticated user"""
    token = authorization.replace('Bearer ', '')
    user = auth_service.get_current_user(token)
    
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    return user
```

#### Step 5: Create Main Application

`app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from app.routes import auth

app = FastAPI(
    title='Security Service',
    description='Authentication and authorization service',
    version='1.0.0'
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Include routers
app.include_router(auth.router)

# Prometheus metrics
Instrumentator().instrument(app).expose(app)

@app.get('/health')
async def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'security'}

@app.get('/ready')
async def readiness_check():
    """Readiness check endpoint"""
    # Check database connection, etc.
    return {'status': 'ready'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
```

#### Step 6: Create Dockerfile

`Dockerfile`:

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY app/ ./app/

# Set PATH
ENV PATH=/root/.local/bin:$PATH

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Step 7: Create Requirements

`requirements.txt`:

```
fastapi==0.111.0
uvicorn[standard]==0.30.1
pydantic==2.7.4
pydantic-settings==2.3.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.9
prometheus-fastapi-instrumentator==7.0.0
asyncpg==0.29.0
pyjwt==2.8.0
bcrypt==4.1.3
```

#### Step 8: Create Kubernetes Deployment

`kubernetes/deployments/security-service.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: security-service
  namespace: aether-ai
  labels:
    app: security-service
    version: v1
spec:
  replicas: 2
  selector:
    matchLabels:
      app: security-service
  template:
    metadata:
      labels:
        app: security-service
        version: v1
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "8000"
        prometheus.io/path: "/metrics"
    spec:
      containers:
      - name: security-service
        image: aether-ai/security-service:1.0.0
        ports:
        - containerPort: 8000
          name: http
        env:
        - name: JWT_SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: security-secret
              key: jwt-secret-key
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: security-secret
              key: database-url
        resources:
          requests:
            cpu: 100m
            memory: 128Mi
          limits:
            cpu: 500m
            memory: 256Mi
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: security-service
  namespace: aether-ai
spec:
  selector:
    app: security-service
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
```

### 4.2 Build and Deploy

```bash
# Build Docker image
cd services/security
docker build -t aether-ai/security-service:1.0.0 .

# Push to registry
docker push aether-ai/security-service:1.0.0

# Deploy to Kubernetes
kubectl apply -f ../../kubernetes/deployments/security-service.yaml

# Verify deployment
kubectl get pods -n aether-ai
kubectl logs -f deployment/security-service -n aether-ai
```

---

## 5. Testing Strategy

### 5.1 Unit Tests

`tests/test_auth_service.py`:

```python
import pytest
from app.services.auth_service import AuthService

@pytest.fixture
def auth_service():
    return AuthService()

def test_hash_password(auth_service):
    password = "TestPassword123!"
    hashed = auth_service.hash_password(password)
    assert hashed != password
    assert auth_service.verify_password(password, hashed)

def test_create_access_token(auth_service):
    data = {'sub': 'user-123', 'email': 'test@example.com'}
    token = auth_service.create_access_token(data)
    assert token is not None
    
    payload = auth_service.validate_token(token)
    assert payload['sub'] == 'user-123'
    assert payload['email'] == 'test@example.com'

def test_invalid_token(auth_service):
    invalid_token = 'invalid.token.here'
    payload = auth_service.validate_token(invalid_token)
    assert payload is None
```

### 5.2 Integration Tests

`tests/test_api.py`:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'healthy'

def test_login_success():
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'TestPass123!'
    })
    assert response.status_code == 200
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data['token_type'] == 'Bearer'

def test_login_invalid_credentials():
    response = client.post('/api/v1/auth/login', json={
        'email': 'test@example.com',
        'password': 'WrongPassword'
    })
    assert response.status_code == 401
```

### 5.3 Contract Tests

Use Pact for contract testing between services.

---

## 6. Deployment Guide

### 6.1 Local Development

```bash
# Start infrastructure
docker-compose -f infrastructure/docker-compose.dev.yml up -d

# Run service locally
cd services/security
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 6.2 Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace aether-ai

# Create secrets
kubectl create secret generic security-secret \
  --from-literal=jwt-secret-key=your-secret-key \
  --from-literal=database-url=postgresql://... \
  -n aether-ai

# Deploy service
kubectl apply -f kubernetes/deployments/security-service.yaml

# Verify
kubectl get all -n aether-ai
```

### 6.3 Monitoring

Access monitoring dashboards:

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Jaeger**: http://localhost:16686

---

## 7. Troubleshooting

### Common Issues

**Issue: Service won't start**
```bash
# Check logs
kubectl logs -f deployment/security-service -n aether-ai

# Check events
kubectl describe pod <pod-name> -n aether-ai
```

**Issue: Database connection fails**
```bash
# Test connectivity
kubectl run -it --rm debug --image=postgres:16-alpine --restart=Never -- \
  psql -h postgres -U aether -d aether
```

**Issue: Services can't communicate**
```bash
# Check DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- \
  nslookup security-service.aether-ai.svc.cluster.local
```

---

**Last Updated:** 2025-11-24  
**Guide Version:** 1.0  
**Maintained by:** AETHER-AI Architecture Team
