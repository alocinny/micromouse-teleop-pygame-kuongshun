# dados da esp32
ESP32_IP= "192.168.4.1"
ESP32_PORT = 4210

# URL da camera do carro
ROBOT_CAMERA_URL = f"http://{ESP32_IP}:81/stream"
ROBOT_BASE_URL = f"http://{ESP32_IP}"

# 0 -> camera principal
PC_CAMERA_INDEX = 2

DEFAULT_SPEED = 180
MIN_SPEED = 100
MAX_SPEED = 255
SPEED_STEP = 10
DEFAULT_FLASH = 0
FLASH_ON_VALUE = 120
FLASH_OFF_VALUE = 0

# tam da janela (usando pygame)
WINDOW_W = 1100
WINDOW_H = 700
FPS = 30
