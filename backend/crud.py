# backend/crud.py
from sqlalchemy.orm import Session
from . import models

def create_trajectory(db: Session, name: str, path: list, meta: dict):
    obj = models.Trajectory(name=name, path=path, meta=meta)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_trajectory(db: Session, id: int):
    return db.query(models.Trajectory).filter(models.Trajectory.id == id).first()

def list_trajectories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trajectory).order_by(models.Trajectory.created_at.desc()).offset(skip).limit(limit).all()

def delete_trajectory(db: Session, id: int):
    obj = db.query(models.Trajectory).filter(models.Trajectory.id == id).first()
    if obj:
        db.delete(obj)
        db.commit()
    return obj
