# Architecture Documentation

This directory contains comprehensive documentation for the AETHER-AI backend microservices architecture refactor.

## Overview

The AETHER-AI backend is being refactored from a monolithic Python application to a microservices architecture to improve scalability, maintainability, and deployment flexibility.

## Documents

### 1. [Microservices Refactor Plan](./MICROSERVICES_REFACTOR_PLAN.md)
**Main planning document** - Comprehensive roadmap for the architecture refactor including:
- Current architecture analysis
- Identified service domains
- Proposed microservices architecture with diagrams
- API boundaries and contracts
- Communication protocols (REST, gRPC, Message Bus)
- Data management strategy
- Security and authentication
- **10-month incremental migration roadmap** (Phase 1-5)
- Deployment strategy (Docker, Kubernetes)
- Monitoring and observability
- Risk analysis and mitigation

**Start here** for understanding the overall vision and plan.

### 2. [API Specifications](./API_SPECIFICATIONS.md)
**Detailed API documentation** for each microservice:
- AI Gateway Service API
- Code Assistant Service API
- Task Manager Service API
- Analytics Service API
- Integration Hub Service API
- Security Service API
- Common patterns (error handling, pagination, rate limiting)
- Event schemas for async communication

Use this document when implementing or integrating with service APIs.

### 3. [Implementation Guide](./IMPLEMENTATION_GUIDE.md)
**Hands-on guide** for developers implementing the microservices:
- Prerequisites and required software
- Development environment setup
- Infrastructure setup (Docker Compose, Kubernetes, RabbitMQ, Monitoring)
- Step-by-step first service extraction (Security Service)
- Complete code examples (models, services, routes, Dockerfile)
- Testing strategy (unit, integration, contract tests)
- Deployment procedures
- Troubleshooting common issues

Use this document when actively building and deploying services.

## Quick Start

### For Architects and Stakeholders
1. Read the [Microservices Refactor Plan](./MICROSERVICES_REFACTOR_PLAN.md)
2. Review the proposed architecture diagrams
3. Evaluate the migration roadmap and timeline
4. Assess risks and resource requirements

### For Backend Developers
1. Skim the [Microservices Refactor Plan](./MICROSERVICES_REFACTOR_PLAN.md) for context
2. Study the [API Specifications](./API_SPECIFICATIONS.md) for the service you're working on
3. Follow the [Implementation Guide](./IMPLEMENTATION_GUIDE.md) for practical steps
4. Reference the API specs while coding

### For DevOps Engineers
1. Review deployment strategy in [Microservices Refactor Plan](./MICROSERVICES_REFACTOR_PLAN.md) (Section 9)
2. Review monitoring setup in [Microservices Refactor Plan](./MICROSERVICES_REFACTOR_PLAN.md) (Section 10)
3. Follow infrastructure setup in [Implementation Guide](./IMPLEMENTATION_GUIDE.md) (Sections 2-3)
4. Set up CI/CD pipelines based on the deployment guide

### For QA Engineers
1. Review testing strategy in [Implementation Guide](./IMPLEMENTATION_GUIDE.md) (Section 5)
2. Reference [API Specifications](./API_SPECIFICATIONS.md) for endpoint testing
3. Set up integration test environments
4. Implement contract tests between services

## Migration Status

| Phase | Status | Timeline | Completion |
|-------|--------|----------|------------|
| **Planning** | ✅ Complete | Nov 2025 | 100% |
| **Phase 1: Foundation** | ⏳ Pending | Months 1-2 | 0% |
| **Phase 2: Core Services** | ⏳ Pending | Months 3-4 | 0% |
| **Phase 3: AI & Code Services** | ⏳ Pending | Months 5-6 | 0% |
| **Phase 4: Integration & Support** | ⏳ Pending | Months 7-8 | 0% |
| **Phase 5: Cleanup & Optimization** | ⏳ Pending | Months 9-10 | 0% |

Legend: ✅ Complete | 🔄 In Progress | ⏳ Pending | ⚠️ Blocked

## Key Decisions

### Architecture Patterns
- **Pattern**: Microservices with API Gateway
- **Rationale**: Better scalability, independent deployment, technology flexibility

