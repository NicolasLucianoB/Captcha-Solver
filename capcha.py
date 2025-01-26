import glob
import os

import cv2


# preprocessing all the images with grayscale to make a better model
def preprocessing(origin_path, destination_path="bd_filtered"):
  files = glob.glob(f"{origin_path}/*")
  
  for file in files:
    image = cv2.imread(file) 
    gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
  
    _, image_filtered = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV or cv2.THRESH_OTSU)
    # _, image_filtered = cv2.threshold(gray_image, 127, 255, cv2.THRESH_TOZERO or cv2.THRESH_OTSU)
    
    cv2.imwrite(f'{destination_path}/{os.path.basename(file)}', image_filtered)
    
    
if __name__ == "__main__":
  preprocessing("images")