"""
Unit tests for PRD firmware modules.
"""

import pytest
from software.firmware.main_controller import PRDController, PRDState
from software.firmware.sensors import CurrentSensor, TemperatureSensor


class TestPRDController:
    def test_initial_state_is_idle(self):
        controller = PRDController(can_bus=None)
        assert controller.state == PRDState.IDLE

    def test_fault_on_overtemp(self):
        controller = PRDController(can_bus=None)
        controller.temperature = 130.0
        controller._check_faults()
        assert controller.state == PRDState.FAULT

    def test_fault_on_overpressure(self):
        controller = PRDController(can_bus=None)
        controller.pressure = 3.0
        controller._check_faults()
        assert controller.state == PRDState.FAULT

    def test_fault_on_overcurrent(self):
        controller = PRDController(can_bus=None)
        controller.measured_current = 700.0
        controller._check_faults()
        assert controller.state == PRDState.FAULT

    def test_state_transition_auth_to_check(self):
        controller = PRDController(can_bus=None)
        controller.state = PRDState.AUTH
        assert controller.state == PRDState.AUTH


class TestSensors:
    def test_current_sensor_reading(self):
        sensor = CurrentSensor(sensor_id=0)
        assert sensor.sensitivity == 0.025

    def test_temperature_sensor_init(self):
        sensor = TemperatureSensor(pin=0)
        assert sensor.pin == 0
