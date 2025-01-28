import glob
import os

import cv2


# preprocessing all the images with grayscale to make a better model
def preprocessing(origin_path, destination_path="bd_filtered"):
  files = glob.glob(f"{origin_path}/*")
  
  for file in files:
      try:
          # Read the image
          image = cv2.imread(file)
          if image is None:
              print(f"Skipping invalid file: {file}")
              continue
          
          # Convert the image to grayscale for better processing
          gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
          
          # Apply binary thresholding (using a bitwise OR for combined flags)
          _, image_filtered = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV or cv2.THRESH_OTSU)
          
          # Save the filtered image to the destination directory
          cv2.imwrite(f'{destination_path}/{os.path.basename(file)}', image_filtered)
      except Exception as e:
          print(f"Error processing file {file}: {e}")
    
    
if __name__ == "__main__":
  preprocessing("images")