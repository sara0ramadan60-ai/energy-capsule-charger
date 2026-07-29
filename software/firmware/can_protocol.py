"""
CAN bus protocol definitions for PRD communication.
"""

from enum import Enum


class CANId(Enum):
    HEARTBEAT = 0x100
    STATUS = 0x101
    CURRENT_MEASUREMENT = 0x200
    TEMPERATURE = 0x201
    PRESSURE = 0x202
    CONTROL_COMMAND = 0x300
    FAULT_REPORT = 0x400
    DIAGNOSTIC_REQUEST = 0x500
    DIAGNOSTIC_RESPONSE = 0x501


class PRDStatus(Enum):
    IDLE = 0
    AUTHENTICATING = 1
    CHECKING = 2
    CHARGING = 3
    VENTING = 4
    FAULT = 5
    COMPLETE = 6


FAULT_CODES = {
    0x01: "OVERTEMP_CRITICAL",
    0x02: "OVERPRESSURE",
    0x03: "OVERCURRENT",
    0x04: "WATCHDOG_TIMEOUT",
    0x05: "AUTH_FAILED",
    0x06: "DIAGNOSTIC_FAILED",
    0x07: "COMMS_LOST",
    0x08: "CONTACTOR_FAILURE",
}


def encode_current_message(current_a: float) -> bytes:
    import struct
    return struct.pack("<f", current_a)


def decode_current_message(data: bytes) -> float:
    import struct
    return struct.unpack("<f", data[:4])[0]


def encode_temperature_message(temp_c: list[float]) -> bytes:
    result = bytearray()
    for t in temp_c[:4]:
        val = int((t + 100) * 100)
        result.extend(val.to_bytes(2, "big"))
    return bytes(result)
