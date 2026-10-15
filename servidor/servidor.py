import socket
import threading
import cv2
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../utils')))

import protocolo
from image import Imagem


class ServidorMT:
    """
    Classe Servidor MultiThread - Atendimento concorrente de processamento de imagem
    """

    def __init__(self, host: str, port: int):
        self._host = host
        self._port = port
        self.__haar_cascade_path = os.path.join(cv2.data.haarcascades,"haarcascade_frontalface_default.xml")

    def _processar_imagem(self, img_obj: Imagem) -> Imagem:
        """
        Recebe um objeto Imagem, detecta faces e desenha os retângulos verdes.
        """
        face_cascade = cv2.CascadeClassifier(self.__haar_cascade_path)
        cinza = cv2.cvtColor(img_obj.matriz, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            cinza, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )

        matriz_resultado = img_obj.matriz.copy()
        for x, y, w, h in faces:
            cv2.rectangle(
                matriz_resultado, (x, y), (x + w, y + h), (0, 255, 0), 2
            )

        return Imagem(matriz_resultado)

    def _atender_cliente(self, con: socket.socket, client_addr):
        """
        Método de atendimento individual executado dentro de cada thread.
        """
        print(f"Iniciou atendimento do cliente {client_addr}")
        try:
            # Recebe dados brutos via protocolo
            dados_recebidos = protocolo.receber_mensagem(con)
            if not dados_recebidos:
                print(f"Conexão encerrada ou vazia pelo cliente {client_addr}")
                return

            # Decodifica bytes para o objeto Imagem
            img_original = Imagem.decodificar(dados_recebidos)

            # Executa a lógica de visão computacional
            img_processada = self._processar_imagem(img_original)

            # Codifica a resposta para bytes e envia ao cliente
            dados_resposta = img_processada.codificar()
            protocolo.enviar_mensagem(con, dados_resposta)

            print(f"Terminou atendimento do cliente {client_addr}")

        except Exception as e:
            print(f"Erro ao atender cliente {client_addr}: {e}")
        finally:
            con.close()

    def start(self):
        """
        Inicializa o socket TCP, realiza a escuta e aceita conexões distribuindo para threads.
        """
        servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            servidor.bind((self._host, self._port))
            servidor.listen()
            print(f"Servidor iniciado em {self._host}:{self._port}")

            while True:
                con, client_addr = servidor.accept()
                thread = threading.Thread(
                    target=self._atender_cliente, args=(con, client_addr)
                )
                thread.start()

        except Exception as e:
            print(f"Erro na execução do servidor: {e}")
        finally:
            servidor.close()


if __name__ == "__main__":
    servidor = ServidorMT("127.0.0.1", 5000)
    servidor.start()