import pygame

from config import (
    ROBOT_BASE_URL,
    ROBOT_CAMERA_URL,
    PC_CAMERA_INDEX,
    WINDOW_W,
    WINDOW_H,
    FPS,
    DEFAULT_SPEED,
    MIN_SPEED,
    MAX_SPEED,
    SPEED_STEP,
    FLASH_ON_VALUE,
    FLASH_OFF_VALUE,
)

from robot_client import RobotClient
from camera_viewer import CameraViewer
from vision_controller import VisionController


def draw_text(screen, text, x, y, font, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def get_manual_command(keys):
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        return "forward"

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        return "backward"

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        return "left"

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        return "right"

    if keys[pygame.K_SPACE]:
        return "stop"

    return "stop"


def send_robot_command(robot, command):
    if command == "forward":
        return robot.forward()

    if command == "backward":
        return robot.backward()

    if command == "left":
        return robot.left()

    if command == "right":
        return robot.right()

    return robot.stop()


def main():
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Micromouse Teleop - KUONGSHUN AD174")

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("monospace", 24)
    small_font = pygame.font.SysFont("monospace", 17)

    robot = RobotClient(ROBOT_BASE_URL)

    robot_camera = CameraViewer(ROBOT_CAMERA_URL)
    pc_camera = CameraViewer(PC_CAMERA_INDEX)

    vision = VisionController()

    speed = DEFAULT_SPEED
    flash_enabled = False
    cameras_enabled = True
    running = True

    last_command = None
    connection_ok = True

    robot.set_speed(speed)
    robot.set_flash(FLASH_OFF_VALUE)
    robot.stop()

    try:
        while running:
            clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                    elif event.key == pygame.K_c:
                        cameras_enabled = not cameras_enabled

                    elif event.key == pygame.K_v:
                        vision.toggle()

                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS, pygame.K_KP_PLUS):
                        speed = min(MAX_SPEED, speed + SPEED_STEP)
                        connection_ok = robot.set_speed(speed)

                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        speed = max(MIN_SPEED, speed - SPEED_STEP)
                        connection_ok = robot.set_speed(speed)

                    elif event.key == pygame.K_l:
                        flash_enabled = not flash_enabled

                        if flash_enabled:
                            connection_ok = robot.set_flash(FLASH_ON_VALUE)
                        else:
                            connection_ok = robot.set_flash(FLASH_OFF_VALUE)

            keys = pygame.key.get_pressed()

            command = get_manual_command(keys)

            if vision.enabled:
                # ainda não usa controle automático
                command = "stop"

            if command != last_command:
                connection_ok = send_robot_command(robot, command)
                last_command = command

            screen.fill((20, 20, 20))

            draw_text(screen, "Micromouse Teleop - KUONGSHUN AD174", 20, 20, font)

            draw_text(screen, f"Robot URL: {ROBOT_BASE_URL}", 20, 65, small_font)
            draw_text(screen, f"Camera URL: {ROBOT_CAMERA_URL}", 20, 90, small_font)
            draw_text(screen, f"Velocidade: {speed}", 20, 125, small_font)
            draw_text(screen, f"Comando: {command}", 20, 150, small_font)
            draw_text(screen, f"LED: {'ON' if flash_enabled else 'OFF'}", 20, 175, small_font)
            draw_text(screen, f"Cameras: {'ON' if cameras_enabled else 'OFF'}", 20, 200, small_font)
            draw_text(screen, f"Modo visao: {'ON' if vision.enabled else 'OFF'}", 20, 225, small_font)

            if connection_ok:
                draw_text(screen, "Conexao: OK", 20, 260, small_font, color=(120, 255, 120))
            else:
                draw_text(screen, "Conexao: FALHA", 20, 260, small_font, color=(255, 120, 120))

            draw_text(screen, "Controles", 20, 320, small_font)
            draw_text(screen, "W / seta cima      -> frente", 20, 350, small_font)
            draw_text(screen, "S / seta baixo     -> re", 20, 375, small_font)
            draw_text(screen, "A / seta esquerda  -> esquerda", 20, 400, small_font)
            draw_text(screen, "D / seta direita   -> direita", 20, 425, small_font)
            draw_text(screen, "Espaco             -> parar", 20, 450, small_font)
            draw_text(screen, "+ / -              -> velocidade", 20, 475, small_font)
            draw_text(screen, "L                  -> LED", 20, 500, small_font)
            draw_text(screen, "C                  -> cameras", 20, 525, small_font)
            draw_text(screen, "V                  -> modo visao futuro", 20, 550, small_font)
            draw_text(screen, "ESC                -> sair", 20, 575, small_font)

            if cameras_enabled:
                robot_surface = robot_camera.read_surface(target_size=(480, 320))

                if robot_surface is not None:
                    screen.blit(robot_surface, (560, 60))
                    draw_text(screen, "Camera do carrinho", 560, 390, small_font)
                else:
                    draw_text(
                        screen,
                        "Camera do carrinho indisponivel",
                        560,
                        100,
                        small_font,
                        color=(255, 120, 120),
                    )

                pc_surface = pc_camera.read_surface(target_size=(320, 220))

                if pc_surface is not None:
                    screen.blit(pc_surface, (560, 430))
                    draw_text(screen, "Camera do computador", 560, 660, small_font)
                else:
                    draw_text(
                        screen,
                        "Camera do computador indisponivel",
                        560,
                        470,
                        small_font,
                        color=(255, 120, 120),
                    )

            pygame.display.flip()

    finally:
        robot.stop()
        robot.set_flash(FLASH_OFF_VALUE)
        robot_camera.release()
        pc_camera.release()
        pygame.quit()


if __name__ == "__main__":
    main()
