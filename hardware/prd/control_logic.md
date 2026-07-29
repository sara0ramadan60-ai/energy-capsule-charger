# PRD Control Logic

## State Machine

```
         +---------+
         |  IDLE   |<---------+
         +----+----+          |
              |               |
         Capsule inserted     |
              |               |
         +----v----+          |
         |  AUTH   |          |
         +----+----+          |
              |               |
         Auth success         |
              |               |
         +----v----+          |
         |  CHECK  |          |
         +----+----+          |
              |               |
         Check passed         |
              |               |
         +----v----+          |
         | CHARGE  |----------+ (Complete)
         +----+----+          |
              |               |
         +----v----+          |
         |  VENT   |----------+
         +----+----+
              |
         +----v----+
         |  IDLE   |
         +---------+
```

Any state can transition to FAULT on error.

## Control Algorithm

### Current Control
```python
# PI controller with anti-windup
error = target_current - measured_current
integral += error * dt * ki
output = error * kp + integral
output = clamp(output, -1.0, 1.0)
```

### Temperature Derating
```python
# Linear derating above 85C
if temp > 85:
    power_limit = 1.0 - (temp - 85) / 35  # 0 at 120C
else:
    power_limit = 1.0
```

### Fault Detection
- Watchdog: 1s timeout, hardware reset
- Overcurrent: 600A threshold, 10us response
- Overtemp: 120C critical, immediate shutdown
- Overpressure: 2.5 bar threshold, vent open
- Communication: CAN heartbeat every 100ms
