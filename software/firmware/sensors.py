"""
Sensor interface module for PRD firmware.
Handles ADC reads, temperature conversion, and pressure monitoring.
"""

import struct
from typing import List


class ADCSensor:
    def __init__(self, channel: int, ref_voltage: float = 3.3):
        self.channel = channel
        self.ref_voltage = ref_voltage

    def read_raw(self) -> int:
        return read_adc_register(self.channel)

    def read_voltage(self) -> float:
        raw = self.read_raw()
        return (raw / 4095.0) * self.ref_voltage


class CurrentSensor:
    def __init__(self, sensor_id: int):
        self.sensor_id = sensor_id
        self.adc = ADCSensor(sensor_id)
        self.sensitivity = 0.025  # 25 mV/A

    def read_current(self) -> float:
        voltage = self.adc.read_voltage()
        current = (voltage - 1.65) / self.sensitivity
        return current


class TemperatureSensor:
    def __init__(self, pin: int):
        self.pin = pin
        self.adc = ADCSensor(pin)

    def read_celsius(self) -> float:
        voltage = self.adc.read_voltage()
        resistance = (voltage * 10000) / (3.3 - voltage)
        temp = 1 / (
            1 / 298.15
            + (1 / 3950.0) * (resistance / 10000.0)
        ) - 273.15
        return temp


class PressureSensor:
    def __init__(self, can_id: int):
        self.can_id = can_id

    def read_pressure_bar(self) -> float:
        msg = receive_can_message(self.can_id)
        if msg:
            pressure = struct.unpack("<f", msg.data[:4])[0]
            return pressure
        return 0.0


class SensorArray:
    def __init__(self):
        self.current_sensors = [
            CurrentSensor(i) for i in range(3)
        ]
        self.temp_sensors = [
            TemperatureSensor(i) for i in range(8)
        ]
        self.pressure_sensors = [
            PressureSensor(0x200), PressureSensor(0x201)
        ]

    def read_all_temperatures(self) -> List[float]:
        return [s.read_celsius() for s in self.temp_sensors]

    def read_all_currents(self) -> List[float]:
        return [s.read_current() for s in self.current_sensors]

    def get_average_temperature(self) -> float:
        temps = self.read_all_temperatures()
        return sum(temps[:4]) / 4.0  # Core sensors

    def get_voted_current(self) -> float:
        currents = self.read_all_currents()
        currents.sort()
        return currents[1]  # Median of 3
