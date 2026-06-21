import socket
import threading
import time


class RobotClient:
    """
    manda comandos em taxa fixa, formato:

        V:<linear>,W:<angular>,F:<flash>
    """

    def __init__(
        self,
        base_url=None,
        robot_ip="192.168.4.1",
        udp_port=4210,
        send_hz=20,
    ):
        self.robot_ip = robot_ip
        self.udp_port = udp_port
        self.address = (robot_ip, udp_port)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.send_period = 1.0 / send_hz

        self.speed = 180
        self.flash = 0

        self.linear = 0
        self.angular = 0

        self.running = True
        self.lock = threading.Lock()

        self.thread = threading.Thread(
            target=self._send_loop,
            daemon=True,
        )
        self.thread.start()

    def _send_loop(self):
        while self.running:
            with self.lock:
                linear = self.linear
                angular = self.angular
                flash = self.flash

            message = f"V:{linear},W:{angular},F:{flash}"

            try:
                self.sock.sendto(message.encode("utf-8"), self.address)
            except OSError:
                pass

            time.sleep(self.send_period)

    def _set_motion(self, linear: int, angular: int) -> bool:
        with self.lock:
            self.linear = int(max(-255, min(255, linear)))
            self.angular = int(max(-255, min(255, angular)))

        return True

    def set_speed(self, speed: int) -> bool:
        with self.lock:
            self.speed = int(max(0, min(255, speed)))

        return True

    def set_flash(self, value: int) -> bool:
        with self.lock:
            self.flash = int(max(0, min(255, value)))

        return True

    def forward(self) -> bool:
        with self.lock:
            speed = self.speed

        return self._set_motion(speed, 0)

    def backward(self) -> bool:
        with self.lock:
            speed = self.speed

        return self._set_motion(-speed, 0)

    def left(self) -> bool:
        with self.lock:
            speed = self.speed

        return self._set_motion(0, -speed)

    def right(self) -> bool:
        with self.lock:
            speed = self.speed

        return self._set_motion(0, speed)

    def stop(self) -> bool:
        return self._set_motion(0, 0)

    def close(self):
        self.stop()
        time.sleep(0.05)

        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=1)

        self.sock.close()
