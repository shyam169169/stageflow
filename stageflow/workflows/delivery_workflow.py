from stageflow.core.domain.models.models import WorkflowDefinition, Stage, Transition

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

workflow = WorkflowDefinition(
    name="delivery_workflow",
    stages=stages,
    transitions=transitions,
    initial_stage="ordered",
    version=1
)
