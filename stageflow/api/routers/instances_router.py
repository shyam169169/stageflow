from fastapi import APIRouter, Depends
from stageflow.api.schemas import CreateInstanceRequest, InstanceResponse, TransitionRequest, TransitionResponse
from stageflow.service.stageflow import Stageflow
from stageflow.api.dependencies import get_stageflow
from typing import List

router = APIRouter(prefix="/instances", tags=["instances"])

@router.post("/", response_model=InstanceResponse)
def create_instance(request: CreateInstanceRequest, stageflow:Stageflow=Depends(get_stageflow)):
    instance = stageflow.create_instance(
        workflow_name=request.workflow_name,
        reference_id=request.reference_id,
        reference_domain=request.reference_domain,
        metadata=request.metadata
    )
    return instance

@router.get("/{instance_id}", response_model=InstanceResponse)
def get_instance(instance_id: str, stageflow:Stageflow=Depends(get_stageflow)):
    return stageflow.get_instance(
        instance_id=instance_id
    )

@router.post("/{instance_id}/transition")
def do_transition(
    instance_id: str,
    request: TransitionRequest, 
    stageflow:Stageflow=Depends(get_stageflow)
):
    transition = stageflow.do_transition(
        instance_id=instance_id,
        to_stage=request.to_stage,
        metadata=request.metadata,
        triggered_by=request.triggered_by
    )
    return transition

@router.get("/{instance_id}/history", response_model=List[TransitionResponse])
def get_all_transitions(instance_id: str, stageflow:Stageflow=Depends(get_stageflow)):
    return stageflow.get_transition_history(instance_id)
