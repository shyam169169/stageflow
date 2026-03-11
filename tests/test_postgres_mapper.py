import pytest

from stageflow.core.domain.models.models import WorkflowInstance, TransitionRecord
from stageflow.repository.postgres.mapper import WorkflowIntanceWrapper, TransitionHistoryWrapper

def test_postgres_instance_mapping():
    instance = WorkflowInstance(
        id="1",
        workflow_name="delivery",
        workflow_version=1,
        reference_id="order_1",
        reference_domain="ORDER",
        current_stage="ORDERED",
        metadata={"payment": "paid"}
    )
    model = WorkflowIntanceWrapper.to_model(instance)
    instance_from_model = WorkflowIntanceWrapper.to_domain(model)
    assert instance == instance_from_model

def test_postgres_history_mapping():
    transition = TransitionRecord(
        id="transition_id",
        instance_id="1",
        from_stage="ORDERED",
        to_stage="PACKED",
        metadata_snapshot={"payment": "paid"}
    )

    model = TransitionHistoryWrapper.to_model(transition)
    transition_from_model = TransitionHistoryWrapper.to_domain(model)
    assert transition == transition_from_model

