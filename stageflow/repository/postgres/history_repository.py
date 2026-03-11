from sqlalchemy.orm import Session

from stageflow.repository.base.base_repository import HistoryRepository
from stageflow.repository.postgres.models import TransitionHistoryModel
from stageflow.core.domain.errors.exceptions import InstanceNotFoundException

class PostgresHistoryRepository(HistoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def record(self, transition):
        model = TransitionHistoryModel(**transition.__dict__)
        self.db.add(model)
        self.db.commit()
        