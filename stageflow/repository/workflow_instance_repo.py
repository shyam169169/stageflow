
from abc import ABC, abstractmethod
from stageflow.stageflow.core.domain.models.models import *

class WorkflowInstanceRepository:
    @abstractmethod
    def save(self, instance :WorkflowInstance) -> WorkflowInstance:
        pass

    @abstractmethod
    def get(self, instance_id: str) -> WorkflowInstance:
        pass

    @abstractmethod
    def update(self, instance_id: str) -> WorkflowInstance:
        pass

    @abstractmethod
    def delete(self, instance_id: str):
        pass