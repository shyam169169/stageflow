import pytest

from stageflow.core.domain.models.models import WorkflowDefinition, Stage, Transition, WorkflowInstance
from stageflow.engine.core_engine import WorkflowEngine
from stageflow.repository.memory import InMemoryWorkflowRepository, InMemoryWorkflowInstanceRepository, InMemoryHistoryRepository
from stageflow.core.domain.errors.exceptions import InvalidTansitionException


def create_engine() -> WorkflowEngine:
    workflow_repo = InMemoryWorkflowRepository()
    instance_repo = InMemoryWorkflowInstanceRepository()
    history_repo = InMemoryHistoryRepository()
    return WorkflowEngine(
        workflow_repo=workflow_repo,
        instance_repo=instance_repo,
        history_repo=history_repo
    )

def create_workflow(engine: WorkflowEngine) -> WorkflowDefinition:
    return engine.register_workflow(
        workflow_name="delivery_workflow",
        stages=[
            Stage("ORDERED"),
            Stage("PACKED"),
            Stage("SHIPPED"),
        ],
        transitions=[
            Transition("ORDERED", "PACKED"),
            Transition("PACKED", "SHIPPED"),
        ],
        initial_stage="ORDERED",
        version=1
    )

def create_instance(engine: WorkflowEngine, workflow: WorkflowDefinition) -> WorkflowInstance:    
    return engine.create_instance(
        workflow_name=workflow.name,
        current_stage="ORDERED",
        reference_id="ORDER 123",
        reference_domain="delivery"
    )

def test_workflow_engine_register_workflow():
    engine = create_engine()
    workflow = create_workflow(engine)
    assert workflow.name == "delivery_workflow"
    assert workflow.initial_stage == "ORDERED"

def test_workflow_engine_instance():
    engine = create_engine()
    workflow = create_workflow(engine)
    instance = create_instance(engine, workflow)
    assert instance.id is not None
    assert instance.current_stage is "ORDERED"

def test_workflow_engine_transition():
    engine = create_engine()
    workflow = create_workflow(engine)
    instance = create_instance(engine, workflow)
    instance = engine.do_transition(
        instance.id,
        "PACKED"
    )
    instance = engine.do_transition(
        instance.id,
        "SHIPPED"
    )
    assert instance.current_stage is "SHIPPED"

def test_transition_history():
    engine = create_engine()
    workflow = create_workflow(engine)
    instance = create_instance(engine, workflow)
    instance = engine.do_transition(
        instance.id,
        "PACKED"
    )
    instance = engine.do_transition(
        instance.id,
        "SHIPPED"
    )
    history = engine.get_history(instance.id)
    
    assert len(history) == 2
    assert history[0].to_stage == "PACKED"
    assert history[1].to_stage == "SHIPPED"

def test_available_transitions(): 
    engine = create_engine()
    workflow = create_workflow(engine)
    instance = create_instance(engine, workflow)

    available_transition_stages = engine.get_available_transitions(instance.id)
    assert len(available_transition_stages) == 1
    assert available_transition_stages[0] is "PACKED"

    transitions=[
            Transition("ORDERED", "PACKED"),
            Transition("PACKED", "SHIPPED"),
            Transition("ORDERED", "SHIPPED")
        ]
    workflow.transitions = transitions
    available_transition_stages = engine.get_available_transitions(instance.id)
    assert len(available_transition_stages) == 2
    assert available_transition_stages[0] is "PACKED"
    assert available_transition_stages[1] is "SHIPPED"

def test_terminal_stage_block():
    engine = create_engine()
    workflow = create_workflow(engine)
    instance = create_instance(engine, workflow)

    instance = engine.do_transition(
        instance.id,
        "PACKED"
    )
    instance = engine.do_transition(
        instance.id,
        "SHIPPED"
    )

    with pytest.raises(InvalidTansitionException): 
        engine.do_transition(instance.id, "ORDERED")