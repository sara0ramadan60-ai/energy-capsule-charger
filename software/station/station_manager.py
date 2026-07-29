"""
Charging Station Manager.
Main application for the capsule exchange station.
"""

import json
import asyncio
from typing import Optional


class Capsule:
    def __init__(self, capsule_id: str):
        self.id = capsule_id
        self.charge_level: float = 0.0
        self.temperature: float = 25.0
        self.cycle_count: int = 0
        self.is_authenticated: bool = False
        self.fault_code: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "charge_level": self.charge_level,
            "temperature": self.temperature,
            "cycle_count": self.cycle_count,
            "fault_code": self.fault_code,
        }


class CapsuleRack:
    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.slots: list[Optional[Capsule]] = [None] * capacity

    def insert_capsule(self, slot: int, capsule: Capsule) -> bool:
        if 0 <= slot < self.capacity and self.slots[slot] is None:
            self.slots[slot] = capsule
            return True
        return False

    def remove_capsule(self, slot: int) -> Optional[Capsule]:
        if 0 <= slot < self.capacity and self.slots[slot]:
            capsule = self.slots[slot]
            self.slots[slot] = None
            return capsule
        return None

    def get_charged_capsules(self) -> list[Capsule]:
        return [c for c in self.slots if c and c.charge_level > 0.9]


class ChargingStation:
    def __init__(self, station_id: str):
        self.station_id = station_id
        self.rack = CapsuleRack()
        self.active_capsule: Optional[Capsule] = None
        self.is_connected: bool = False

    async def exchange_capsule(
        self, spent: Capsule
    ) -> Optional[Capsule]:
        charged_capsules = self.rack.get_charged_capsules()
        if not charged_capsules:
            return None

        charged = charged_capsules[0]
        slot = self.rack.slots.index(charged)

        self.rack.remove_capsule(slot)
        self.rack.insert_capsule(slot, spent)

        return charged

    def authenticate_capsule(self, capsule: Capsule) -> bool:
        capsule.is_authenticated = verify_rfid(capsule.id)
        return capsule.is_authenticated

    def diagnose_capsule(self, capsule: Capsule) -> bool:
        if capsule.temperature > 60.0:
            capsule.fault_code = 0x01
            return False
        if capsule.cycle_count > 10000:
            capsule.fault_code = 0x02
            return False
        return True

    def get_status(self) -> dict:
        return {
            "station_id": self.station_id,
            "capsules_available": len(self.rack.get_charged_capsules()),
            "total_slots": self.rack.capacity,
            "active_session": self.active_capsule is not None,
        }
