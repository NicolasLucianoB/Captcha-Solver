import cv2
from PIL import Image

metodos = [cv2.THRESH_BINARY,
           cv2.THRESH_BINARY_INV,
           cv2.THRESH_TRUNC,
           cv2.THRESH_TOZERO,
           cv2.THRESH_TOZERO_INV]

imagem = cv2.imread('capchas/img1.png', cv2.IMREAD_GRAYSCALE)
# 2 e 4 são melhores aparentemente

i = 0 

for metodo in metodos:
    i += 1
    _, imagem_tratada = cv2.threshold(imagem, 127, 255, metodo or cv2.THRESH_OTSU)
    cv2.imshow('imagem', imagem_tratada)
    cv2.imwrite(f'teste_metodo/imagem_tratada_{i}.png', imagem_tratada)
    
    
    # Kinda useless
imagem = Image.open ("teste_metodo/imagem_tratada_2.png")
imagem = imagem.convert("L")
imagem2 = Image.new("L", imagem.size, 255)

for x in range (imagem.size [1]):
  for y in range (imagem.size[0]):
    cor_pixel = imagem. getpixel((y, x))
    if cor_pixel < 115:
      imagem2. putpixel((y, x), 0)

imagem2.save("teste_metodo/imagem_final.png")