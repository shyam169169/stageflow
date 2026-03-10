import pytest

from stageflow.rules.metadata_rule import MetadataRule
from stageflow.core.domain.context import TransitionContext
from stageflow.core.domain.models.models import WorkflowInstance

def test_metadata_rule():
    rule1 = MetadataRule("payment_status", "paid")
    metadata = {"payment_status" : "paid"}
    instance = WorkflowInstance("id", "name", "stage", "id", "orders", metadata=metadata)
    context = TransitionContext(
        instance=instance,
        workflow=None,
        transition=None,
        metadata={}
    )

    rule1 = MetadataRule("payment_status", "paid")
    rule2 = MetadataRule("payment_status", "sent")
    assert rule1.evaluate(context) is True
    assert rule2.evaluate(context) is False
    