# Roadmap do projeto

Este roadmap organiza a evolução do projeto desde teleoperação simples até Micromouse e conceitos de SLAM.

## v0.1.0 - Teleoperação manual

Status: implementado.

Objetivo:

```text
Controlar o carrinho real pelo PC usando Pygame.
```

Funcionalidades:

- controle manual por teclado;
- câmera do carrinho;
- câmera do computador;
- ajuste de velocidade;
- LED;
- comunicação HTTP.

## v0.2.0 - Controle automático simples por visão

Objetivo:

```text
Usar a webcam do computador para gerar comandos simples.
```

Possíveis tarefas:

- detectar objeto colorido;
- seguir alvo;
- alinhar carrinho com uma marca visual;
- parar ao perder o alvo.

## v0.3.0 - Protocolo próprio

Objetivo:

```text
Trocar HTTP por UDP ou WebSocket.
```

Motivo:

- reduzir latência;
- melhorar resposta dos comandos;
- aproximar de uma arquitetura robótica real;
- preparar integração futura com ROS.

## v0.4.0 - Sensores de parede

Objetivo:

```text
Adicionar sensores para navegação em labirinto.
```

Possíveis sensores:

- infravermelho lateral;
- infravermelho frontal;
- ultrassônico;
- ToF;
- câmera como sensor auxiliar.

## v0.5.0 - Wall Follower

Objetivo:

```text
Fazer o robô seguir parede.
```

Técnicas:

- regra da mão direita;
- regra da mão esquerda;
- controle proporcional;
- início de PID.

## v0.6.0 - Mapeamento simples

Objetivo:

```text
Representar o labirinto como matriz.
```

Estruturas:

- célula;
- paredes;
- posição atual;
- direção atual;
- células visitadas.

## v0.7.0 - Flood Fill

Objetivo:

```text
Resolver labirintos no estilo Micromouse.
```

Técnicas:

- atualização de custos;
- escolha de vizinho;
- exploração;
- segunda corrida usando mapa conhecido.

## v0.8.0 - Odometria

Objetivo:

```text
Estimar deslocamento do robô.
```

Possíveis melhorias:

- encoders;
- calibração de distância;
- calibração de giro;
- correção de erro.

## v0.9.0 - Ponte para ROS

Objetivo:

```text
Separar o projeto em blocos próximos de uma arquitetura ROS.
```

Conceitos:

- comando de velocidade;
- câmera;
- odometria;
- mapa;
- nó de controle;
- nó de visão.

## v1.0.0 - Micromouse funcional

Objetivo:

```text
Ter uma versão capaz de navegar em labirinto de forma autônoma.
```

Critérios:

- detectar paredes;
- manter posição no labirinto;
- mapear células;
- escolher caminho;
- chegar ao objetivo;
- executar movimento de forma repetível.
