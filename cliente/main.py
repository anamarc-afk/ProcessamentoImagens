from cliente import Cliente

CAMINHO_IMAGEM = 'imagem.jpg'  # Ajuste para o caminho da sua imagem

c = Cliente("127.0.0.1", 50000)
c.start(CAMINHO_IMAGEM)
