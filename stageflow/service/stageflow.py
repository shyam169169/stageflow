
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from stageflow.repository.memory import InMemoryWorkflowRepository
from stageflow.repository.postgres.instance_repository import PostgresInstanceRepository
from stageflow.repository.postgres.history_repository import PostgresHistoryRepository
from stageflow.api.workflows_loader import workflows_loader
from stageflow.engine.core_engine import WorkflowEngine
from typing import Optional

class Stageflow:
    def __init__(self, db_url, workflows_package):
        # create a DB session
        engine = create_engine(db_url)
        SessionLocal = sessionmaker(bind=engine)
        db = SessionLocal()

        # Create the worklfow engine
        workflow_repo = InMemoryWorkflowRepository()
        instance_repo = PostgresInstanceRepository(db)
        history_repo = PostgresHistoryRepository(db)

        # Create tne engine instance
        self.workflow_engine = WorkflowEngine(
            workflow_repo=workflow_repo,
            instance_repo=instance_repo,
            history_repo=history_repo
        )   

        # Register the workflows
        workflows_loader(self.workflow_engine, workflows_package)

    def create_instance(
        self,
        workflow_name: str,
        reference_id: str,
        reference_domain: str,
        metadata: Optional[dict] = None
    ):
        return self.workflow_engine.create_instance(
            workflow_name,
            reference_id,
            reference_domain,
            metadata
        )

    def do_transition(
        self,
        instance_id: str,
        to_stage: str,
        metadata: Optional[dict] = None,
        triggered_by: Optional[dict] = None
    ):
        return self.workflow_engine.do_transition(
            instance_id,
            to_stage,
            metadata,
            triggered_by
        )

    def get_instance(self, instance_id: str):
        return self.workflow_engine.get_instance(instance_id)

    def get_transition_history(self, instance_id: str):
        return self.workflow_engine.get_history(instance_id)