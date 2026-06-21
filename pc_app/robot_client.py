import requests

class RobotClient:
    FORWARD = 1
    RIGHT = 2
    STOP = 3
    LEFT = 4
    BACKWARD = 5

    def __init__(self, base_url: str, timeout: float = 0.2):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.last_car_command = None
        self.last_speed = None
        self.last_flash = None

    def _send_control(self, var: str, value: int) -> bool:
        url = f"{self.base_url}/control"
        params = {
            "var": var,
            "val": value,
        }

        try:
            response = requests.get(
                url,
                params=params,
                timeout=self.timeout,
            )
            return response.status_code == 200
        except requests.RequestException:
            return False

    def set_car(self, command: int) -> bool:
        if command == self.last_car_command:
            return True

        ok = self._send_control("car", command)

        if ok:
            self.last_car_command = command

        return ok

    def set_speed(self, speed: int) -> bool:
        speed = max(0, min(255, speed))

        if speed == self.last_speed:
            return True

        ok = self._send_control("speed", speed)

        if ok:
            self.last_speed = speed

        return ok

    def set_flash(self, value: int) -> bool:
        value = max(0, min(255, value))

        if value == self.last_flash:
            return True

        ok = self._send_control("flash", value)

        if ok:
            self.last_flash = value

        return ok

    def forward(self) -> bool:
        return self.set_car(self.FORWARD)

    def backward(self) -> bool:
        return self.set_car(self.BACKWARD)

    def left(self) -> bool:
        return self.set_car(self.LEFT)

    def right(self) -> bool:
        return self.set_car(self.RIGHT)

    def stop(self) -> bool:
        return self.set_car(self.STOP)

    
