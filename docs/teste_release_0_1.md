# Checklist de teste - Release v0.1.0

Use este documento antes de criar a release no GitHub.

## 1. Ambiente Python

- [ ] Ambiente virtual criado.
- [ ] Dependências instaladas.
- [ ] Aplicação inicia sem erro.

Comandos:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python pc_app/main.py
```

## 2. Rede

- [ ] PC conectado à rede `KUONGSHUN-AD174`.
- [ ] IP `192.168.4.1` acessível.
- [ ] Página web do carrinho abre no navegador.

Teste:

```text
http://192.168.4.1
```

## 3. Câmera do carrinho

- [ ] Stream abre no navegador.
- [ ] Stream aparece na aplicação Pygame.

Teste:

```text
http://192.168.4.1:81/stream
```

## 4. Webcam do computador

- [ ] Webcam aparece na aplicação Pygame.
- [ ] Aplicação não trava se a webcam estiver indisponível.

## 5. Controle manual

- [ ] `W` move para frente.
- [ ] `S` move para trás.
- [ ] `A` vira para esquerda.
- [ ] `D` vira para direita.
- [ ] `Espaço` para o robô.
- [ ] `ESC` fecha aplicação e envia comando de parada.

## 6. Velocidade

- [ ] `+` aumenta velocidade.
- [ ] `-` diminui velocidade.
- [ ] Valor de velocidade respeita mínimo e máximo.

## 7. LED

- [ ] `L` liga o LED.
- [ ] `L` desliga o LED.
- [ ] LED desliga ao fechar a aplicação.

## 8. Segurança básica

- [ ] Robô para ao fechar a janela.
- [ ] Robô para ao pressionar `ESC`.
- [ ] Robô não continua andando após encerrar o programa normalmente.

## 9. Documentação

- [ ] README atualizado.
- [ ] CHANGELOG atualizado.
- [ ] RELEASE_NOTES atualizado.
- [ ] Roadmap criado.
- [ ] Protocolo HTTP documentado.

## Resultado

Se todos os itens críticos foram validados, a release `v0.1.0` pode ser criada.
