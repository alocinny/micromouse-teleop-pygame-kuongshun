# Release v0.1.0 - Teleoperação inicial com Pygame

Esta é a primeira release funcional do projeto.

## Objetivo

Validar uma aplicação desktop em Python/Pygame para controlar o carrinho KUONGSHUN AD174 com ESP32-CAM usando o firmware original do tutorial.

## Funcionalidades

- Interface com Pygame.
- Controle manual por teclado.
- Comunicação HTTP com o carrinho.
- Ajuste de velocidade.
- Controle do LED.
- Visualização da câmera do carrinho.
- Visualização da webcam do computador.
- Estrutura inicial para controle automático por visão computacional.

## Requisitos

- Python 3.
- Pygame.
- OpenCV.
- NumPy.
- Requests.
- Computador conectado à rede Wi-Fi do carrinho.

## Rede padrão

```text
SSID: KUONGSHUN-AD174
Senha: 12345678
IP: 192.168.4.1
```

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python pc_app/main.py
```

## Escopo desta versão

Esta versão fecha a base de teleoperação.

Ela ainda não implementa Micromouse completo, SLAM, PID ou mapeamento.

## Próximo passo

A próxima versão deve focar em controle automático simples usando a câmera do computador.
