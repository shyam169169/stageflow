
from fastapi import FastAPI, Request
from stageflow.core.domain.errors.exceptions import StageFlowException
from fastapi.responses import JSONResponse

def register_exception_handlers(app: FastAPI):

    @app.exception_handler(StageFlowException)
    async def stageflow_exception_handler(request: Request, ex: StageFlowException):
        return JSONResponse(
            status_code=400,
            content={
                "error": ex.code,
                "message": str(ex)
            }
        )
    
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, ex: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": ""
            }
        )