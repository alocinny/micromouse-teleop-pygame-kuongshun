# Changelog

Todas as mudanças relevantes do projeto serão documentadas aqui.

O formato segue a ideia de versionamento semântico:

```text
MAJOR.MINOR.PATCH
```

## [0.2.0] - 2026-06-21

### Adicionado

- Controle do carrinho via UDP.
- Envio contínuo de comandos em taxa fixa.
- Modo de controle automático simples por visão computacional.
- Detecção de alvo por cor usando HSV.
- Conversão da posição do alvo em comandos de movimento.
- Leitor MJPEG mais robusto para a câmera ESP32-CAM.
- Reconexão automática do stream da câmera do carrinho.
- Watchdog no firmware para parar o robô caso os comandos UDP parem de chegar.

### Alterado

- Substituído o controle HTTP por controle UDP.
- Reduzida a latência dos comandos de movimentação.
- Mantida a API HTTP apenas como parte do firmware web original.
- Melhorada a estabilidade da leitura da câmera do carrinho.

### Validado

- Controle manual via Pygame.
- Controle por visão usando a câmera do computador.
- Firmware UDP na ESP32-CAM.
- Stream da câmera do carrinho em modo best effort.
- Parada automática do robô em caso de perda de comandos.

## [0.1.1] - 2026-06-21

### Corrigido

- Atualizada a API LEDC do firmware ESP32-CAM para compatibilidade com Arduino ESP32 Core 3.x.
- Substituído `ledcSetup` e `ledcAttachPin` por `ledcAttach`.
- Ajustado `ledcWrite` para usar GPIO em vez de canal.

### Validado

- Firmware compilado e gravado na ESP32-CAM.
- Aplicação Pygame testada com o robô real.
- Controle manual, câmera e comandos HTTP validados.

## [0.1.0] - 2026-06-21

### Adicionado

- Aplicação inicial com Pygame.
- Controle manual do carrinho por teclado.
- Cliente HTTP para o firmware original KUONGSHUN AD174.
- Suporte aos comandos:
  - frente;
  - ré;
  - esquerda;
  - direita;
  - parar.
- Ajuste de velocidade pela interface.
- Controle do LED da ESP32-CAM.
- Visualização da câmera do carrinho via stream MJPEG.
- Visualização da webcam do computador.
- Estrutura inicial para controle por visão computacional.
- Documentação do protocolo HTTP.
- Roadmap inicial para evolução até Micromouse.

### Limitações

- Controle ainda usa HTTP do firmware original.
- Ainda não há UDP próprio.
- Ainda não há controle autônomo por visão.
- Ainda não há sensores de parede.
- Ainda não há odometria.
- Ainda não há PID.
- Ainda não há mapeamento do labirinto.

### Objetivo da release

Validar a comunicação entre PC e carrinho real usando Pygame, HTTP e câmera em tempo real.
