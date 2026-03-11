
from abc import ABC, abstractmethod
from stageflow.core.domain.models.models import WorkflowInstance, TransitionRecord
from typing import List

class InstanceRepository(ABC):
    @abstractmethod
    def create(self, instance: WorkflowInstance) -> WorkflowInstance:
        pass

    @abstractmethod
    def get(self, instance_id: str) -> WorkflowInstance:
        pass

    @abstractmethod
    def update(self, instance: WorkflowInstance) -> WorkflowInstance:
        pass

    @abstractmethod
    def delete(self, instance_id: str) -> None:
        pass

class HistoryRepository(ABC):
    @abstractmethod
    def record(self, transition: TransitionRecord) -> None:
        pass

    @abstractmethod
    def get_all_transitions(self, instance_id: str) -> List[TransitionRecord]:
        pass
        