### Communication
- **Synchronous**: REST (client-facing), gRPC (inter-service)
- **Asynchronous**: RabbitMQ (initially), migrate to Kafka as needed
- **Rationale**: REST for simplicity, gRPC for performance, RabbitMQ for ease of use

### Data Strategy
- **Pattern**: Database per service (polyglot persistence)
- **Consistency**: Saga pattern for distributed transactions
- **Rationale**: Loose coupling, technology fit per service

### Deployment
- **Development**: Docker Compose
- **Production**: Kubernetes (managed: EKS/GKE/AKS)
- **Rationale**: Industry standard, auto-scaling, self-healing

### Migration Strategy
- **Pattern**: Strangler Fig (incremental extraction)
- **Rationale**: Minimize risk, maintain functionality, gradual rollout

## Service Architecture

```
┌─────────────┐
│ API Gateway │ ◄── All client traffic
└──────┬──────┘
       │
       ├─► AI Gateway (Gemini, Groq, Ollama, etc.)
       ├─► Code Assistant (Review, Refactor, Test)
       ├─► Task Manager (CRUD, Scheduling)
       ├─► Analytics (Metrics, Monitoring)
       ├─► Integration Hub (GitHub, Slack, Discord)
       ├─► Security (Auth, AuthZ)
       ├─► Docker Manager
       └─► RAG Service (Semantic Search)
       
       │
       ▼
┌──────────────┐
│ Message Bus  │ ◄── Event-driven communication
└──────────────┘
       │
       ▼
┌──────────────┐
│  Databases   │ ◄── PostgreSQL, MongoDB, Redis, ChromaDB
└──────────────┘
```

## Technology Stack

### Languages & Frameworks
- **Python**: FastAPI (most services)
- **Node.js**: Express (optional for some services)
- **Go**: High-performance services (optional)

### Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Message Bus**: RabbitMQ → Kafka (as scale demands)
- **API Gateway**: Kong or Traefik
- **Service Mesh**: Istio or Linkerd (optional, Phase 5)

### Databases
- **PostgreSQL**: Relational data (tasks, users, permissions)
- **MongoDB**: Unstructured data (logs, flexible schemas)
- **Redis**: Caching, sessions, rate limiting
- **ChromaDB**: Vector embeddings (RAG)

### Monitoring & Observability
- **Metrics**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana) or Loki
- **Tracing**: Jaeger or Zipkin
- **APM**: OpenTelemetry instrumentation

### CI/CD
- **Version Control**: Git + GitHub
- **CI/CD**: GitHub Actions
- **GitOps**: ArgoCD
- **IaC**: Terraform
- **Package Management**: Helm

## Resources

### External Documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [gRPC Documentation](https://grpc.io/docs/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Kong API Gateway](https://docs.konghq.com/)

### Related Reading
- [Microservices Patterns by Chris Richardson](https://microservices.io/patterns/index.html)
- [Building Microservices by Sam Newman](https://samnewman.io/books/building_microservices_2nd_edition/)
- [The Twelve-Factor App](https://12factor.net/)
- [Strangler Fig Pattern](https://martinfowler.com/bliki/StranglerFigApplication.html)

## Contributing

When updating architecture documentation:

1. **Keep documents in sync**: If you update one document, check if related documents need updates
2. **Version documents**: Update the "Last Updated" date and increment version numbers
3. **Add examples**: Include code examples, diagrams, and real-world scenarios
4. **Review with team**: Get feedback from architects, developers, and DevOps
5. **Update this README**: Keep the status table and key decisions current

## Questions & Support

- **Architecture questions**: Contact Architecture Team
- **Implementation help**: See [Implementation Guide](./IMPLEMENTATION_GUIDE.md) Troubleshooting section
- **API clarifications**: See [API Specifications](./API_SPECIFICATIONS.md) or ask in #backend channel

## Glossary

- **BFF**: Backend for Frontend - API Gateway pattern
- **CQRS**: Command Query Responsibility Segregation
- **gRPC**: Google Remote Procedure Call - high-performance RPC framework
- **JWT**: JSON Web Token - authentication token standard
- **Saga**: Distributed transaction pattern for microservices
- **Strangler Fig**: Incremental migration pattern

---

**Last Updated**: 2025-11-24  
**Document Version**: 1.0  
**Maintained by**: AETHER-AI Architecture Team
