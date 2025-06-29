# Qt6 Classification App

A modern PyQt6 desktop application for training and evaluating image classification models on your own datasets.  
You can select a dataset folder, train up to 3 different CNN models, and classify images using the trained models—all in a stylish, user-friendly interface.

---

## Features

- 📁 Select your dataset directory (expects `train` and `test` subfolders)
- 🔢 Choose how many models to train (1–3)
- 🚀 Train models and view their accuracy
- 🖼️ Select an image and preview it
- 🤖 Classify images using any trained model

---

## App Preview

![image](https://github.com/user-attachments/assets/55e4da09-6083-4bf7-9442-54989409abe3)

---

## Dataset Structure

Your dataset directory should look like this:
```
dataset/
  train/
    class1/
      img1.jpg
      img2.jpg
      ...
    class2/
      ...
  test/
    class1/
      ...
    class2/
      ...
```

---

## Getting Started

1. **Install requirements:**
    ```
    pip install -r requirements.txt
    ```

2. **Run the app:**
    ```
    python pyqt6-app/src/main.py
    ```

3. **Select your dataset folder and start training!**

---

## Requirements

- Python 3.8+
- PyQt6
- TensorFlow
- Pillow

---

## Customization

- You can adjust the number and architecture of models in `model.py`.
- The UI style is defined in `main_window.py` using Qt stylesheets.

---
