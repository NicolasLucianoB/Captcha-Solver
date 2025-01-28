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
    """
    Resize an image to the specified width and height.
    Maintains the aspect ratio and handles errors gracefully.
    """
    try:
        resized_image = cv2.resize(image, (width, height))
        return resized_image
    except cv2.error as e:
        print(f"Error resizing the image: {e}")
        return None


def load_and_preprocess_images(base_letters_file):
    """
    Load images from a directory, preprocess them, and extract labels.
    
    Args:
        base_letters_file (str): Path to the directory containing labeled images.
    
    Returns:
        datas (np.ndarray): Array of processed images.
        labels (np.ndarray): Array of corresponding labels.
    """
    datas = []
    labels = []

    images = paths.list_images(base_letters_file)

    for f in images:
        label = f.split(os.path.sep)[-2]  # Extract label from folder name
        
        try:
            # Read the image
            image = cv2.imread(f)
            if image is None:
                print(f"Error reading the image {f}")
                continue
            
            # Convert image to grayscale
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Resize the image to 127x127
            image_resized = resize_image(image, 127, 127)
            if image_resized is None:
                print(f"Error resizing the image {f}")
                continue

            # Add channel dimension (for grayscale images)
            image_resized = np.expand_dims(image_resized, axis=-1)

            datas.append(image_resized)
            labels.append(label)
        
        except Exception as e:
            print(f"Error processing the image {f}: {e}")
    
    datas = np.array(datas)
    labels = np.array(labels)
    
    if len(datas) == 0 or len(labels) == 0:
        raise ValueError("No valid images were loaded for training.")
    
    return datas, labels


def prepare_data(datas, labels):
    """
    Normalize images, split data into training and testing sets, and encode labels.
    
    Args:
        datas (np.ndarray): Array of image data.
        labels (np.ndarray): Array of image labels.
    
    Returns:
        x_train, x_test, y_train, y_test: Training and testing datasets.
    """
    # Normalize the image data
    datas = datas.astype("float32") / 255.0

    # Split data into training and testing sets
    x_train, x_test, y_train, y_test = train_test_split(datas, labels, test_size=0.25, random_state=42)

    # Encode the labels
    lb = LabelBinarizer().fit(y_train)
    y_train = lb.transform(y_train)
    y_test = lb.transform(y_test)
    
    # Save the label encoder to a file
    with open("labels.dat", "wb") as pickle_file:
        pickle.dump(lb, pickle_file)

    return x_train, x_test, y_train, y_test


def build_model():
    """
    Build a Convolutional Neural Network model.
    
    Returns:
        model: Compiled Keras Sequential model.
    """
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation="relu", input_shape=(127, 127, 1)))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dense(64, activation="relu"))
    model.add(Dense(32, activation="relu"))
    model.add(Dense(26, activation="softmax"))  # 26 output classes (e.g., A-Z)

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    return model


def main():
    """
    Main function to execute the training process.
    """
    base_letters_file = "/Users/nicolaslucianobezerra/BreakCapcha/base_letters"
    
    # Load and preprocess images
    try:
        datas, labels = load_and_preprocess_images(base_letters_file)
    except ValueError as e:
        print(e)
        return

    # Prepare data (normalize and split)
    x_train, x_test, y_train, y_test = prepare_data(datas, labels)
    
    # Build the model
    model = build_model()

    # Train the model
    model.fit(x_train, y_train, validation_data=(x_test, y_test), epochs=10, batch_size=26, verbose=1)
    
    # Save the trained model
    model.save('model.keras')
    print("Model trained and saved successfully!")


if __name__ == "__main__":
    main()