import socket
import cv2
from imagem import Imagem
import protocolo


class Cliente:
    """
    Classe Cliente - Comunicação via Socket para Envio e Exibição de Imagens
    """

    def __init__(self, server_ip: str, port: int):
        self.__server_ip = server_ip
        self.__port = port

    def start(self, caminho_imagem: str = 'imagem.jpg'):
        """
        Carrega a imagem, envia para o servidor via protocolo,
        recebe a imagem processada e exibe na janela do OpenCV.
        """
        # Carrega e codifica a imagem em JPEG usando a classe Imagem
        img_obj = Imagem.ler(caminho_imagem)
        if img_obj.matriz is None:
            print(f"Erro ao carregar a imagem do caminho: {caminho_imagem}")
            return

        bytes_imagem = img_obj.codificar()

        # Conecta ao servidor TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        endpoint = (self.__server_ip, self.__port)

        try:
            sock.connect(endpoint)
            print(f"Conectado ao servidor {self.__server_ip}:{self.__port}")

            # Envia o cabeçalho com o tamanho e os bytes da imagem
            protocolo.enviar_mensagem(sock, bytes_imagem)
            print("Imagem enviada com sucesso. Aguardando resposta do servidor...")

            # Recebe a resposta do servidor em bytes
            bytes_resposta = protocolo.receber_mensagem(sock)

            if bytes_resposta:
                # Decodifica os bytes recebidos
                img_processada = Imagem.decodificar(bytes_resposta)

                # Exibe a janela com o resultado
                cv2.imshow("Resultado - Detecção de Faces",
                           img_processada.matriz)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print("Erro: Resposta vazia ou falha na leitura pelo servidor.")

        except Exception as e:
            print(f"Erro na comunicação com o servidor: {e}")
        finally:
            # Fecha o socket após o término da comunicação
            sock.close()
            print("Conexão encerrada.")
