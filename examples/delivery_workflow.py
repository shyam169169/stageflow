from stageflow.engine.core_engine import WorkflowEngine
from stageflow.core.domain.models.models import *
from stageflow.repository.memory import InMemoryHistoryRepository, InMemoryWorkflowInstanceRepository, InMemoryWorkflowRepository
from stageflow.hooks.builtin.audit_hook import AuditHook
from stageflow.hooks.builtin.web_hook import WebHook


stages = [
    Stage("ordered"),
    Stage("packed"),
    Stage("shipped"),
    Stage("in-transit"),
    Stage("delivered", is_terminal=True)
]
transitions = [
    Transition("ordered", "packed"),
    Transition("packed", "shipped"),
    Transition("shipped", "in-transit"),
    Transition("in-transit", "delivered")
]

workflow_repo = InMemoryWorkflowRepository()
instance_repo = InMemoryWorkflowInstanceRepository()
history_repo = InMemoryHistoryRepository()

engine = WorkflowEngine(
    workflow_repo=workflow_repo,
    instance_repo=instance_repo,
    history_repo=history_repo
)

engine.register_hooks(AuditHook())
engine.register_hooks(WebHook())

delivery_workflow = engine.register_workflow(
    workflow_name="delivery_workflow",
    stages=stages,
    transitions=transitions,
    initial_stage="ordered",
    version=1
)

instance = engine.create_instance(
    "delivery_workflow",
    "ordered",
    "order #123",
    "Delivery orders"
)

print("Created instance : ")
print(instance)
print(type({delivery_workflow.name}))

engine.do_transition(instance.id, "packed")
engine.do_transition(instance.id, "shipped")
engine.do_transition(instance.id, "in-transit")
engine.do_transition(instance.id, "delivered")

instance = engine.get_instance(instance.id)
print ("Final state of instance : ")
print(instance)

history = engine.get_history(instance.id)

for record in history:
    print (f"{record.from_stage} -> {record.to_stage}")