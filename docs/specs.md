# Technical Specifications

## Energy Capsule

| Parameter | Value | Notes |
|-----------|-------|-------|
| Capacity | 35 kWh | Usable energy |
| Energy Density | 1.2 kWh/kg | Cell level |
| Voltage Range | 200-800V | Compatible with all EVs |
| Max Discharge | 350 kW | Pulse 10s |
| Continuous Discharge | 150 kW | Sustained |
| Weight | 25 kg | Including enclosure |
| Dimensions | 400x300x200 mm | Standard form factor |
| Cycle Life | 10,000+ cycles | To 80% capacity |
| Operating Temp | -30C to +60C | Active cooling above 45C |
| Storage Temp | -40C to +85C | |
| IP Rating | IP67 | Dust/water immersion |
| Connector | CCS2 compatible | Standardized |

## Pressure Release Device (PRD)

| Parameter | Value |
|-----------|-------|
| MCU | ARM Cortex-M7 @ 300 MHz |
| ADC Resolution | 16-bit |
| Current Sensing | 0-1000A, 0.5% accuracy |
| Voltage Sensing | 0-1000V, 0.1% accuracy |
| Switching Frequency | 50 kHz |
| Efficiency | 98.5% |
| Response Time | < 100 microseconds |
| CAN Bus | CAN 2.0, 500 kbps |
| Weight | 3.5 kg |
| Dimensions | 250x180x100 mm |

## Charging Station

| Parameter | Value |
|-----------|-------|
| Exchange Time | < 3 minutes |
| Capsule Capacity | 20 capsules (on-site) |
| Power Input | 480V 3-phase AC |
| Peak Power Draw | 200 kW (charging capsules) |
| Interface | 15.6" touchscreen |
| Connectivity | 4G LTE, Ethernet, Wi-Fi 6 |
| Payment | NFC, QR, Mobile app |
| Authentication | OAuth 2.0 + RFID |
| Weight | 800 kg (empty) |
| Dimensions | 2.5 x 1.5 x 2.2 m |
