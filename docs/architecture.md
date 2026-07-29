# System Architecture

## Overview

The Energy Capsule Charger system is built on a modular architecture with three main subsystems: Energy Capsule, Pressure Release Device (PRD), and Charging Station.

## Architecture Diagram

```
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|  Energy Capsule   |<----->|  Pressure Release |<----->|  Charging Station |
|  (Storage Unit)   |       |  Device (PRD)     |       |  (Exchange Unit)  |
|                   |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+
        |                           |                           |
        |   Solid-state cells       |   PWM control             |   Capsule handling
        |   BMS monitoring          |   Current sensing         |   Payment system
        |   Thermal sensors         |   Temperature monitoring  |   Diagnostics
        +---------------------------+---------------------------+
```

## Subsystems

### 1. Energy Capsule
- Solid-state energy cells (1.2 kWh/kg density)
- Built-in Battery Management System (BMS)
- Temperature sensors (4x NTC thermistors)
- Voltage monitoring per cell
- Secure enclosure with tamper detection
- RFID identification tag

### 2. Pressure Release Device (PRD)
- Microcontroller: ARM Cortex-M7 @ 300 MHz
- Current sensing: Hall-effect sensors (0-1000A)
- Voltage regulation: Buck-boost converter (200-800V)
- Communication: CAN bus 2.0
- Safety: Hardware watchdog, redundant cutoff relays

### 3. Charging Station
- Main controller: Raspberry Pi CM4
- Capsule handling: Robotic arm with 6 DOF
- User interface: 15.6" touchscreen
- Payment: NFC card reader + mobile app
- Network: 4G LTE + Ethernet
- Authentication: OAuth 2.0

## Communication Protocol

- CAN bus 2.0 for capsule-PRD communication (500 kbps)
- Ethernet for station backend (1 Gbps)
- WebSocket for real-time monitoring
- MQTT for IoT telemetry

## Power Flow

1. Capsule inserted into station
2. PRD authenticates capsule via RFID
3. PRD performs integrity check (2s)
4. Pressure equalization begins
5. Energy transfer at 350 kW peak
6. Transfer complete in < 3 minutes
7. PRD disconnects and vents residual pressure
8. Station releases spent capsule
