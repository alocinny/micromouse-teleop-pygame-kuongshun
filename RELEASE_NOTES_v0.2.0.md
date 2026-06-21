# v0.2.0 - Controle por visão com transporte UDP

Esta release evolui a aplicação de teleoperação para uma arquitetura mais adequada para robótica em tempo real.

## Principais mudanças

- Substituição do controle HTTP por controle UDP.
- Redução perceptível da latência dos comandos.
- Envio contínuo de comandos em taxa fixa.
- Watchdog no firmware para parar o robô caso a comunicação seja perdida.
- Modo de controle automático simples usando a câmera do computador.
- Detecção de alvo colorido em HSV.
- Visualização da câmera do carrinho mantida como monitoramento.
- Leitor MJPEG mais robusto, com reconexão automática.

## Arquitetura atual

```text
PC
 ├── Pygame
 ├── OpenCV
 ├── câmera do computador
 ├── controle manual
 ├── controle por visão
 └── comandos UDP

ESP32-CAM
 ├── firmware web
 ├── stream MJPEG
 ├── servidor HTTP original
 ├── receptor UDP
 ├── controle dos motores
 └── watchdog de segurança
```

## Validação

Esta versão foi testada com o robô real.

Foram validados:

- movimentação manual com menor latência;
- modo visão usando câmera do computador;
- envio de comandos UDP;
- parada por timeout;
- stream da câmera do carrinho com reconexão no app.

## Limitações conhecidas

- A câmera ESP32-CAM ainda pode apresentar glitches em MJPEG.
- O stream da câmera do carrinho deve ser tratado como monitoramento best effort.
- A navegação ainda não é Micromouse completa.
- Ainda não há sensores de parede, odometria, PID, mapeamento ou Flood Fill.
- Próximos passos
- Melhorar a calibração HSV.
- Criar ferramenta de calibração visual.
- Adicionar sensores de parede.
- Iniciar Wall Follower.
- Preparar a base para odometria e controle PID.
