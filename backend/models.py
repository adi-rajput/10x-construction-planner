# backend/models.py
from sqlalchemy import Column, Integer, String, DateTime, JSON, Index
from datetime import datetime
from .database import Base

class Trajectory(Base):
    __tablename__ = "trajectories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # JSON column stores list of [x,y] coordinates or segments
    path = Column(JSON, nullable=False)
    meta = Column(JSON, nullable=True)     # store wall dims, resolution, obstacles
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

# create helpful index on created_at
Index("idx_created_at", Trajectory.created_at)
