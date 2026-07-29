"""
Main controller for Pressure Release Device (PRD) firmware.
Runs on ARM Cortex-M7 @ 300 MHz.
"""

import can
import time
import asyncio
from enum import Enum


class PRDState(Enum):
    IDLE = 0
    AUTH = 1
    CHECK = 2
    CHARGE = 3
    VENT = 4
    FAULT = 5


class PRDController:
    def __init__(self, can_bus: can.Interface):
        self.state = PRDState.IDLE
        self.can = can_bus
        self.target_current = 0.0
        self.measured_current = 0.0
        self.temperature = 25.0
        self.pressure = 1.0
        self.power_limit = 1.0
        self.watchdog = 0

    async def run(self):
        while True:
            self.watchdog += 1
            self._read_sensors()
            self._check_faults()

            if self.state == PRDState.IDLE:
                await self._handle_idle()
            elif self.state == PRDState.AUTH:
                await self._handle_auth()
            elif self.state == PRDState.CHECK:
                await self._handle_check()
            elif self.state == PRDState.CHARGE:
                await self._handle_charge()
            elif self.state == PRDState.VENT:
                await self._handle_vent()
            elif self.state == PRDState.FAULT:
                await self._handle_fault()

            self._send_heartbeat()
            await asyncio.sleep(0.001)  # 1 kHz control loop

    def _read_sensors(self):
        self.measured_current = read_current_sensor()
        self.temperature = read_temperature_sensors()
        self.pressure = read_pressure_sensors()

    def _check_faults(self):
        if self.temperature > 120.0:
            self._enter_fault("OVERTEMP_CRITICAL")
        elif self.pressure > 2.5:
            self._enter_fault("OVERPRESSURE")
        elif self.measured_current > 600.0:
            self._enter_fault("OVERCURRENT")
        elif self.watchdog > 1000:
            self._enter_fault("WATCHDOG_TIMEOUT")

    def _enter_fault(self, reason: str):
        self.state = PRDState.FAULT
        open_cutoff_relays()
        log_error(reason)
        send_alert(reason)

    async def _handle_idle(self):
        if detect_capsule_insertion():
            self.state = PRDState.AUTH

    async def _handle_auth(self):
        capsule_id = read_rfid()
        if authenticate_capsule(capsule_id):
            self.state = PRDState.CHECK
        else:
            self._enter_fault("AUTH_FAILED")

    async def _handle_check(self):
        if run_self_diagnostic():
            self.state = PRDState.CHARGE
        else:
            self._enter_fault("DIAGNOSTIC_FAILED")

    async def _handle_charge(self):
        self.target_current = calculate_target_current()
        self._apply_current_control()

        if is_charge_complete():
            self.state = PRDState.VENT

    def _apply_current_control(self):
        error = self.target_current - self.measured_current
        pwm_duty = pid_controller(error)
        set_pwm_output(pwm_duty)

    async def _handle_vent(self):
        open_vent_valve()
        await asyncio.sleep(5.0)
        close_vent_valve()
        self.state = PRDState.IDLE

    async def _handle_fault(self):
        activate_alarm()
        await asyncio.sleep(3600)
        if is_fault_cleared():
            self.state = PRDState.IDLE

    def _send_heartbeat(self):
        msg = can.Message(
            arbitration_id=0x100,
            data=[self.state.value, self.watchdog & 0xFF],
            is_extended_id=False,
        )
        self.can.send(msg)
