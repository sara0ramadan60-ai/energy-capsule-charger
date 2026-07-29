"""
Tests for PID controller.
"""

import pytest
from software.firmware.pid import PIDController


class TestPIDController:
    def test_initial_state(self):
        pid = PIDController()
        assert pid.kp == 0.8
        assert pid.ki == 0.1
        assert pid.kd == 0.05
        assert pid._integral == 0.0
        assert pid._prev_error == 0.0

    def test_pure_proportional(self):
        pid = PIDController(kp=1.0, ki=0.0, kd=0.0)
        output = pid.compute(setpoint=10.0, measurement=0.0)
        assert output == pytest.approx(1.0)

    def test_pid_tracks_setpoint(self):
        pid = PIDController(kp=1.0, ki=0.5, kd=0.1)
        for _ in range(100):
            output = pid.compute(setpoint=10.0, measurement=9.0)
            assert -1.0 <= output <= 1.0

    def test_reset(self):
        pid = PIDController()
        pid.compute(10.0, 0.0)
        pid.reset()
        assert pid._integral == 0.0
        assert pid._prev_error == 0.0

    def test_output_limits(self):
        pid = PIDController(kp=100.0, ki=0.0, kd=0.0, output_limit=0.5)
        output = pid.compute(setpoint=100.0, measurement=0.0)
        assert output == 0.5

    def test_integral_limits(self):
        pid = PIDController(kp=0.0, ki=1.0, kd=0.0, integral_limit=10.0)
        for _ in range(1000):
            pid.compute(setpoint=10.0, measurement=0.0)
        assert pid._integral == 10.0
