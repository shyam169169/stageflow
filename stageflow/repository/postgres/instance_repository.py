from sqlalchemy.orm import Session

from stageflow.repository.base.base_repository import InstanceRepository
from stageflow.repository.postgres.models import WorkflowInstanceModel
from stageflow.core.domain.errors.exceptions import InstanceNotFoundException
from stageflow.repository.postgres.mapper import WorkflowIntanceWrapper

class PostgresInstanceRepository(InstanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, instance):
        model = WorkflowIntanceWrapper.to_model(instance)
        self.db.add(model)
        self.db.commit()
        return instance
    
    def get(self, instance_id):
        model = (
            self.db.query(WorkflowInstanceModel)
            .filter_by(id=instance_id)
            .first()
        )

        if not model:
            raise Exception(f"Instance {instance_id} not found")
        
        return WorkflowIntanceWrapper.to_domain(model)