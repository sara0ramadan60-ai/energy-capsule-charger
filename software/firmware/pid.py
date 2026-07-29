"""
PID controller implementation for PRD current control.
"""


class PIDController:
    def __init__(
        self,
        kp: float = 0.8,
        ki: float = 0.1,
        kd: float = 0.05,
        integral_limit: float = 100.0,
        output_limit: float = 1.0,
    ):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_limit = integral_limit
        self.output_limit = output_limit

        self._integral = 0.0
        self._prev_error = 0.0
        self._dt = 0.001

    def set_dt(self, dt: float):
        self._dt = dt

    def compute(self, setpoint: float, measurement: float) -> float:
        error = setpoint - measurement

        self._integral += error * self._dt
        self._integral = max(
            -self.integral_limit,
            min(self.integral_limit, self._integral),
        )

        derivative = (error - self._prev_error) / self._dt
        self._prev_error = error

        output = (
            self.kp * error
            + self.ki * self._integral
            + self.kd * derivative
        )

        return max(-self.output_limit, min(self.output_limit, output))

    def reset(self):
        self._integral = 0.0
        self._prev_error = 0.0
