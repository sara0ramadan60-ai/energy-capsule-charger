# Pressure Release Device (PRD) Overview

## Purpose

The PRD is a safety-critical subsystem that controls the energy flow between the capsule and the vehicle. It prevents dangerous pressure buildup, thermal runaway, and electrical faults during the high-speed energy transfer.

## Block Diagram

```
+------------+     +------------+     +------------+
| Capsule    |<--->| Power Stage|<--->| Vehicle    |
| Interface  |     | (Buck-Boost|     | Interface  |
|            |     |  350kW)    |     |            |
+------------+     +------------+     +------------+
       |                  |                  |
       v                  v                  v
+------------+     +------------+     +------------+
| Safety MCU |<--->| Main MCU   |<--->| CAN Bus    |
| (Cortex-M7)|     | (Cortex-M7)|     | Transceiver|
+------------+     +------------+     +------------+
       |
       v
+------------+
| Watchdog   |
| + Cutoff   |
| Relays     |
+------------+
```

## Key Components

### Power Stage
- IGBT modules (6x, 600A/1200V each)
- Gate drivers with desaturation protection
- DC link capacitor bank (10mF)
- LCL filter for EMI suppression

### Control System
- Main MCU: STM32H743 (Cortex-M7, 300 MHz)
- Safety MCU: TI TMS570LS (lockstep ARM)
- ADC: 16-bit, 8-channel simultaneous sampling
- PWM: 16-channel, 50 kHz switching

### Sensors
- Current: LEM HASS 600-S (Hall-effect, 600A)
- Voltage: ISO224 isolation amplifier
- Temperature: 4x PT100 RTD, 4x NTC
- Pressure: 2x MEMS pressure sensor

## Operation Modes

| Mode | Description |
|------|-------------|
| IDLE | No capsule, all circuits de-energized |
| AUTH | Capsule detected, authentication in progress |
| CHECK | Integrity check, contactor test |
| CHARGE | Energy transfer active |
| VENT | Pressure release, cooldown |
| FAULT | Safety shutdown, error reporting |
