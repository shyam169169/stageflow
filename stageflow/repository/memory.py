from stageflow.core.domain.models.models import *
from stageflow.core.domain.errors.exceptions import WorkflowNotFoundException, InstanceNotFoundException, ConcurrentTransitionException

class InMemoryWorkflowRepository():
    def __init__(self):
        self.workflows = {}

    def save(self, workflow: WorkflowDefinition) -> None:
        print ("WORKFLOW SAVED!!!!")
        self.workflows[workflow.name] = workflow

    def get(self, name: str, version: Optional[int] = None) -> WorkflowDefinition:
        workflow = self.workflows.get(name)
        if workflow == None:
            raise WorkflowNotFoundException("workflow '{name}' not found")
        
        if version is not None:
            ## Implement this later
            x = 1
        return self.workflows[name]

    def get_list(self) -> List[WorkflowDefinition]:
        return list(self.workflows.values())

class InMemoryWorkflowInstanceRepository():
    def __init__(self):
        self.instances: dict[str, WorkflowInstance] = {}

    def create(self, instance: WorkflowInstance) -> WorkflowInstance:
        self.instances[instance.id] = instance
        return instance
    
    def get(self, instance_id: str) -> WorkflowInstance:
        instance = self.instances.get(instance_id)
        if instance is None:
            raise InstanceNotFoundException("Instance id '{instance_id}' not found")
        return instance

    def update(self, instance_to_update: WorkflowInstance) -> WorkflowInstance:
        instance_stored = self.get(instance_to_update.id)
        
        ## check for optimistic locking
        if instance_stored.version != instance_to_update.version:
            raise ConcurrentTransitionException("Instance version mismatch. Existing version '{instance_stored.version}' ")

        instance_to_update.version += 1
        self.instances[instance_stored.id] = instance_to_update
    
    def delete(self, instance_id: str) -> None:
        self.instances.pop(instance_id, None)

class InMemoryHistoryRepository():
    def __init__(self):
        self.transition_history: Dict[str, List[TransitionRecord]] =  {}
    
    def record(self, transition: TransitionRecord) -> None:
        instance_id = transition.instance_id

        if instance_id not in self.transition_history:
            self.transition_history[instance_id] = []

        list_of_records = self.transition_history[instance_id]
        list_of_records.append(transition)
        

    def get_all_transitions(self, instance_id: str) -> List[TransitionRecord]:
        return self.transition_history.get(instance_id, None)