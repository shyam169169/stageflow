from pydantic import BaseModel
from datetime import datetime

class WorkflowDefinition(BaseModel):
    name: str
    stages : list[Stage]
    transitions : list[Transition]
    version: int

class WorkflowInstance[BaseModel]:
    id: str
    workflow_name: str
    current_stage: str
    reference_id: str # link to external system ids ORderid mapping to payment id on external system
    reference_domain: str # order, payment, user etc 
    metadata: dict  | None # Used for data points for rules
    created_date: datetime
    updated_date: datetime
    created_by: str
    updated_by: str

class Transition[BaseModel]:
    from_stage: str
    to_stage: str
    metadata: dict | None
    rules : list["Rule"] # Something like if payment == success, proceed with the transition

class TransitionRecord[BaseModel]: # When did the order move to SHIPPED? Which stage is causing delays?
    id: str
    workflow_instance_id: int
    from_stage: str
    to_stage: str
    created_date: datetime
    metadata_snapshot: dict | None

class Stage[BaseModel]:
    name: str
    is_terminal: bool = False
    metadata: dict | None

class TransitionContext[BaseModel]:
    instance: WorkflowInstance
    metadata: dict| None
    transition: Transition


