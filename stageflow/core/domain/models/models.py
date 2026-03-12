
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field
from stageflow.rules.base_rule import Rule


@dataclass
class Transition:
    from_stage: str
    to_stage: str
    metadata: Optional[Dict] = None
    rules: Optional[list[Rule]] = None

@dataclass
class Stage:
    name: str
    is_terminal: bool = False
    metadata: Optional[dict] = None

@dataclass
class WorkflowDefinition:
    name: str
    stages : list[Stage]
    transitions : list[Transition]
    initial_stage: str
    version: int

    def allowed_transitions_from(self, stage_name: str) -> List[Transition]:
        return [
            transition 
            for transition in self.transitions
            if transition.from_stage == stage_name
        ]
    
    def get_stage(self, stage_name:str) -> Stage:
        stage = None
        for stage in self.stages: 
            if stage.name == stage_name:
                return stage
        
@dataclass
class WorkflowInstance:
    id: str
    workflow_name: str
    current_stage: str
    reference_id: str # link to external system ids ORderid mapping to payment id on external system
    reference_domain: str # order, payment, user etc 
    metadata: Optional[dict] = None # Used for data points for rules
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1 ## This is used for optimistic locking
    workflow_version:int = 1


@dataclass
class TransitionRecord: # When did the order move to SHIPPED? Which stage is causing delays?
    id: str
    instance_id: str
    from_stage: str
    to_stage: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata_snapshot: Optional[Dict] = None




