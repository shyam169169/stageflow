🚀 StageFlow

StageFlow is a lightweight, extensible workflow engine for backend systems.

It allows you to define state machines (workflows) and execute them with:

rules

transitions

history tracking

persistence

hooks for integrations

✨ Features

✅ Configurable workflow definitions

✅ Dynamic state transitions

✅ Rule engine (metadata, expressions, time-based)

✅ Transition hooks (before/after)

✅ PostgreSQL persistence

✅ Optimistic locking (concurrency safe)

✅ Transition history tracking

✅ Graph visualization (Graphviz)

✅ REST API (via FastAPI)

✅ Clean service interface for easy integration

🧠 Use Cases

Order / delivery tracking

Payment processing flows

User onboarding pipelines

Approval workflows

Internal business processes

🏗 Architecture
API → Service → Engine → Repository → Database

API Layer → Handles HTTP requests

Service Layer → Public interface (SDK-like)

Engine → Core workflow execution

Repositories → Persistence abstraction

Database → PostgreSQL

📦 Installation
pip install -e .
⚙️ Quick Start
1. Define a Workflow
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
2. Initialize StageFlow
from stageflow import StageFlow
import my_app.workflows as workflows

sf = StageFlow(
    db_url="postgresql://localhost/stageflow",
    workflows_package=workflows
)
3. Create Instance
instance = sf.create_instance(
    workflow_name="delivery",
    reference_id="order_123",
    reference_type="ORDER"
)
4. Transition
sf.transition(instance.id, "PACKED")
5. Get State
sf.get_instance(instance.id)
🔁 Workflow Lifecycle
Create Instance → Transition → Transition → Terminal State
📊 Visualization

Export workflow graph:

sf.export_graph("delivery")

Example:

ORDERED → PACKED → SHIPPED → DELIVERED
🧩 Rules

Example rule:

MetadataRule("payment_status", "paid")
🔌 Hooks
class AuditHook(Hook):

    def after_transition(self, context):
        print(context.transition)
🗄 Persistence

PostgreSQL via SQLAlchemy

JSON metadata support

Transition history tracking

🔐 Concurrency Safety

Uses optimistic locking:

UPDATE ... WHERE version = ?

Prevents race conditions across services.

🌐 API Endpoints
POST   /instances
GET    /instances/{id}
POST   /instances/{id}/transition
GET    /instances/{id}/transitions
GET    /instances/{id}/history
GET    /workflows/{name}/graph
🧪 Testing
pytest
🧱 Project Structure
stageflow/
├── api/
├── service/
├── engine/
├── persistence/
├── rules/
├── hooks/
├── visualization/
├── workflows/
🚀 Roadmap

 Workflow versioning

 Async hooks

 Kafka / event integration

 UI dashboard

 Multi-tenant workflows

🤝 Contributing

Contributions are welcome!

📄 License

MIT License