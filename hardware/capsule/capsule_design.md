# Energy Capsule Design

## Mechanical Design

### Enclosure
- Material: 6061-T6 aluminum with steel reinforcement
- Sealing: Dual O-ring IP67 rated
- Cooling: Passive heat sink fins + phase change material
- Handle: Ergonomic, integrated grip
- Color: High-visibility yellow with reflective strips

### Internal Layout
```
+--------------------------------------------------+
|  [RFID Tag]  [BMS PCB]  [Status LED]             |
|  +-------+  +-------+  +-------+  +-------+     |
|  | Cell 1|  | Cell 2|  | Cell 3|  | Cell 4|     |
|  +-------+  +-------+  +-------+  +-------+     |
|  +-------+  +-------+  +-------+  +-------+     |
|  | Cell 5|  | Cell 6|  | Cell 7|  | Cell 8|     |
|  +-------+  +-------+  +-------+  +-------+     |
|  [Thermal Pad]  [Phase Change Material]          |
|  [Pressure Relief Valve]  [Connector]            |
+--------------------------------------------------+
```

### Cell Configuration
- 8 cells in 2P4S configuration
- Individual cell monitoring
- Passive cell balancing (100mA)
- Mica sheet insulation between cells

### Connector
- Type: Modified CCS2
- Pins: Power (2), Signal (4), Ground (2)
- Rating: 1000V, 500A continuous
- Cycle life: 50,000 matings
- Locking: Electromechanical with manual release

## BMS Specifications

| Feature | Detail |
|---------|--------|
| MCU | TI BQ79600-Q1 |
| Monitoring | Voltage, current, temp per cell |
| Balancing | Passive, 100mA |
| Communication | CAN 2.0, SPI |
| Isolation | 5 kV optocoupler |
| Shutdown | Independent hardware path |
