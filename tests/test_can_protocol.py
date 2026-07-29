"""
Tests for CAN bus protocol.
"""

import pytest
from software.firmware.can_protocol import (
    CANId,
    PRDStatus,
    FAULT_CODES,
    encode_current_message,
    decode_current_message,
    encode_temperature_message,
)


class TestCANProtocol:
    def test_can_id_values(self):
        assert CANId.HEARTBEAT.value == 0x100
        assert CANId.FAULT_REPORT.value == 0x400

    def test_prd_status_values(self):
        assert PRDStatus.IDLE.value == 0
        assert PRDStatus.FAULT.value == 5

    def test_fault_codes(self):
        assert FAULT_CODES[0x01] == "OVERTEMP_CRITICAL"
        assert FAULT_CODES[0x04] == "WATCHDOG_TIMEOUT"

    def test_encode_decode_current(self):
        original = 150.5
        encoded = encode_current_message(original)
        decoded = decode_current_message(encoded)
        assert decoded == pytest.approx(original)

    def test_encode_temperature(self):
        temps = [25.0, 30.0, 35.0, 40.0]
        encoded = encode_temperature_message(temps)
        assert len(encoded) == 8  # 4 temps * 2 bytes
