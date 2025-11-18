# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routes import trajectory
from .logger import logger
import time

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Coverage Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # allow all domains (or restrict later)
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, DELETE, etc.
    allow_headers=["*"],
)

app.include_router(trajectory.router, prefix="/trajectory", tags=["trajectory"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = (time.time() - start) * 1000
    logger.info(f"{request.method} {request.url.path} status={response.status_code} time_ms={duration:.2f}")
    return response
