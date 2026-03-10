
import uuid
from datetime import datetime
from typing import Set
from stageflow.core.domain.models.models import *
from stageflow.core.domain.errors.exceptions import *
from stageflow.repository.memory import *
from stageflow.core.domain.context import TransitionContext
from stageflow.core.domain.validator.workflow_definition_validation import WorkflowDefinitionValidator
from stageflow.hooks.base_hooks import Hook

class WorkflowEngine:
    def __init__(
            self, 
            workflow_repo: InMemoryWorkflowRepository,
            instance_repo: InMemoryWorkflowInstanceRepository,
            history_repo: InMemoryHistoryRepository): 
        self.workflow_repo = workflow_repo
        self.instance_repo = instance_repo
        self.history_repo = history_repo
        self.hooks: List[Hook] = []

    def register_hooks(self, hook: Hook):
        self.hooks.append(hook)

    def register_workflow(
            self, 
            workflow_name: str,
            stages: list[Stage],
            transitions: list[Transition],
            initial_stage: str,
            version: int) -> WorkflowDefinition:
        workflow = WorkflowDefinition(
            name=workflow_name,
            stages=stages,
            transitions=transitions,
            initial_stage=initial_stage,
            version=version
        )

        WorkflowDefinitionValidator.validate_workflow(workflow)
        self.workflow_repo.save(workflow)
        return workflow

    def create_instance(
            self,
            workflow_name: str,
            current_stage: str,
            reference_id: str,
            reference_domain: str,
            metadata : Optional[dict] = None
        ) -> WorkflowInstance:
        
        instance = WorkflowInstance(
            id=str(uuid.uuid4()),
            workflow_name=workflow_name,
            current_stage=current_stage,
            reference_id=reference_id,
            reference_domain=reference_domain,
            metadata=metadata
        )
        return self.instance_repo.create(instance)

    def do_transition(
            self, 
            instance_id: str,
            to_stage: str,
            metadata: Optional[Dict] = None,
            triggered_by: Optional[str] = None) -> WorkflowInstance:

        instance = self.instance_repo.get(instance_id)

        workflow = self.workflow_repo.get(instance.workflow_name)

        # Validate if stage is terminal or it doesn't have any transitions
        stage = workflow.get_stage(instance.current_stage)
        allowed_transitions = workflow.allowed_transitions_from(instance.current_stage)

        if not allowed_transitions or not stage or stage.is_terminal:
            raise InvalidTansitionException (f"No transitions allowed from stage '{instance.current_stage}")

        transition = self.get_transition(
            workflow,
            instance.current_stage,
            to_stage
        )

        # Before doing the transition, check for rules
        context = TransitionContext(
            instance=instance,
            workflow= workflow,
            transition=transition,
            metadata=metadata
        )

        if transition.rules is not None:
            for rule in transition.rules:
                if not rule.evaluate(context):
                    raise RuleVoilationException("Rule failed for transition '{transition.from_stage} -> {transition.to_stage}'")

        
        for hook in self.hooks:
            hook.perform_pre_hook(context)

        from_stage = instance.current_stage
        instance.current_stage = to_stage
        instance.updated_date = datetime.now()

        if metadata:
            instance.metadata.update(metadata)
        
        # Update the instance
        self.instance_repo.update(instance)

        #record the transition
        record = TransitionRecord(
            id=str(uuid.uuid4()),
            instance_id=instance_id,
            from_stage=from_stage,
            to_stage=to_stage,
            metadata_snapshot=metadata
        )
        self.history_repo.record(record)

        # run post hook
        for hook in self.hooks:
            hook.perform_post_hook(context)

        # return the updated instance
        return instance


    def get_instance(self, instance_id: str) -> WorkflowInstance:
        return self.instance_repo.get(instance_id)

    def get_history(self, instance_id: str) -> List[TransitionRecord]:
        return self.history_repo.get_all_transitions(instance_id)
    
    def get_transition(self, workflow: WorkflowDefinition, from_stage: str, to_stage: str) -> Transition:
        workflow = self.workflow_repo.get(workflow.name)

        for transition in workflow.transitions:
            if (from_stage == transition.from_stage 
            and to_stage == transition.to_stage): 
                return transition
        
        raise InvalidTansitionException(f"Transition from {from_stage} to {to_stage} not allowed")
    
    def get_available_transitions(self, instance_id: str) -> List[str]:
        instance = self.instance_repo.get(instance_id)
        workflow = self.workflow_repo.get(instance.workflow_name)

        transitions = workflow.allowed_transitions_from(instance.current_stage)
        return [
            transition.to_stage
            for transition in transitions
        ]
        