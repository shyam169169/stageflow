import pytest

from stageflow.core.domain.models.models import WorkflowDefinition, Stage, Transition
from stageflow.core.domain.errors.exceptions import WorkflowValidationException
from stageflow.core.domain.validator.workflow_definition_validation import WorkflowDefinitionValidator


def test_workflow_validation():
    workflow = WorkflowDefinition(
        name="delivery",
        initial_stage="ORDERED",
        stages=[
            Stage("ORDERED"),
            Stage("PACKED"),
            Stage("SHIPPED"),
        ],
        transitions=[
            Transition("ORDERED", "PACKED"),
            Transition("PACKED", "SHIPPED"),
        ],
        version=1
    )
    WorkflowDefinitionValidator.validate_workflow(workflow)


def test_duplicate_stage():
    workflow = WorkflowDefinition(
        name="delivery",
        initial_stage="ORDERED",
        stages=[
            Stage("ORDERED"),
            Stage("ORDERED"),
        ],
        transitions=[],
        version=1
    )
    with pytest.raises(WorkflowValidationException):
        WorkflowDefinitionValidator.validate_workflow(workflow)


def test_invalid_transition():
    workflow = WorkflowDefinition(
        name="delivery",
        initial_stage="ORDERED",
        stages=[Stage("ORDERED")],
        transitions=[Transition("ORDERED", "INVALID")],
        version=1
    )

    with pytest.raises(WorkflowValidationException):
        WorkflowDefinitionValidator.validate_workflow(workflow)