from fastapi import FastAPI, Security, HTTPException, Depends, status, requests, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.security import APIKeyHeader
from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import os, glueops.setup_logging, traceback, base64, yaml, tempfile, json
from schemas.schemas import Message, CloudDevelopmentEnvironmentRequest
from util import github
from fastapi.responses import RedirectResponse


# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger = glueops.setup_logging.configure(level=LOG_LEVEL)


app = FastAPI(
    title="Cloud Developer Environments API",
    description="Quick Provision a new Cloud Development Environment",
    version=os.getenv("VERSION", "unknown"),
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Extract the full stack trace
    stack_trace = traceback.format_exc()

    logger.error(f"Exception: {str(exc)} STACK_TRACE: {stack_trace}")
    
    # Return the full stack trace in the response
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An internal server error occurred.",
            "error": str(exc),
            "traceback": stack_trace,  # Include the full stack trace
        },
    )


@app.post("/v1/create-cloud-development-environment", response_class=JSONResponse, summary="Run this to create a new developer environment.  Be sure to update the request parameters")
async def nuke_aws_captain_account(request: CloudDevelopmentEnvironmentRequest):
    url = github.create_cloud_development_environment(request)
    return {"url": url} 


@app.get("/health", include_in_schema=False)
async def health():
    """health check

    Returns:
        dict: health status
    """
    return {"status": "healthy"}


@app.get("/version",  include_in_schema=False)
async def version():
    return {
        "version": os.getenv("VERSION", "unknown"),
        "commit_sha": os.getenv("COMMIT_SHA", "unknown"),
        "build_timestamp": os.getenv("BUILD_TIMESTAMP", "unknown")
    }
