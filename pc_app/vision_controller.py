class VisionController:
    """
    Classe reservada para controle automático baseado na câmera do computador.

    No futuro:
      - detectar linha
      - detectar cor
      - detectar posição do robô
      - gerar comando de movimento
    """

    def __init__(self):
        self.enabled = False

    def toggle(self):
        self.enabled = not self.enabled

    def process(self, frame):
        """
        futuramente retorna uma ação:
          "forward"
          "left"
          "right"
          "backward"
          "stop"
        """
        return "stop"
