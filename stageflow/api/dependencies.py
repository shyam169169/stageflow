
from fastapi import Request
from stageflow.repository.postgres.db import SessionLocal

def get_engine(request: Request):
    return request.app.state.engine

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()