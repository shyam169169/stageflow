from abc import ABC
from stageflow.core.domain.models.workflow import *

class WorkflowEngine(ABC):
    def register_workflow(self, workflow: WorkflowDefinition):
        pass

    
    def create_instance(self, workflow: WorkflowInstance):
        pass

    def do_transition(self, transition:Transition):
        pass

    def get_instance(self, instance_id: str) -> WorkflowInstance:
        pass

    def get_history(self, instance_id: str) -> list[TransitionRecord]:
        pass