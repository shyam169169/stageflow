from sqlalchemy.orm import Session
from sqlalchemy import update

from stageflow.repository.base.base_repository import InstanceRepository
from stageflow.repository.postgres.models import WorkflowInstanceModel
from stageflow.core.domain.errors.exceptions import InstanceNotFoundException, ConcurrentTransitionException
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
            .filter(WorkflowInstanceModel.id==instance_id)
            .first()
        )
        if not model:
            raise InstanceNotFoundException(f"Instance {instance_id} not found")
        
        return WorkflowIntanceWrapper.to_domain(model)
    
    def update(self, instance):
        query = (
            update(WorkflowInstanceModel)
            .where(
                WorkflowInstanceModel.id == instance.id,
                WorkflowInstanceModel.version == instance.version
            )
            .values(
                current_stage=instance.current_stage,
                metadata_json=instance.metadata,
                version=instance.version+1
            )
        )
        result = self.db.execute(query)

        if result.rowcount == 0:
            raise ConcurrentTransitionException(f"Concurrent updates detected for instance {instance.id}")
        self.db.commit()
        instance.version += 1
        return instance