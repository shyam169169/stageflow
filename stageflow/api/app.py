#initialize the engine once
from fastapi import FastAPI
from contextlib import asynccontextmanager
from stageflow.service.stageflow import Stageflow
from stageflow.api.routers import instances_router, workflow_router
import stageflow.workflows as workflows

@asynccontextmanager
async def lifespan(app: FastAPI):
    print ("!!!!Starting STAGEFLOW API!!!!!")
    stageflow = Stageflow(
        db_url="postgresql://localhost/stageflow",
        workflows_package=workflows
    )
    app.state.stageflow = stageflow

    yield

app = FastAPI(
    title="Stageflow API",
    version="1.0",
    lifespan=lifespan
)

app.include_router(instances_router.router)
app.include_router(workflow_router.router)


