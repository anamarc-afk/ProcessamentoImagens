from cliente import Cliente

CAMINHO_IMAGEM = 'D:\\Users\\dias.jordan\\Documents\\ProcessamentoImagens\\testes\\image_0001.jpg'  # Ajuste para o caminho da sua imagem

c = Cliente("127.0.0.1", 5000)
c.start(CAMINHO_IMAGEM)
