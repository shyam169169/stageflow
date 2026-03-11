from stageflow.repository.postgres.db import engine
from stageflow.repository.postgres.models import Base

Base.metadata.create_all(engine)