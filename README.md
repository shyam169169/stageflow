# 🚀 StageFlow

**StageFlow** is a lightweight, extensible workflow engine for backend systems.

It allows you to define **state machines (workflows)** and execute them with:

- rules
- transitions
- history tracking
- persistence
- hooks for integrations

---

## ✨ Features

- ✅ Configurable workflow definitions  
- ✅ Dynamic state transitions  
- ✅ Rule engine (metadata, expressions, time-based)  
- ✅ Transition hooks (before/after)  
- ✅ PostgreSQL persistence  
- ✅ Optimistic locking (concurrency safe)  
- ✅ Transition history tracking  
- ✅ Graph visualization (Graphviz)  
- ✅ REST API (FastAPI)  
- ✅ Clean service interface for easy integration
- ✅ Docker containerization

---

## 💡 Why StageFlow?

Most backend systems implement ad-hoc state transitions.

StageFlow provides:
- structured workflow management
- safe state transitions
- extensibility via rules and hooks

Designed to simplify complex business processes like:
- order pipelines
- payment flows
- approvals

---

## 🧠 Use Cases

- Order / delivery tracking  
- Payment processing flows  
- User onboarding pipelines  
- Approval workflows  
- Internal business processes  

---

## 🏗 Architecture

```
                           ┌──────────────────────────────┐
                           │        Client / API          │
                           │ (HTTP / Service / CLI / SDK) │
                           └──────────────┬───────────────┘
                                          │
                                          ▼
                           ┌──────────────────────────────┐
                           │        FastAPI Layer         │
                           │  Routers / Schemas / DI      │
                           └──────────────┬───────────────┘
                                          │
                                          ▼
                           ┌──────────────────────────────┐
                           │     StageFlow Service        │
                           │  (Public Interface / SDK)    │
                           └──────────────┬───────────────┘
                                          │
                                          ▼
                           ┌──────────────────────────────┐
                           │      Workflow Engine         │
                           │  State Machine + Rules       │
                           └──────────────┬───────────────┘
                                          │
                 ┌────────────────────────┼────────────────────────┐
                 ▼                        ▼                        ▼
      ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
      │     Rules        │     │      Hooks       │     │   Visualization  │
      │ Metadata/Expr    │     │ Before/After     │     │ Graphviz Export  │
      └──────────────────┘     └──────────────────┘     └──────────────────┘
                                          │
                                          ▼
                           ┌──────────────────────────────┐
                           │      Repository Layer        │
                           │  (Interface + Implementations)
                           └──────────────┬───────────────┘
                                          │
                                          ▼
                           ┌──────────────────────────────┐
                           │       PostgreSQL DB          │
                           │ Instances + History          │
                           └──────────────────────────────┘
```

---

## ⚙️ Quick Start (Docker)

### 1. Run the system

```bash
docker-compose up --build
```

### 2. Open API docs

```
http://localhost:8000/docs
```

---

## 🔥 Demo Flow (Try it out!!)

### Create instance

```bash
curl -X POST http://localhost:8000/instances \
-H "Content-Type: application/json" \
-d '{
  "workflow_name": "delivery_workflow",
  "reference_id": "order_123",
  "reference_type": "ORDER"
}'
```

### Transition

```bash
curl -X POST http://localhost:8000/instances/<id>/transition \
-H "Content-Type: application/json" \
-d '{
  "to_stage": "PACKED"
}'
```

---

### Get state

```bash
curl http://localhost:8000/instances/<id>
```

---

## 📦 Local Installation

```bash
pip install -e .
```

### 1. Define a Workflow

```python
from stageflow.core.domain.models import WorkflowDefinition, Stage, Transition

workflow = WorkflowDefinition(
    name="delivery",
    stages=[
        Stage("ORDERED"),
        Stage("PACKED"),
        Stage("SHIPPED"),
        Stage("DELIVERED", is_terminal=True)
    ],
    transitions=[
        Transition("ORDERED", "PACKED"),
        Transition("PACKED", "SHIPPED"),
        Transition("SHIPPED", "DELIVERED")
    ]
)
```

---

### 2. Initialize StageFlow

```python
from stageflow import StageFlow
import my_app.workflows as workflows

sf = StageFlow(
    db_url="postgresql://localhost/stageflow",
    workflows_package=workflows
)
```

---

### 3. Create Instance

```python
instance = sf.create_instance(
    workflow_name="delivery",
    reference_id="order_123",
    reference_type="ORDER"
)
```

---

### 4. Transition

```python
sf.transition(instance.id, "PACKED")
```

---

### 5. Get State

```python
sf.get_instance(instance.id)
```

---

## 🔁 Workflow Lifecycle

```
Create Instance → Transition → Transition → Terminal State
```

---

## 📊 Visualization

```python
sf.export_graph("delivery")
```

Example:

```
ORDERED → PACKED → SHIPPED → DELIVERED
```

---

## 🧩 Rules

```python
MetadataRule("payment_status", "paid")
```

---

## 🔌 Hooks

```python
class AuditHook(Hook):

    def after_transition(self, context):
        print(context.transition)
```

---

## 🗄 Persistence

- PostgreSQL via SQLAlchemy  
- JSON metadata support  
- Transition history tracking  

---

## 🔐 Concurrency Safety

Uses **optimistic locking**:

```
UPDATE ... WHERE version = ?
```

Prevents race conditions across services.

---

## 🌐 API Endpoints

```
POST   /instances
GET    /instances/{id}
POST   /instances/{id}/transition
GET    /instances/{id}/history
GET    /workflows/{name}/graph
```

---

## 🧪 Testing

```bash
pytest
```

---

## 🧱 Project Structure

```
stageflow/
├── api/
├── core/
├── service/
├── engine/
├── repository/
├── rules/
├── hooks/
├── visualization/
├── workflows/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

---

## 🚀 Roadmap

- [ ] Workflow versioning  
- [ ] Async hooks  
- [ ] Kafka / event integration  
- [ ] UI dashboard  
- [ ] Multi-tenant workflows  

---

## 🤝 Contributing

Contributions are welcome!

---

## 📄 License

MIT License
