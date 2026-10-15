import socket
import struct


def enviar_mensagem(sock: socket.socket, dados: bytes) -> None:
    """
    Envia 4 bytes contendo o tamanho do conteúdo em formato big-endian
    seguido pelos bytes do conteúdo (imagem).
    """
    tamanho = len(dados)
    cabecalho = struct.pack('!I', tamanho)
    sock.sendall(cabecalho + dados)


def receber_mensagem(sock: socket.socket) -> bytes:
    """
    Lê os 4 bytes do cabeçalho para obter o tamanho total e realiza
    um laço while para garantir a leitura completa de todos os bytes.
    """
    # 1. Leitura do cabeçalho (4 bytes)
    cabecalho = _receber_exatamente(sock, 4)
    if not cabecalho:
        return b""

    tamanho_esperado = struct.unpack('!I', cabecalho)[0]

    # 2. Leitura do corpo da mensagem
    return _receber_exatamente(sock, tamanho_esperado)


def _receber_exatamente(sock: socket.socket, n_bytes: int) -> bytes:
    """Função auxiliar para acumular o retorno de recv até atingir n_bytes."""
    buffer = bytearray()
    while len(buffer) < n_bytes:
        faltam = n_bytes - len(buffer)
        dados = sock.recv(faltam)
        if not dados:
            # Conexão encerrada prematuramente
            return b""
        buffer.extend(dados)
    return bytes(buffer)
