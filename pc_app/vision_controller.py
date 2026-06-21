import cv2
import numpy as np


class VisionController:
    """
    controle automático simples usando a webcam do computador.

    estratégia:
      - detecta um alvo colorido em HSV
      - calcula o centro do maior contorno
      - decide o comando com base na posição horizontal do alvo
    """

    def __init__(
        self,
        lower_hsv,
        upper_hsv,
        min_area,
        deadzone_ratio,
        stop_area_ratio,
    ):
        self.enabled = False

        self.lower_hsv = np.array(lower_hsv, dtype=np.uint8)
        self.upper_hsv = np.array(upper_hsv, dtype=np.uint8)

        self.min_area = min_area
        self.deadzone_ratio = deadzone_ratio
        self.stop_area_ratio = stop_area_ratio

        self.last_info = {
            "detected": False,
            "command": "stop",
            "cx": None,
            "cy": None,
            "area": 0,
            "area_ratio": 0.0,
        }

    def toggle(self):
        self.enabled = not self.enabled

    def process(self, frame_bgr):
        """
        Recebe frame BGR.
        Retorna:
          command, debug_frame, info
        """
        if frame_bgr is None:
            info = self._make_info(False, "stop")
            return "stop", frame_bgr, info

        debug = frame_bgr.copy()

        height, width = frame_bgr.shape[:2]
        frame_area = width * height

        blur = cv2.GaussianBlur(frame_bgr, (5, 5), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.lower_hsv, self.upper_hsv)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        center_x = width // 2
        deadzone_px = int(width * self.deadzone_ratio)

        left_limit = center_x - deadzone_px
        right_limit = center_x + deadzone_px

        cv2.line(debug, (center_x, 0), (center_x, height), (255, 255, 255), 1)
        cv2.line(debug, (left_limit, 0), (left_limit, height), (100, 100, 100), 1)
        cv2.line(debug, (right_limit, 0), (right_limit, height), (100, 100, 100), 1)

        if not contours:
            info = self._make_info(False, "stop")
            self._draw_status(debug, info)
            return "stop", debug, info

        largest = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest)

        if area < self.min_area:
            info = self._make_info(False, "stop", area=area)
            self._draw_status(debug, info)
            return "stop", debug, info

        moments = cv2.moments(largest)

        if moments["m00"] == 0:
            info = self._make_info(False, "stop", area=area)
            self._draw_status(debug, info)
            return "stop", debug, info

        cx = int(moments["m10"] / moments["m00"])
        cy = int(moments["m01"] / moments["m00"])

        area_ratio = area / frame_area

        if area_ratio > self.stop_area_ratio:
            command = "stop"
        elif cx < left_limit:
            command = "left"
        elif cx > right_limit:
            command = "right"
        else:
            command = "forward"

        cv2.drawContours(debug, [largest], -1, (0, 255, 0), 2)
        cv2.circle(debug, (cx, cy), 6, (0, 0, 255), -1)

        info = self._make_info(
            detected=True,
            command=command,
            cx=cx,
            cy=cy,
            area=area,
            area_ratio=area_ratio,
        )

        self._draw_status(debug, info)
        self.last_info = info

        return command, debug, info

    def _make_info(
        self,
        detected,
        command,
        cx=None,
        cy=None,
        area=0,
        area_ratio=0.0,
    ):
        return {
            "detected": detected,
            "command": command,
            "cx": cx,
            "cy": cy,
            "area": int(area),
            "area_ratio": float(area_ratio),
        }

    def _draw_status(self, frame, info):
        if frame is None:
            return

        text_1 = f"vision: {'ON' if self.enabled else 'OFF'}"
        text_2 = f"detected: {info['detected']}"
        text_3 = f"cmd: {info['command']}"
        text_4 = f"area: {info['area']}"

        cv2.putText(frame, text_1, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, text_2, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, text_3, (10, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(frame, text_4, (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
