# Capcha Solver

## Overview
Capcha Solver is a Python-based solution designed to train and test models for solving captchas. It leverages TensorFlow for deep learning, OpenCV for image preprocessing, and includes robust functionalities for image handling, dataset preparation, and model training.

## Features
- Downloads and processes captcha images.
- Implements multiple image thresholding techniques for preprocessing.
- Builds a convolutional neural network (CNN) to classify captcha characters.
- Saves trained models and label encodings for future use.

## Prerequisites
Ensure you have the following installed on your system:

- Python 3.10 or higher
- TensorFlow
- OpenCV
- NumPy
- scikit-learn
- boto3
- imutils
- pickle
- dotenv

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/capcha-solver.git
   cd capcha-solver
   ```
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables by creating a `.env` file in the project root:
   ```env
   ACCESS_KEY=<your-access-key>
   SECRET_KEY=<your-secret-key>
   BUCKET_NAME=<your-bucket-name>
   ENDPOINT_URL=<your-endpoint-url>
   ```

## Project Structure
```
capcha-solver/
├── capcha_downloader.py        # Downloads captcha images from an S3-compatible bucket
├── preprocess_images.py        # Applies image preprocessing techniques
├── main.py                     # Builds and trains the CNN model
├── utils.py                    # Contains helper functions
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
└── README.md                   # Project documentation
```

## Usage
### Download Captcha Images
Run the `capcha_downloader.py` script to fetch captcha images from your configured S3-compatible bucket:
```bash
python capcha_downloader.py
```

### Preprocess Images
Use the `preprocess_images.py` script to apply thresholding methods:
```bash
python preprocess_images.py
```

### Train the Model
Execute the `main.py` script to train the model:
```bash
python main.py
```
The trained model will be saved as `model.keras` in the project directory.

## Configuration
Modify the following parameters in the scripts as needed:
- **Image dimensions**: Set in `main.py` for resizing images.
- **Model architecture**: Customizable in the `build_model` function.
- **Data path**: Update paths in `load_and_preprocess_images` for the dataset location.

## Examples
### Thresholding Results
The `preprocess_images.py` script generates thresholded images in the `teste_metodo/` folder. The final processed image is saved as `imagem_final.png`.

### Training Output
Model training outputs metrics like accuracy and loss for each epoch.

## Troubleshooting
- **Image reading errors**: Ensure all images are in the correct format and the dataset path is accurate.
- **S3 connection issues**: Double-check your `.env` configuration and network connectivity.
- **Empty dataset**: Verify the dataset directory contains valid images.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

### Author

BreakCaptcha is solely developed and maintained by Nicolas Luciano Bezerra. This project is a study, a demonstration of technical skills and serves as a portfolio addition. For any inquiries, please reach out via [LinkedIn](https://www.linkedin.com/in/n%C3%ADcolas-luciano-8941281a9).



