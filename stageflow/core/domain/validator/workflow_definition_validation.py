from stageflow.core.domain.errors.exceptions import WorkflowValidationException
from typing import Set
from stageflow.core.domain.models.models import WorkflowDefinition

class WorkflowDefinitionValidator:
    @staticmethod
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
        
        # check for unreachable stages in the configuration
        WorkflowDefinitionValidator.check_for_unreachable_stage(workflow)

    @staticmethod
    def check_for_unreachable_stage(workflow: WorkflowDefinition) -> None:
        visited = set()
        stage_graph = {}
        for transition in workflow.transitions:
            stage_graph.setdefault(transition.from_stage, []).append(transition.to_stage)

        WorkflowDefinitionValidator.dfs(workflow.initial_stage, visited, stage_graph)
        all_stages = set(stage_graph.keys())
        unreachable = all_stages - visited

        if unreachable:
                raise WorkflowValidationException(
                    f"Unreachable stages detected : {','.join(unreachable)}")


    @staticmethod
    def dfs(stage: str, visited: dict, stage_graph: dict):
            visited.add(stage)
            for next_stage in stage_graph.get(stage, []):
                WorkflowDefinitionValidator.dfs(next_stage, visited, stage_graph)
