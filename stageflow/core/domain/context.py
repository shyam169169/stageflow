from dataclasses import dataclass, field
from typing import Dict, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from stageflow.core.domain.models.models import (
        WorkflowDefinition,
        WorkflowInstance,
        Transition
    )

@dataclass
class TransitionContext:
    instance: "WorkflowInstance"
    workflow: "WorkflowDefinition"
    transition: "Transition"
    metadata : Dict
    timestamp: datetime = field(default_factory=datetime.utcnow)
    triggered_by: Optional[str] = None