import os
import pickle

import cv2
import numpy as np
import tensorflow as tf
from imutils import paths
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.layers import Conv2D, Dense, Flatten, MaxPooling2D
from tensorflow.keras.models import Sequential


def resize_image(image, width, height):
    """Função para redimensionar a imagem, mantendo a proporção."""
    try:
        resized_image = cv2.resize(image, (width, height))
        return resized_image
    except cv2.error as e:
        print(f"Erro ao redimensionar a imagem: {e}")
        return None

def load_and_preprocess_images(base_letters_file):
    """Função para carregar, processar e redimensionar as imagens."""
    datas = []
    labels = []

    images = paths.list_images(base_letters_file)

    for f in images:
        label = f.split(os.path.sep)[-2]
        
        try:
            # Ler a imagem
            image = cv2.imread(f)
            if image is None:
                print(f"Erro ao ler a imagem {f}")
                continue
            
            # Converter para escala de cinza
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Redimensionar para 127x127
            image_resized = resize_image(image, 127, 127)
            if image_resized is None:
                print(f"Erro ao redimensionar a imagem {f}")
                continue

            # Adicionar a dimensão de canal
            image_resized = np.expand_dims(image_resized, axis=-1)

            datas.append(image_resized)
            labels.append(label)
        
        except Exception as e:
            print(f"Erro ao processar a imagem {f}: {e}")
    
    datas = np.array(datas)
    labels = np.array(labels)
    
    if len(datas) == 0 or len(labels) == 0:
        raise ValueError("Nenhuma imagem válida foi carregada para o treinamento.")
    
    return datas, labels

def prepare_data(datas, labels):
    """Função para normalizar e dividir os dados em treino e teste."""
    # Normalizar as imagens
    datas = datas.astype("float32") / 255.0

    # Dividir os dados em treino e teste
    x_train, x_test, y_train, y_test = train_test_split(datas, labels, test_size=0.25, random_state=42)

    # Codificar as labels
    lb = LabelBinarizer().fit(y_train)
    y_train = lb.transform(y_train)
    y_test = lb.transform(y_test)
    
    # Salvar as labels em arquivo pickle
    with open("labels.dat", "wb") as pickle_file:
        pickle.dump(lb, pickle_file)

    return x_train, x_test, y_train, y_test

def build_model():
    """Função para construir o modelo de rede neural."""
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(127, 127, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(26, activation="softmax"))

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model

def main():
    """Função principal para executar o treinamento do modelo."""
    base_letters_file = "/Users/nicolaslucianobezerra/BreakCapcha/base_letters"
    
    # Carregar e processar as imagens
    try:
        datas, labels = load_and_preprocess_images(base_letters_file)
    except ValueError as e:
        print(e)
        return

    # Preparar os dados (normalização e divisão)
    x_train, x_test, y_train, y_test = prepare_data(datas, labels)
    
    # Construir o modelo
    model = build_model()

    # Treinar o modelo
    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10, batch_size=26, verbose=1)
    
    # Salvar o modelo treinado
    model.save('model.keras')
    print("Modelo treinado e salvo com sucesso!")

if __name__ == "__main__":
    main()