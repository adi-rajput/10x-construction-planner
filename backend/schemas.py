# backend/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Any

class Obstacle(BaseModel):
    x: float  # meters
    y: float
    width: float
    height: float

class Wall(BaseModel):
    width: float
    height: float

class PlannerInput(BaseModel):
    name: str
    wall: Wall
    obstacles: List[Obstacle] = []
    resolution: Optional[float] = 0.1  # meters per grid cell

class TrajectoryOut(BaseModel):
    id: int
    name: str
    path: Any
    meta: Any
    created_at: str
