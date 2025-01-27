# BreakCaptcha

Capcha Solver is a Python-based project designed to preprocess, train, and solve CAPTCHA images using computer vision and machine learning techniques. This project demonstrates a complete pipeline from image preprocessing to model training and CAPTCHA resolution.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [License](#license)

---

## Overview

BreakCaptcha is a project built to showcase expertise in Python programming, machine learning, and image processing. The primary goal of the project is to preprocess CAPTCHA images, train a machine learning model, and accurately resolve CAPTCHA challenges.

---

## Features

- Preprocessing of CAPTCHA images to enhance model accuracy.
- Training a convolutional neural network (CNN) to recognize and solve CAPTCHA challenges.
- Modular design with functions for preprocessing, training, and prediction.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/captcha-solver.git
   cd BreakCaptcha
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### 1. Preprocess Images

Run the preprocessing script to convert raw CAPTCHA images into a format suitable for training:
```bash
python preprocess.py
```

### 2. Train the Model

Train the convolutional neural network (CNN) using preprocessed images:
```bash
python train_model.py
```

### 3. Solve CAPTCHA

Use the trained model to resolve CAPTCHA challenges:
```bash
python solve_captcha.py
```

### Note
- Replace the paths in the scripts with your own image dataset.
- The project requires users to upload their own CAPTCHA image datasets. Sensitive information related to cloud storage has been excluded to ensure security.

---

## Project Structure

```plaintext
Capcha Solver/
├── preprocess.py       # Script for preprocessing CAPTCHA images
├── train_model.py      # Script for training the CNN model
├── solve_captcha.py    # Script for solving CAPTCHA challenges
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
└── models/             # Directory to save trained models
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

### Author

BreakCaptcha is solely developed and maintained by Nicolas Luciano Bezerra. This project is a demonstration of technical skills and serves as a portfolio addition. For any inquiries, please reach out via [LinkedIn](https://www.linkedin.com/in/n%C3%ADcolas-luciano-8941281a9).



