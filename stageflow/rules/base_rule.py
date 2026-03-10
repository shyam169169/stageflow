from abc import ABC, abstractmethod
from stageflow.core.domain.context import TransitionContext

class Rule(ABC):
    @abstractmethod
    def evaluate(self, context: TransitionContext) -> bool:
        pass
