import re
import threading
import time

import cv2
import pygame
import numpy as np
import requests


class CameraViewer:

    def __init__(self, source):
        self.source = source

        self.is_mjpeg_url = (
            isinstance(source, str)
            and source.startswith("http")
            and "/stream" in source
        )

        self.cap = None

        self.latest_frame = None
        self.latest_frame_time = 0.0

        self.running = False
        self.thread = None
        self.lock = threading.Lock()

        self.frames_received = 0
        self.decode_errors = 0
        self.connection_errors = 0
        self.reconnects = 0

        self.max_frame_age_sec = 3.0

        if self.is_mjpeg_url:
            self._start_mjpeg_thread()
        else:
            self.cap = cv2.VideoCapture(source)

    def _start_mjpeg_thread(self):
        self.running = True
        self.thread = threading.Thread(
            target=self._mjpeg_loop,
            daemon=True,
        )
        self.thread.start()

    def _mjpeg_loop(self):
        while self.running:
            try:
                self._read_mjpeg_stream()
            except requests.RequestException:
                self.connection_errors += 1
                self.reconnects += 1
                time.sleep(0.8)
            except Exception:
                self.connection_errors += 1
                self.reconnects += 1
                time.sleep(0.8)

    def _read_mjpeg_stream(self):
        response = requests.get(
            self.source,
            stream=True,
            timeout=(3, 5),
            headers={
                "User-Agent": "micromouse-teleop-pygame",
                "Connection": "close",
            },
        )

        if response.status_code != 200:
            self.connection_errors += 1
            time.sleep(1.0)
            return

        buffer = b""

        for chunk in response.iter_content(chunk_size=4096):
            if not self.running:
                break

            if not chunk:
                continue

            buffer += chunk

            if len(buffer) > 3_000_000:
                buffer = buffer[-500_000:]

            while True:
                frame, buffer = self._extract_frame_from_buffer(buffer)

                if frame is None:
                    break

                self._store_frame(frame)

    def _extract_frame_from_buffer(self, buffer):

        header_end = buffer.find(b"\r\n\r\n")

        if header_end != -1:
            header = buffer[:header_end].decode(errors="ignore")
            content_length = self._parse_content_length(header)

            if content_length is not None:
                frame_start = header_end + 4
                frame_end = frame_start + content_length

                if len(buffer) < frame_end:
                    return None, buffer

                jpg = buffer[frame_start:frame_end]
                remaining = buffer[frame_end:]

                frame = self._decode_jpeg(jpg)
                return frame, remaining

        # Fallback: procura início e fim do JPEG.
        start = buffer.find(b"\xff\xd8")

        if start == -1:
            return None, buffer[-1024:]

        if start > 0:
            buffer = buffer[start:]

        end = buffer.find(b"\xff\xd9", 2)

        if end == -1:
            return None, buffer

        jpg = buffer[:end + 2]
        remaining = buffer[end + 2:]

        frame = self._decode_jpeg(jpg)
        return frame, remaining

    def _parse_content_length(self, header):
        match = re.search(r"Content-Length:\s*(\d+)", header, re.IGNORECASE)

        if not match:
            return None

        try:
            return int(match.group(1))
        except ValueError:
            return None

    def _decode_jpeg(self, jpg):
        if len(jpg) < 100:
            self.decode_errors += 1
            return None

        if not jpg.startswith(b"\xff\xd8"):
            self.decode_errors += 1
            return None

        if not jpg.endswith(b"\xff\xd9"):
            self.decode_errors += 1
            return None

        img_array = np.frombuffer(jpg, dtype=np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        if frame is None:
            self.decode_errors += 1
            return None

        return frame

    def _store_frame(self, frame):
        with self.lock:
            self.latest_frame = frame
            self.latest_frame_time = time.time()
            self.frames_received += 1

    def is_opened(self) -> bool:
        if self.is_mjpeg_url:
            with self.lock:
                if self.latest_frame is None:
                    return False

                age = time.time() - self.latest_frame_time

            return age <= self.max_frame_age_sec

        if self.cap is None:
            return False

        return self.cap.isOpened()

    def read_frame(self):
        if self.is_mjpeg_url:
            with self.lock:
                if self.latest_frame is None:
                    return None

                age = time.time() - self.latest_frame_time

                if age > self.max_frame_age_sec:
                    return None

                return self.latest_frame.copy()

        if self.cap is None or not self.cap.isOpened():
            return None

        ret, frame = self.cap.read()

        if not ret:
            return None

        return frame

    def frame_to_surface(self, frame, target_size=None):
        if frame is None:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if target_size is not None:
            frame_rgb = cv2.resize(frame_rgb, target_size)

        frame_rgb = np.rot90(frame_rgb)
        surface = pygame.surfarray.make_surface(frame_rgb)

        return surface

    def read_surface(self, target_size=None):
        frame = self.read_frame()
        return self.frame_to_surface(frame, target_size=target_size)

    def get_status(self):
        return {
            "frames_received": self.frames_received,
            "decode_errors": self.decode_errors,
            "connection_errors": self.connection_errors,
            "reconnects": self.reconnects,
            "opened": self.is_opened(),
        }

    def release(self):
        self.running = False

        if self.thread is not None:
            self.thread.join(timeout=1)

        if self.cap is not None:
            self.cap.release()
