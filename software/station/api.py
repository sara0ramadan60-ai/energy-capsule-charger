"""
REST API for the Charging Station.
Built with FastAPI.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from station_manager import ChargingStation, Capsule

app = FastAPI(title="Energy Capsule Charger API")
station = ChargingStation("ECC-001")


class ExchangeRequest(BaseModel):
    capsule_id: str
    vehicle_id: str


class StatusResponse(BaseModel):
    station_id: str
    capsules_available: int
    total_slots: int
    active_session: bool


@app.get("/status", response_model=StatusResponse)
async def get_status():
    return station.get_status()


@app.post("/exchange")
async def exchange_capsule(request: ExchangeRequest):
    spent = Capsule(request.capsule_id)

    if not station.authenticate_capsule(spent):
        raise HTTPException(status_code=401, detail="Authentication failed")

    if not station.diagnose_capsule(spent):
        raise HTTPException(
            status_code=400,
            detail=f"Capsule rejected: fault code {spent.fault_code}",
        )

    charged = await station.exchange_capsule(spent)
    if not charged:
        raise HTTPException(status_code=503, detail="No charged capsules available")

    return {
        "status": "success",
        "exchanged_capsule_id": charged.id,
        "estimated_range_km": 350,
    }


@app.post("/cancel")
async def cancel_session():
    station.active_capsule = None
    return {"status": "session_cancelled"}
