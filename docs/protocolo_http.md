# Protocolo HTTP do carrinho KUONGSHUN AD174

Este documento descreve a API HTTP usada pelo firmware web original do carrinho.

## Endereço base

```text
http://192.168.4.1
```

## Stream da câmera

```text
http://192.168.4.1:81/stream
```

O stream da câmera é usado pela aplicação Pygame/OpenCV para exibir a visão do carrinho.

## Controle dos motores

Endpoint:

```text
/control?var=car&val=VALOR
```

Exemplo:

```text
http://192.168.4.1/control?var=car&val=1
```

## Tabela de comandos

| Valor | Ação |
|---:|---|
| `1` | Frente |
| `2` | Direita |
| `3` | Parar |
| `4` | Esquerda |
| `5` | Ré |

## Controle de velocidade

Endpoint:

```text
/control?var=speed&val=VALOR
```

Exemplo:

```text
http://192.168.4.1/control?var=speed&val=180
```

Faixa usada pelo projeto:

```text
100 a 255
```

## Controle do LED

Endpoint:

```text
/control?var=flash&val=VALOR
```

Exemplo:

```text
http://192.168.4.1/control?var=flash&val=120
```

Valores usados:

| Valor | Ação |
|---:|---|
| `0` | LED desligado |
| `120` | LED ligado |

## Observações

A release `v0.1.0` usa o protocolo HTTP original do tutorial porque ele já funciona no carrinho real.

Futuramente, o projeto pode migrar para um protocolo UDP próprio para reduzir latência e melhorar o controle em tempo real.
