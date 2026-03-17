
from fastapi import Request
from stageflow.repository.postgres.db import SessionLocal
from stageflow.service.stageflow import Stageflow

def get_stageflow(request: Request):
    return request.app.state.stageflow

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()