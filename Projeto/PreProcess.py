import os
import numpy as np
import matplotlib.pyplot as plt 
from skimage import data
from PIL import Image
import math

# Diretório que contém as imagens
diretorio = "img/"
diretorio_saida = "img_processada"

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

# função de conversão de cor
def convert_to_gray(image, luma=False):
    image_array = np.array(image)  # Converte a imagem em uma matriz NumPy
    if luma:
        params = [0.299, 0.589, 0.114]
    else:
        params = [0.2125, 0.7154, 0.0721]    
    gray_image = np.ceil(np.dot(image_array[...,:3], params))
 
    # Saturando os valores em 255
    gray_image[gray_image > 255] = 255
    
    return gray_image

def instantiate_histogram():    
    hist_array= []
    
    for i in range(0,256):
        hist_array.append(str(i))
        hist_array.append(0)
    
    hist_dct = {hist_array[i]: hist_array[i + 1] for i in range(0, len(hist_array), 2)} 
    
    return hist_dct

def count_intensity_values(hist, img):
    #image_array = np.array(img)
    for row in img:
        for column in row:
            hist[str(int(column))] = hist[str(int(column))] + 1
     
    return hist

# Comparacao de dois histogramas
def plot_hist(hist, hist2=''):
    if hist2 != '':
        figure, axarr = plt.subplots(1,2, figsize=(20, 10))
        axarr[0].bar(hist.keys(), hist.values())
        axarr[1].bar(hist2.keys(), hist2.values())
    else:
        plt.bar(hist.keys(), hist.values())
        plt.xlabel("Níveis intensidade")
        ax = plt.gca()
        ax.axes.xaxis.set_ticks([])
        plt.grid(True)
        plt.show()

def get_hist_proba(hist, n_pixels):
    hist_proba = {}
    for i in range(0, 256):
        hist_proba[str(i)] = hist[str(i)] / n_pixels
    
    return hist_proba

def get_accumulated_proba(hist_proba): 
    acc_proba = {}
    sum_proba = 0
    
    for i in range(0, 256):
        if i == 0:
            pass
        else: 
            sum_proba += hist_proba[str(i - 1)]
            
        acc_proba[str(i)] = hist_proba[str(i)] + sum_proba
        
    return acc_proba

def get_new_gray_value(acc_proba):
    new_gray_value = {}
    
    for i in range(0, 256):
        new_gray_value[str(i)] = np.ceil(acc_proba[str(i)] * 255)
    
    return new_gray_value

def equalize_hist(img, new_gray_value):
    for row in range(img.shape[0]):
        for column in range(img.shape[1]):
            img[row][column] = new_gray_value[str(int(img[row] [column]))]
            
    return img

# Agora, a lista "imagens" contém todas as imagens da pasta
cont = 0
for imagem in imagens:
    cont = cont + 1
    # Redimensiona a imagem
    nova_imagem = imagem.resize((3560, 3269))

    # Converte a imagem para tons de cinza usando a função
    image_cinza = convert_to_gray(nova_imagem)

    histogram = instantiate_histogram()
    
    histogram = count_intensity_values(histogram, image_cinza)
    
    n_pixels = image_cinza.shape[0] * image_cinza.shape[1]
    hist_proba = get_hist_proba(histogram, n_pixels)
    
    accumulated_proba = get_accumulated_proba(hist_proba)
    
    new_gray_value = get_new_gray_value(accumulated_proba)
    
    eq_img = equalize_hist(image_cinza.copy(), new_gray_value)
    
    figure, axarr = plt.subplots(1,2, figsize=(20, 10))
    axarr[0].imshow(image_cinza, cmap='gray')
    axarr[1].imshow(eq_img, cmap='gray')
    
    # Exibe a imagem em tons de cinza
    plt.imshow(image_cinza, cmap='gray')
    plt.show()

    # Salva a imagem em tons de cinza
    caminho_saida = os.path.join(diretorio_saida, "imagem" + str(cont) + ".jpg")
    
    # Crie uma imagem do Pillow a partir da matriz NumPy
    imagem_pillow = Image.fromarray(eq_img.astype(np.uint8))
    imagem_pillow.save(caminho_saida)