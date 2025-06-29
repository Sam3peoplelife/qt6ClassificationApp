import os
import sys
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image
import numpy as np


directory = os.environ.get('DATASET_DIR', 'dataset')

#  Directory paths for training and testing datasets
train_dir = directory + '/train'
test_dir = directory + '/test'
number_of_classes = len(list(os.walk(train_dir))[0][1])  # Count number of classes from train directory

# Data loading
train_data = tf.keras.preprocessing.image_dataset_from_directory(
    train_dir,
    image_size=(224, 224),
    batch_size=32,
    label_mode='categorical'
)

test_data = tf.keras.preprocessing.image_dataset_from_directory(
    test_dir,
    image_size=(224, 224),
    batch_size=32,
    label_mode='categorical'
)

# Model definition
model1 = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Rescaling(1./255),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(number_of_classes, activation='softmax')
])
model2 = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Rescaling(1./255),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(number_of_classes, activation='softmax')
])
model3 = models.Sequential([
    layers.Input(shape=(224, 224, 3)),
    layers.Rescaling(1./255),
    layers.Conv2D(32, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(256, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(number_of_classes, activation='softmax')
])

def compliling(model_list):
    for model in model_list:
        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])
    return model_list

def training(model_list, train_data, test_data, epochs=10):
    for model in model_list:
        model.fit(train_data, validation_data=test_data, epochs=epochs)
    return model_list

def evaluation(model_list, test_data):
    results = []
    for model in model_list:
        test_loss, test_accuracy = model.evaluate(test_data)
        results.append((test_loss, test_accuracy))
    return results

def save_models(model_list, save_path):
    for i, model in enumerate(model_list):
        model.save(os.path.join(save_path, f'model_{i+1}.h5'))
    return [os.path.join(save_path, f'model_{i+1}.h5') for i in range(len(model_list))]

def load_models(model_paths):
    loaded_models = []
    for path in model_paths:
        loaded_model = models.load_model(path)
        loaded_models.append(loaded_model)
    return loaded_models

def predict_image(model_path, img_path, class_names):
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    model = models.load_model(model_path)
    preds = model.predict(x)
    print("Predicted probabilities:", preds)
    pred_class = class_names[np.argmax(preds)]
    print(f"Predicted class: {pred_class}")

def main(number_of_models=3):
    model_list = [model1, model2, model3][:number_of_models]
    model_list = compliling(model_list)
    model_list = training(model_list, train_data, test_data)
    results = evaluation(model_list, test_data)
    save_paths = save_models(model_list, 'models')
    return results, save_paths

if __name__ == "__main__":
    # Prediction mode
    if len(sys.argv) > 1 and sys.argv[1] == "--predict":
        img_path = sys.argv[2]
        model_index = int(sys.argv[3])
        model_path = os.path.join('models', f'model_{model_index}.h5')
        train_dir = directory + '/train'
        class_names = sorted(os.listdir(train_dir))
        predict_image(model_path, img_path, class_names)
        sys.exit(0)

    # Training mode
    if len(sys.argv) > 1:
        try:
            n_models = int(sys.argv[1])
            n_models = max(1, min(3, n_models))
        except Exception:
            n_models = 3
    else:
        n_models = 3
    results, save_paths = main(n_models)
    for i, (loss, accuracy) in enumerate(results):
        print(f"Model {i+1}: Accuracy = {accuracy}")