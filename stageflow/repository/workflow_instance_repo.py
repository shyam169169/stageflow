
from abc import ABC, abstractmethod
from stageflow.core.domain.models.workflow import *

class WorkflowInstanceRepository:
    @abstractmethod
    def create_instance(self, instance :WorkflowInstance) -> WorkflowInstance:
        pass

    @abstractmethod
    def get_instance(self, instance_id: str) -> WorkflowInstance:
        pass

    @abstractmethod
    def update_instance(self, instance_id: str) -> WorkflowInstance:
        pass

    @abstractmethod
    def delete_instance(self, instance_id: str):
        pass