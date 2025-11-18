# backend/logger.py
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("coverage_planner")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("coverage_planner.log", maxBytes=2_000_000, backupCount=3)
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(fmt)
logger.addHandler(handler)
