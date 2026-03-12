from pydantic import BaseModel
from typing import Optional, Dict

class CreateInstanceRequest(BaseModel):
    workflow_name: str
    reference_id: str
    reference_domain: str
    metadata: Optional[Dict] = None

class TransitionRequest(BaseModel):
    to_stage: str
    metadata: Optional[Dict] = None
    triggered_by: Optional[str] = None

class InstanceResponse(BaseModel):
    id: str
    workflow_name: str
    current_stage: str
    reference_id: str