#initialize the engine once
from fastapi import FastAPI
from contextlib import asynccontextmanager
from stageflow.service.stageflow import Stageflow
from stageflow.api.routers import instances_router, workflow_router
import stageflow.workflows as workflows
import os
from sqlalchemy import create_engine
from stageflow.repository.postgres.models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    print ("!!!!Starting STAGEFLOW API!!!!!")
    db_url = os.getenv("DATABASE_URL", "postgresql://localhost/stageflow")

    db_engine = create_engine(db_url)

    # Create database tables
    Base.metadata.create_all(db_engine)

    stageflow = Stageflow(
        db_url=db_url,
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


