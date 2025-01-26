import glob
import os

import cv2

files = glob.glob("bd_filtered/*")
for f in files:
    image_f = cv2.imread(f)
    if image_f is None:
        print(f"Erro ao carregar a imagem {f}")
        continue

    # Redimensiona a imagem
    image_resized = cv2.resize(image_f, (550, 220))
    
    # Cortar 15 pixels do topo, 15 pixels da parte inferior, 10 pixels do lado esquerdo e 10 pixels do lado direito
    image_cropped = image_resized[10:-10, 5:-5]  # Cropping

    # Converte para escala de cinza
    image = cv2.cvtColor(image_cropped, cv2.COLOR_RGB2GRAY)
    _, new_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV)

    # Detecta contornos
    contours, _ = cv2.findContours(new_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    letter_area = []
    for c in contours:
        area = cv2.contourArea(c)
        if 50 < area < 2000:
            (x, y, w, h) = cv2.boundingRect(c)
            # Adiciona padding ao redor de cada contorno
            padding = 20
            letter_area.append((x - padding, y - padding, w + 2 * padding, h + 2 * padding))

    # Verifica se temos contornos suficientes
    if len(letter_area) < 5:
        print(f"Imagem {f} ignorada: apenas {len(letter_area)} contornos válidos encontrados.")
        continue

    final_image = cv2.merge([image] * 3)
    for i, (x, y, w, h) in enumerate(letter_area, start=1):
        # Recorta a imagem da letra isolada com padding
        padded_image_letter = image[max(0, y): min(y + h, image.shape[0]), max(0, x): min(x + w, image.shape[1])]
        cv2.imwrite(f"letter_field/{os.path.basename(f).replace('png', f'letra{i}.png')}", padded_image_letter)

    for (x, y, w, h) in letter_area:
        cv2.rectangle(final_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(f"identified/{os.path.basename(f)}", final_image)