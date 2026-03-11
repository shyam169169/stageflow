from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.sql import func

from .db import Base

class WorkflowInstanceModel(Base):
    __tablename__ = "workflow_instance"

    id = Column(String, primary_key=True)
    workflow_name = Column(String, nullable=False)
    workflow_version = Column(Integer)
    referece_id = Column(String)
    referece_domain = Column(String)
    current_stage = Column(String)
    metadata_json = Column("metadata", JSON)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now())

class TransitionHistoryModel(Base):
    __tablename__ = "transition_history"

    id = Column(String, primary_key=True)
    instance_id = Column(String)
    from_stage = Column(String)
    to_stage = Column(String)
    metadata_snapshot_json = Column("metadata_snapshot", JSON)
    triggered_by=Column(String)
    created_at = Column(DateTime, server_default=func.now())