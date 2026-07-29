"""
Unit tests for Charging Station modules.
"""

import pytest
from software.station.station_manager import ChargingStation, Capsule, CapsuleRack


class TestCapsule:
    def test_capsule_initial_state(self):
        capsule = Capsule("CAP-001")
        assert capsule.id == "CAP-001"
        assert capsule.charge_level == 0.0
        assert capsule.cycle_count == 0
        assert capsule.fault_code is None

    def test_capsule_to_dict(self):
        capsule = Capsule("CAP-001")
        data = capsule.to_dict()
        assert data["id"] == "CAP-001"
        assert data["charge_level"] == 0.0


class TestCapsuleRack:
    def test_insert_and_remove(self):
        rack = CapsuleRack(capacity=5)
        capsule = Capsule("CAP-001")
        assert rack.insert_capsule(0, capsule) is True
        assert rack.remove_capsule(0) == capsule

    def test_insert_full_slot(self):
        rack = CapsuleRack(capacity=2)
        rack.insert_capsule(0, Capsule("CAP-001"))
        assert rack.insert_capsule(0, Capsule("CAP-002")) is False

    def test_get_charged_capsules(self):
        rack = CapsuleRack(capacity=3)
        charged = Capsule("CAP-FULL")
        charged.charge_level = 0.95
        empty = Capsule("CAP-EMPTY")
        empty.charge_level = 0.1

        rack.insert_capsule(0, empty)
        rack.insert_capsule(1, charged)

        result = rack.get_charged_capsules()
        assert len(result) == 1
        assert result[0].id == "CAP-FULL"


class TestChargingStation:
    def test_authenticate_capsule(self):
        station = ChargingStation("ECC-001")
        capsule = Capsule("CAP-001")
        # Mock: assuming verify_rfid returns True
        result = station.authenticate_capsule(capsule)
        assert capsule.is_authenticated is True
        assert result is True

    def test_diagnose_capsule_fault(self):
        station = ChargingStation("ECC-001")
        hot_capsule = Capsule("CAP-HOT")
        hot_capsule.temperature = 80.0
        assert station.diagnose_capsule(hot_capsule) is False
        assert hot_capsule.fault_code == 0x01

    def test_diagnose_capsule_cycle_limit(self):
        station = ChargingStation("ECC-001")
        old_capsule = Capsule("CAP-OLD")
        old_capsule.cycle_count = 15000
        assert station.diagnose_capsule(old_capsule) is False
        assert old_capsule.fault_code == 0x02

    def test_get_status(self):
        station = ChargingStation("ECC-001")
        status = station.get_status()
        assert status["station_id"] == "ECC-001"
        assert status["capsules_available"] == 0
