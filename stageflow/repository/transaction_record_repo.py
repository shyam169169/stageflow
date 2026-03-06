
from abc import ABC, abstractmethod
from stageflow.core.domain.models.models import TransitionRecord
from typing import List

class TransactionRecordRepository(ABC):
    @abstractmethod
    def save(self, transaction_record: TransitionRecord):
        pass

    @abstractmethod
    def get(self, instance_id: str) -> List[TransitionRecord]:
        pass

    @abstractmethod
    def update():
        pass

    @abstractmethod
    def delete():
        pass