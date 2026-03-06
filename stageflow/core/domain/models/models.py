
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class WorkflowDefinition:
    name: str
    stages : list[Stage]
    transitions : list[Transition]
    version: int

@dataclass
class WorkflowInstance:
    id: str
    workflow_name: str
    current_stage: str
    reference_id: str # link to external system ids ORderid mapping to payment id on external system
    reference_domain: str # order, payment, user etc 
    metadata: dict  | None # Used for data points for rules
    created_date: datetime = field(default_factory=datetime.utcnow)
    updated_date: datetime = field(default_factory=datetime.utcnow)
    created_by: str
    updated_by: str

@dataclass
class Transition:
    from_stage: str
    to_stage: str
    metadata: dict | None
    rules : list["Rule"] # Something like if payment == success, proceed with the transition


@dataclass
class TransitionRecord: # When did the order move to SHIPPED? Which stage is causing delays?
    id: str
    workflow_instance_id: int
    from_stage: str
    to_stage: str
    created_date: datetime = field(default_factory=datetime.utcnow)
    metadata_snapshot: dict | None

@dataclass
class Stage:
    name: str
    is_terminal: bool = False
    metadata: dict | None



