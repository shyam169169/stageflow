from stageflow.repository.workflow_instance_repo import WorkflowInstanceRepository

class InMemoryRepository(WorkflowInstanceRepository):
    def __init__(self):
        self.instances = {}
    