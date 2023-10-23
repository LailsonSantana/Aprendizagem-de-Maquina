import os
from PIL import Image
from PIL import ImageFilter
import numpy as np

# Diretório que contém as imagens
diretorio = "Img/"

# Lista para armazenar as imagens
imagens = []

# Percorra todos os arquivos na pasta
for nome_arquivo in os.listdir(diretorio):
    caminho_completo = os.path.join(diretorio, nome_arquivo)

    # Verifique se o arquivo é uma imagem (você pode adicionar mais extensões de arquivo, se necessário)
    if nome_arquivo.endswith(('.jpg', '.jpeg', '.png', '.gif')):
        try:
            imagem = Image.open(caminho_completo)
            imagens.append(imagem)
        except Exception as e:
            print(f"Erro ao abrir a imagem {caminho_completo}: {str(e)}")

# Agora, a lista "imagens" contém todas as imagens da pasta
cont = 0
for imagem in imagens:
    cont = cont + 1
    #Redimensiona Imagem
    nova_imagem = imagem.resize((224, 224))
    #Transforma RGB
    imagem_rgb = nova_imagem.convert("RGB")
    #Suaviza para eliminar ruído
    imagem_suavizada = imagem_rgb.filter(ImageFilter.MedianFilter(size=3))
    #Faz a normalização
    imagem_suavizada = np.array(imagem_suavizada)
    
    imagem_normalizada = (imagem_suavizada - imagem_suavizada.min()) / (imagem_suavizada.max() - imagem_suavizada.min())
    #Salvar Imagem
    imagem_desnormalizada = (imagem_normalizada * 255).astype(np.uint8)
    imagem_pillow = Image.fromarray(imagem_desnormalizada)
    
    imagem_pillow.save("imagem" + str(cont) + ".jpg")













