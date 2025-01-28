import cv2
from PIL import Image

# List of thresholding methods to test
methods = [cv2.THRESH_BINARY,
           cv2.THRESH_BINARY_INV,
           cv2.THRESH_TRUNC,
           cv2.THRESH_TOZERO,
           cv2.THRESH_TOZERO_INV]

# Load the image in grayscale mode
image = cv2.imread('capchas/img1.png', cv2.IMREAD_GRAYSCALE)
# Note: Methods 2 (THRESH_BINARY_INV) and 4 (THRESH_TOZERO_INV) seem to work better.

# Counter for naming the processed images
i = 0

# Apply each thresholding method
for method in methods:
    i += 1
    # Apply the current thresholding method with OTSU as a fallback
    _, processed_image = cv2.threshold(image, 127, 255, method or cv2.THRESH_OTSU)
    
    # Display the processed image
    cv2.imshow('Processed Image', processed_image)
    
    # Save the processed image to a file
    cv2.imwrite(f'teste_metodo/imagem_tratada_{i}.png', processed_image)

# Close all OpenCV windows after processing
cv2.destroyAllWindows()

# Open the second processed image for additional treatment
image = Image.open("teste_metodo/imagem_tratada_2.png")
image = image.convert("L")  # Convert the image to grayscale mode (if not already)
processed_image_2 = Image.new("L", image.size, 255)  # Create a blank white image

# Perform custom pixel-level processing
for x in range(image.size[1]):  # Iterate over the rows
    for y in range(image.size[0]):  # Iterate over the columns
        pixel_value = image.getpixel((y, x))  # Get the pixel value at (x, y)
        if pixel_value < 115:  # If the pixel is darker than the threshold
            processed_image_2.putpixel((y, x), 0)  # Set the pixel to black

# Save the final processed image
processed_image_2.save("teste_metodo/imagem_final.png")