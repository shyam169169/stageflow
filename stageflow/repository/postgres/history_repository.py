from sqlalchemy.orm import Session

from stageflow.repository.base.base_repository import HistoryRepository
from stageflow.repository.postgres.models import TransitionHistoryModel
from stageflow.repository.postgres.mapper import TransitionHistoryWrapper
from stageflow.core.domain.models.models import TransitionRecord
from typing import List

class PostgresHistoryRepository(HistoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def record(self, transition):
        model = TransitionHistoryWrapper.to_model(transition)
        self.db.add(model)
        self.db.commit()
    
    def get_all_transitions(self, instance_id):
        models = (
            self.db.query(TransitionHistoryModel)
            .filter(TransitionHistoryModel.instance_id==instance_id)
            .all()
        )

        if not models:
            raise Exception(f"Transitions for Instance {instance_id} not found")
        
        list_transitions: List[TransitionRecord] = []
        for model in models:
            list_transitions.append(TransitionHistoryWrapper.to_domain(model))
        return list_transitions
        