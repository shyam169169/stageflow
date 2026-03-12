#initialize the engine once
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session

from stageflow.repository.memory import InMemoryWorkflowRepository
from stageflow.repository.postgres.instance_repository import PostgresInstanceRepository
from stageflow.repository.postgres.history_repository import PostgresHistoryRepository
from stageflow.repository.postgres.db import SessionLocal
from stageflow.api.workflows_loader import workflows_loader
import stageflow.workflows as workflows
from stageflow.engine.core_engine import WorkflowEngine
from stageflow.api.schemas import InstanceResponse, CreateInstanceRequest, TransitionRequest
from stageflow.api.dependencies import get_engine

@asynccontextmanager

def create_engine(db: Session) -> WorkflowEngine:
    # Inject the repositories
    workflow_repo = InMemoryWorkflowRepository()
    instance_repo = PostgresInstanceRepository(db)
    history_repo = PostgresHistoryRepository(db)

    # Create tne engine instance
    return WorkflowEngine(
        workflow_repo=workflow_repo,
        instance_repo=instance_repo,
        history_repo=history_repo
    )   

async def lifespan(app: FastAPI):
    # get DB session
    db = SessionLocal()

    # Create the engine
    workflow_repo = InMemoryWorkflowRepository()
    instance_repo = PostgresInstanceRepository(db)
    history_repo = PostgresHistoryRepository(db)

    # Create tne engine instance
    engine = WorkflowEngine(
        workflow_repo=workflow_repo,
        instance_repo=instance_repo,
        history_repo=history_repo
    )   

    # Register the workflows
    workflows_loader(engine, workflows)

    #assign engine to app
    app.state.engine = engine

    yield

app = FastAPI(
    title="Stageflow API",
    version="1.0",
    lifespan=lifespan
)

@app.post("/instances", response_model=InstanceResponse)
def create_instance(request: CreateInstanceRequest, engine:WorkflowEngine=Depends(get_engine)):
    instance = engine.create_instance(
        workflow_name=request.workflow_name,
        reference_id=request.reference_id,
        reference_domain=request.reference_domain,
        metadata=request.metadata
    )
    print ("Entering APIsdsdfdsf!!!")
    return instance

@app.get("/instances/{instance_id}", response_model=InstanceResponse)
def get_instance(instance_id: str, engine:WorkflowEngine=Depends(get_engine)):
    print ("Entering API!!!!")
    return engine.get_instance(
        instance_id=instance_id
    )

@app.post("/instances/{instance_id}/transition")
def do_transition(
    instance_id: str,
    request: TransitionRequest, 
    engine:WorkflowEngine=Depends(get_engine)
):
    transition = engine.do_transition(
        instance_id=instance_id,
        to_stage=request.to_stage,
        metadata=request.metadata,
        triggered_by=request.triggered_by
    )
    return transition

@app.get("/workflows/{workflow_name}/graph")
def export_graph(
    workflow_name: str,
    engine:WorkflowEngine=Depends(get_engine)
):
    return {"dot": engine.export_graph(workflow_name)} 
