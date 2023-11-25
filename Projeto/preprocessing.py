import os
import cv2
import numpy as np


def padronizar_dimensoes(imagem, largura, altura):
    return cv2.resize(imagem, (largura, altura))


def normalizar_cores(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def remover_ruidos(imagem):
    row, col = 1, 1
    return cv2.GaussianBlur(imagem, (row, col), 0)


def augmentacao_dados(imagem):
    return cv2.rotate(imagem, cv2.ROTATE_90_CLOCKWISE)


def ajuste_exposicao_contraste(imagem):
    alpha, beta = 1.2, 1.1
    return cv2.convertScaleAbs(imagem, alpha=alpha, beta=beta)


def equalizacao_histograma(imagem):
    return cv2.equalizeHist(imagem)


def filtragem_bordas(imagem):
    return cv2.Laplacian(imagem, cv2.CV_64F)


def segmentacao(imagem, limiar):
    _, imagem_segmentada = cv2.threshold(imagem, limiar, 255, cv2.THRESH_BINARY)
    return imagem_segmentada


def remover_artefatos(imagem):
    return cv2.medianBlur(imagem, 1)


# Diretório que contém as imagens
diretorio = "img"
try:
    # Listar todos os arquivos no diretório das imagens
    for nome_arquivo in os.listdir(diretorio):
        caminho_arquivo = os.path.join(diretorio, nome_arquivo)
        # Agora você tem o caminho completo para cada arquivo de imagem
        print(caminho_arquivo)  # Isto é apenas para teste, para mostrar o caminho do arquivo
        # Aqui você processaria o arquivo
except FileNotFoundError:
    print(f"Não foi possível encontrar o diretório: {diretorio}")

# Lista para armazenar as imagens
imagens = []

# Percorra todos os arquivos na pasta
for nome_arquivo in os.listdir( diretorio):
    caminho_completo = os.path.join( diretorio, nome_arquivo)
    if nome_arquivo.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        try:
            imagem = cv2.imread(caminho_completo)
            largura, altura = 256, 256

            # padronizar dimensoes
            imagem = padronizar_dimensoes(imagem, largura, altura)
            # preto e branco
            imagem = normalizar_cores(imagem)
            # desfoque gausiano na imagem
            imagem = remover_ruidos(imagem)
            # rotacionar imagem
            # imagem = augmentacao_dados(imagem)
            # contraste
            imagem = ajuste_exposicao_contraste(imagem)
            # equalizar os valores dos pixels na imagem
            imagem = equalizacao_histograma(imagem)
            # outro desfoque, so q mediano
            imagem = remover_artefatos(imagem)
            # atribui um valor binario a cada pixel dependendo de um threshhold
            imagem = segmentacao(imagem, 164)
            # deixa os pixels q representam as "bordas" de um objeto
            imagem = filtragem_bordas(imagem)

            imagens.append(imagem)
        except Exception as e:
            print(f"Erro ao abrir a imagem {caminho_completo}: {str(e)}")

# salvar as imagens processadas
novo_diretorio = "\\img_processada"

if not os.path.exists(novo_diretorio):
    os.makedirs(novo_diretorio)

i = 0
for img in imagens:
    caminho_imagem = os.path.join(novo_diretorio, 'imagem_processada_' + str(i) + '.jpg')
    cv2.imwrite(caminho_imagem, img)
    i += 1
