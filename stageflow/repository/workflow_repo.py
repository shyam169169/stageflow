
from abc import ABC, abstractmethod
from stageflow.core.domain.models.models import WorkflowDefinition
from typing import Optional, List

class WorkflowRepository(ABC):

    @abstractmethod
    def save(self, workflow: WorkflowDefinition):
        pass

    
    @abstractmethod
    def get(self, name: str, 
            version: Optional[int] = None
            ) ->WorkflowDefinition:
        pass

    @abstractmethod
    def get_all(self) -> List[WorkflowDefinition]:
        pass