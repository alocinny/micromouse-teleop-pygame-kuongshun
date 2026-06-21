# Changelog

Todas as mudanças relevantes do projeto serão documentadas aqui.

O formato segue a ideia de versionamento semântico:

```text
MAJOR.MINOR.PATCH
```

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
