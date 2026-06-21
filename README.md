# Micromouse Teleop Pygame - KUONGSHUN AD174

Aplicação em Python com Pygame para controlar o robô KUONGSHUN AD174 / ESP32-CAM 4WD usando o firmware original do tutorial.

A versão inicial `v0.1.0` permite:

- controlar o carrinho pelo teclado;
- ajustar velocidade;
- ligar/desligar o LED da ESP32-CAM;
- visualizar a câmera do carrinho;
- visualizar a webcam do computador;
- manter uma estrutura preparada para controle por visão computacional.

## Arquitetura

```text
PC
 ├── Pygame
 │    ├── interface
 │    ├── leitura de teclado
 │    └── loop principal
 │
 ├── OpenCV
 │    ├── câmera do carrinho
 │    └── webcam do computador
 │
 └── HTTP Client
      └── envia comandos para o ESP32-CAM

Carrinho
 ├── ESP32-CAM
 ├── firmware original KUONGSHUN
 ├── servidor HTTP
 ├── stream MJPEG
 └── controle dos motores
```

## Hardware alvo

Este projeto foi feito para o kit:

```text
KUONGSHUN AD174 ESP32 WiFi Camera 4WD Smart Robot Car Kit V2.0
```

A aplicação assume o firmware web original do tutorial do carrinho.

## Rede padrão do carrinho

O firmware original cria uma rede Wi-Fi própria:

```text
SSID: KUONGSHUN-AD174
Senha: 12345678
IP do carrinho: 192.168.4.1
```

## URLs principais

Página web do carrinho:

```text
http://192.168.4.1
```

Stream da câmera:

```text
http://192.168.4.1:81/stream
```

API de controle:

```text
http://192.168.4.1/control?var=car&val=VALOR
```

## Instalação

Crie o ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

Conecte o computador à rede Wi-Fi do carrinho:

```text
KUONGSHUN-AD174
```

Depois execute:

```bash
python pc_app/main.py
```

## Controles

| Tecla | Ação |
|---|---|
| `W` ou seta cima | Frente |
| `S` ou seta baixo | Ré |
| `A` ou seta esquerda | Esquerda |
| `D` ou seta direita | Direita |
| `Espaço` | Parar |
| `+` | Aumentar velocidade |
| `-` | Diminuir velocidade |
| `L` | Liga/desliga LED |
| `C` | Liga/desliga visualização das câmeras |
| `V` | Alterna modo de visão futura |
| `ESC` | Sair |

## Estrutura do projeto

```text
pc_app/
 ├── main.py
 ├── config.py
 ├── robot_client.py
 ├── camera_viewer.py
 └── vision_controller.py
```

### `main.py`

Loop principal da aplicação Pygame.

### `config.py`

Configurações de IP, URLs, velocidade, câmera e janela.

### `robot_client.py`

Cliente HTTP para conversar com o firmware original do carrinho.

### `camera_viewer.py`

Leitura de câmera usando OpenCV e conversão para `Surface` do Pygame.

### `vision_controller.py`

Classe reservada para controle automático por visão computacional.

## Status da release v0.1.0

Esta release é focada em teleoperação manual e validação da comunicação com o carrinho real.

Ainda não inclui:

- wall follower;
- controle PID;
- odometria;
- mapeamento;
- Flood Fill;
- A*;
- ROS;
- SLAM.

Esses recursos entram nas próximas versões.
