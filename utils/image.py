import cv2
import numpy as np


class Imagem:
    """
    Classe para manipular a matriz de pixels e codificação/decodificação JPEG.
    A classe não realiza operações de rede.
    """

    def __init__(self, matriz):
        self.matriz = matriz

    @classmethod
    def ler(cls, caminho: str):
        """Lê um arquivo de imagem do disco e retorna uma instância de Imagem."""
        matriz = cv2.imread(caminho)
        return cls(matriz)

    def codificar(self) -> bytes:
        """Codifica a matriz de pixels em um array de bytes no formato JPEG."""
        if self.matriz is None:
            return b""
        sucesso, buffer = cv2.imencode('.jpg', self.matriz)
        if not sucesso:
            raise ValueError("Falha ao codificar a imagem em JPEG.")
        return buffer.tobytes()

    @classmethod
    def decodificar(cls, dados_bytes: bytes):
        """Decodifica um array de bytes JPEG e retorna uma instância de Imagem."""
        nparr = np.frombuffer(dados_bytes, np.uint8)
        matriz = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return cls(matriz)
