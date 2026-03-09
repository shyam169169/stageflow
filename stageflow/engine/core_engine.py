
import uuid
from datetime import datetime
from stageflow.stageflow.core.domain.models.models import *
from stageflow.stageflow.core.domain.errors.exceptions import *
from stageflow.stageflow.repository.memory import *


class WorkflowEngine:
    def __init__(
            self, 
            workflow_repo: InMemoryWorkflowRepository,
            instance_repo: InMemoryWorkflowInstanceRepository,
            history_repo: InMemoryHistoryRepository): 
        self.workflow_repo = workflow_repo
        self.instance_repo = instance_repo
        self.history_repo = history_repo 

    def register_workflow(self, workflow: WorkflowDefinition):
        self.workflow_repo.save(workflow)

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

        transition = self.get_transition(
            workflow,
            instance.current_stage,
            to_stage
        )

        # Before doing the transition, check for rules
        context = {
            "instance": instance,
            "workflow": workflow,
            "metadata": metadata or {}
        }

        for rule in transition.rules:
            if not rule.evaluate(context):
                raise RuleVoilationException("Rule failed for transition '{transition.from_stage} -> {transition.to_stage}'")
            
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
            metadata=metadata
        )
        self.history_repo.record(record)

        # return the updated instance
        return instance


    def get_instance(self, instance_id: str) -> WorkflowInstance:
        return self.instance_repo.get(instance_id)

    def get_history(self, instance_id: str) -> list[TransitionRecord]:
        return self.history_repo.get_all_transitions(instance_id)
    
    def get_transition(self, workflow, from_stage, to_stage) -> Transition:
        workflow = self.workflow_repo.get(workflow)

        for transition in workflow.transitions:
            if (from_stage == transition.from_stage 
            and to_stage == transition.to_stage): 
                return transition
        
        raise InvalidTansitionException("Transition from '{from_stage}' to '{to_stage}' not allowed")