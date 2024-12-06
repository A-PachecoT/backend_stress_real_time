from fastapi import APIRouter, HTTPException, status
from typing import Optional

router = APIRouter(prefix="/api/v1/sensors", tags=["sensors"])


@router.post("/")
async def create_sensor_reading():
    """Create a new sensor reading"""
    # TODO: Implement sensor data creation
    pass


@router.get("/latest")
async def get_latest_reading():
    """Get latest sensor reading"""
    # TODO: Implement getting latest sensor data
    pass
