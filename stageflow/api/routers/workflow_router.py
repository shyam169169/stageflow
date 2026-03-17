from fastapi import APIRouter, Depends
from stageflow.service.stageflow import Stageflow
from stageflow.api.dependencies import get_stageflow

router = APIRouter(prefix="/workflows", tags=["workflows"])

@router.get("/{workflow_name}/graph")
def export_graph(
    workflow_name: str,
    stageflow:Stageflow=Depends(get_stageflow)
):
    return {"dot": stageflow.export_graph(workflow_name)}
