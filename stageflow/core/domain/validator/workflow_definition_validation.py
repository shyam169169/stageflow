from stageflow.core.domain.errors.exceptions import WorkflowValidationException
from typing import Set
from stageflow.core.domain.models.models import WorkflowDefinition

class WorkflowDefinitionValidator:
    def validate_workflow(workflow: WorkflowDefinition):
        # workflow has at least one stage
        if not workflow.stages:
            raise WorkflowValidationException("Workflow should have atleast one stage")

        # duplicate stages
        stage_names: Set[str] = set()
        for stage in workflow.stages:
            if stage.name in stage_names:
                raise WorkflowValidationException(f"Duplicate stage found - {stage.name}")
            stage_names.add(stage.name)

        # workflow's initial stage exists in stages
        if workflow.initial_stage not in stage_names:
            raise WorkflowValidationException("Initial stage not set")
        

        #transition validations
        transition_pairs = set()
        for transition in workflow.transitions:
            if transition.from_stage not in stage_names:
                raise WorkflowValidationException(f"stage {transition.from_stage} is not defined")

            if transition.to_stage not in stage_names:
                raise WorkflowValidationException(f"stage {transition.to_stage} is not defined")
            
            pair = (transition.from_stage, transition.to_stage)

            if pair in transition_pairs:
                raise WorkflowValidationException(f"Duplicate transitions {transition.from_stage} -> {transition.to_stage} found")
        
            transition_pairs.add(pair)

        # terminal stages have no outgoing transitions
        terminal_stages = {
            stage.name for stage in workflow.stages if stage.is_terminal
        }

        for transition in workflow.transitions:
            if transition.from_stage in terminal_stages:
                raise WorkflowValidationException(f"{transition.from_stage} is a terminal stage and cannot have transitions")
