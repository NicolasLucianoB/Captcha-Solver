import glob
import os

import cv2

# Get all filtered image files from the specified directory
files = glob.glob("bd_filtered/*")
for f in files:
    # Load the image
    image_f = cv2.imread(f)
    if image_f is None:
        print(f"Error loading image {f}")
        continue

    # Resize the image to a fixed size
    image_resized = cv2.resize(image_f, (550, 220))
    
    # Crop 10 pixels from the top and bottom, and 5 pixels from the sides
    image_cropped = image_resized[10:-10, 5:-5]  # Cropping

    # Convert the cropped image to grayscale
    image = cv2.cvtColor(image_cropped, cv2.COLOR_RGB2GRAY)

    # Apply binary inverse thresholding to highlight regions of interest
    _, new_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(new_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Store bounding box areas for valid contours
    letter_area = []
    for c in contours:
        area = cv2.contourArea(c)
        # Filter contours by area to eliminate noise
        if 50 < area < 2000:
            (x, y, w, h) = cv2.boundingRect(c)
            # Add padding around each contour
            padding = 20
            letter_area.append((x - padding, y - padding, w + 2 * padding, h + 2 * padding))

    # Check if there are enough valid contours
    if len(letter_area) < 5:
        print(f"Image {f} ignored: only {len(letter_area)} valid contours found.")
        continue

    # Create a colored version of the grayscale image to draw bounding boxes
    final_image = cv2.merge([image] * 3)
    for i, (x, y, w, h) in enumerate(letter_area, start=1):
        # Crop the isolated letter with padding
        padded_image_letter = image[max(0, y): min(y + h, image.shape[0]), max(0, x): min(x + w, image.shape[1])]
        
        # Save the cropped letter image to the output directory
        output_filename = f"letter_field/{os.path.basename(f).replace('png', f'letra{i}.png')}"
        cv2.imwrite(output_filename, padded_image_letter)

    # Draw rectangles around detected letters
    for (x, y, w, h) in letter_area:
        cv2.rectangle(final_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Save the final annotated image to the identified folder
    cv2.imwrite(f"identified/{os.path.basename(f)}", final_image)