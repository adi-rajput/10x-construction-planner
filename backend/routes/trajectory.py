# backend/routes/trajectory.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, planner, crud, database
from ..logger import logger
import time

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_traj(payload: schemas.PlannerInput, db: Session = Depends(get_db)):
    start = time.time()
    obs = [o.dict() for o in payload.obstacles]
    path = planner.generate_coverage_path(payload.wall.dict(), obs, payload.resolution)
    meta = {"wall": payload.wall.dict(), "obstacles": obs, "resolution": payload.resolution}
    obj = crud.create_trajectory(db, payload.name, path, meta)
    duration = (time.time() - start) * 1000
    logger.info(f"Created trajectory id={obj.id} name={payload.name} duration_ms={duration:.2f}")
    return {"id": obj.id, "duration_ms": duration}

@router.get("/list")
def list_trajs(skip:int=0, limit:int=100, db: Session = Depends(get_db)):
    start = time.time()
    items = crud.list_trajectories(db, skip, limit)
    duration = (time.time() - start) * 1000
    logger.info(f"Listed trajectories count={len(items)} duration_ms={duration:.2f}")
    return [{"id":i.id,"name":i.name,"created_at":i.created_at,"meta":i.meta} for i in items]

@router.get("/{id}")
def get_traj(id:int, db: Session = Depends(get_db)):
    start = time.time()
    obj = crud.get_trajectory(db, id)
    duration = (time.time() - start) * 1000
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    logger.info(f"Get id={id} duration_ms={duration:.2f}")
    return {"id":obj.id,"name":obj.name,"path":obj.path,"meta":obj.meta,"created_at":obj.created_at}

@router.delete("/{id}")
def delete_traj(id:int, db: Session = Depends(get_db)):
    obj = crud.delete_trajectory(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Not found")
    logger.info(f"Deleted id={id}")
    return {"status":"deleted"}
