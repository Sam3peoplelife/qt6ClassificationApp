from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QSpinBox, QHBoxLayout, QComboBox, QLineEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import subprocess
import sys
import os
import re

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dataset Classifier")
        self.setGeometry(100, 100, 700, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Select a dataset directory to start classification.")
        self.layout.addWidget(self.label)

        self.select_button = QPushButton("Select Dataset Directory")
        self.select_button.clicked.connect(self.select_directory)
        self.layout.addWidget(self.select_button)

        # Add spin box for number of models
        spin_layout = QHBoxLayout()
        self.spin_label = QLabel("Number of models:")
        self.spin_label.setObjectName("spin_label")
        spin_layout.addWidget(self.spin_label)
        self.model_spin = QSpinBox()
        self.model_spin.setObjectName("model_spin")
        self.model_spin.setMinimum(1)
        self.model_spin.setMaximum(3)
        self.model_spin.setValue(3)
        spin_layout.addWidget(self.model_spin)
        self.layout.addLayout(spin_layout)

        self.run_button = QPushButton("🚀 Run Classification")
        self.run_button.clicked.connect(self.run_classification)
        self.run_button.setEnabled(False)
        self.layout.addWidget(self.run_button)

        self.result_label = QLabel("")
        self.result_label.setObjectName("result_label")
        self.layout.addWidget(self.result_label)

        self.image_label = QLabel("No image selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(224, 224)
        self.image_label.setObjectName("image_label")
        self.layout.addWidget(self.image_label)

        self.select_image_button = QPushButton("🖼️ Select Image for Classification")
        self.select_image_button.clicked.connect(self.select_image)
        self.select_image_button.setEnabled(False)
        self.layout.addWidget(self.select_image_button)

        # Style for model choice label and combobox
        self.model_choice_label = QLabel("Choose model for classification:")
        self.model_choice_label.setObjectName("model_choice_label")
        self.layout.addWidget(self.model_choice_label)
        self.model_choice = QComboBox()
        self.model_choice.setObjectName("model_choice")
        self.layout.addWidget(self.model_choice)

        self.classify_button = QPushButton("🤖 Classify Image")
        self.classify_button.clicked.connect(self.classify_image)
        self.classify_button.setEnabled(False)
        self.layout.addWidget(self.classify_button)

        self.classify_result_label = QLabel("")
        self.classify_result_label.setObjectName("classify_result_label")
        self.layout.addWidget(self.classify_result_label)

        self.dataset_dir = None
        self.trained_models = 0
        self.selected_image_path = None

        # For saving model manually
        self.save_model_layout = QHBoxLayout()
        self.save_model_label = QLabel("Save selected model as:")
        self.save_model_label.setObjectName("save_model_label")
        self.save_model_layout.addWidget(self.save_model_label)
        self.save_model_name = QLineEdit()
        self.save_model_name.setPlaceholderText("Enter model name (no extension)")
        self.save_model_name.setObjectName("save_model_name")
        self.save_model_layout.addWidget(self.save_model_name)
        self.save_model_button = QPushButton("💾 Save Model")
        self.save_model_button.clicked.connect(self.save_model)
        self.save_model_button.setEnabled(False)
        self.save_model_layout.addWidget(self.save_model_button)
        self.layout.addLayout(self.save_model_layout)

        # For uploading a model
        self.upload_model_button = QPushButton("⬆️ Upload Model (.h5)")
        self.upload_model_button.clicked.connect(self.upload_model)
        self.layout.addWidget(self.upload_model_button)
        self.uploaded_model_path = None
        self.uploaded_model_name = None

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f6fa;
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 15px;
            }
            QLabel {
                color: #222f3e;
                font-size: 15px;
            }
            #save_model_label {
                color: #20bf6b;
                font-size: 15px;
                font-weight: bold;
                margin-right: 8px;
            }
            #save_model_name {
                min-width: 120px;
                font-size: 15px;
                color: #2f3542;
                background-color: #fff;
                border: 1.5px solid #20bf6b;
                border-radius: 6px;
                padding: 4px 8px;
            }
            #spin_label {
                color: #576574;
                font-size: 15px;
                font-weight: bold;
                margin-right: 8px;
            }
            #model_spin {
                min-width: 60px;
                font-size: 15px;
                color: #2f3542;
                background-color: #fff;
                border: 1.5px solid #54a0ff;
                border-radius: 6px;
                padding: 4px 8px;
            }
            QPushButton {
                background-color: #54a0ff;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover:!disabled {
                background-color: #2e86de;
            }
            QPushButton:disabled {
                background-color: #c8d6e5;
                color: #8395a7;
            }
            #model_choice_label {
                color: #0097e6;
                font-size: 15px;
                font-weight: bold;
                margin-top: 10px;
                margin-bottom: 4px;
            }
            #model_choice {
                background-color: #fff;
                color: #2f3542;
                border: 1.5px solid #54a0ff;
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 15px;
                min-width: 120px;
            }
            #result_label {
                color: #20bf6b;
                font-size: 16px;
                font-weight: bold;
                margin: 8px 0;
            }
            #classify_result_label {
                color: #e17055;
                font-size: 16px;
                font-weight: bold;
                margin: 8px 0;
            }
            #image_label {
                border: 2px dashed #8395a7;
                background: #fff;
                min-height: 224px;
                min-width: 224px;
            }
            QComboBox QAbstractItemView {
                background: #fff;
                color: #2f3542;
                selection-background-color: #d6eaff;
                selection-color: #222f3e;
                border-radius: 6px;
                font-size: 15px;
            }
            QComboBox, QSpinBox {
                background-color: #fff;
                border: 1px solid #c8d6e5;
                border-radius: 6px;
                padding: 4px 8px;
            }
            QComboBox:focus, QSpinBox:focus {
                border: 1.5px solid #54a0ff;
            }
            QScrollBar:vertical {
                width: 12px;
                background: #f5f6fa;
            }
            QScrollBar::handle:vertical {
                background: #c8d6e5;
                border-radius: 6px;
            }
        """)

    def select_directory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Dataset Directory")
        if dir_path:
            self.dataset_dir = dir_path
            # Show only the last folder name, not the full path
            folder_name = os.path.basename(dir_path.rstrip("/\\"))
            self.label.setText(f"Selected folder: <b>{folder_name}</b>")
            self.run_button.setEnabled(True)

    def run_classification(self):
        if not self.dataset_dir:
            QMessageBox.warning(self, "Error", "Please select a dataset directory first.")
            return

        env = os.environ.copy()
        env["DATASET_DIR"] = self.dataset_dir

        num_models = self.model_spin.value()

        try:
            result = subprocess.run(
                [sys.executable, os.path.abspath("../../model.py"), str(num_models)],
                cwd=os.path.dirname(os.path.abspath("../../model.py")),
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            # Extract only accuracy percentages from stdout
            accuracies = re.findall(r'Accuracy = ([0-9.]+)', result.stdout)
            if accuracies:
                acc_text = "<br>".join([f"Model {i+1}: <b>{float(acc)*100:.2f}%</b>" for i, acc in enumerate(accuracies)])
                self.result_label.setText(acc_text)
                self.trained_models = len(accuracies)
                self.model_choice.clear()
                for i in range(self.trained_models):
                    self.model_choice.addItem(f"Model {i+1}")
                self.select_image_button.setEnabled(True)
                self.classify_button.setEnabled(False)
                self.save_model_button.setEnabled(True)
            else:
                self.result_label.setText("No accuracy results found.")
                self.select_image_button.setEnabled(False)
                self.save_model_button.setEnabled(False)
        except subprocess.CalledProcessError as e:
            self.result_label.setText("Classification failed.")
            self.save_model_button.setEnabled(False)

    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.selected_image_path = file_path
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(224, 224, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            self.classify_button.setEnabled(True)
        else:
            self.selected_image_path = None
            self.image_label.setText("No image selected")
            self.classify_button.setEnabled(False)

    def classify_image(self):
        if not self.selected_image_path:
            QMessageBox.warning(self, "Error", "Please select an image first.")
            return
        # If uploaded model is used, predict with it
        if self.uploaded_model_path:
            try:
                result = subprocess.run(
                    [sys.executable, os.path.abspath("../../model.py"), "--predict", self.selected_image_path, "1", self.uploaded_model_path],
                    cwd=os.path.dirname(os.path.abspath("../../model.py")),
                    capture_output=True,
                    text=True,
                    check=True
                )
                match = re.search(r'Predicted class: (.+)', result.stdout)
                if match:
                    self.classify_result_label.setText(f"Prediction (uploaded): <b>{match.group(1)}</b>")
                else:
                    self.classify_result_label.setText("Prediction failed or not found.")
            except subprocess.CalledProcessError as e:
                self.classify_result_label.setText("Prediction failed.")
        else:
            model_index = self.model_choice.currentIndex() + 1
            # Call model.py with --predict argument, passing image path and model index
            try:
                result = subprocess.run(
                    [sys.executable, os.path.abspath("../../model.py"), "--predict", self.selected_image_path, str(model_index)],
                    cwd=os.path.dirname(os.path.abspath("../../model.py")),
                    capture_output=True,
                    text=True,
                    check=True
                )
                match = re.search(r'Predicted class: (.+)', result.stdout)
                if match:
                    self.classify_result_label.setText(f"Prediction: <b>{match.group(1)}</b>")
                else:
                    self.classify_result_label.setText("Prediction failed or not found.")
            except subprocess.CalledProcessError as e:
                self.classify_result_label.setText("Prediction failed.")

    def save_model(self):
        name = self.save_model_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a model name.")
            return
        model_index = self.model_choice.currentIndex() + 1
        src_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath("../../model.py")), "models", f"model_{model_index}.h5"))
        save_dir = QFileDialog.getExistingDirectory(self, "Select directory to save model")
        if not save_dir:
            return
        dst_path = os.path.join(save_dir, name + ".h5")
        try:
            import shutil
            shutil.copyfile(src_path, dst_path)
            QMessageBox.information(self, "Success", f"Model saved as {dst_path}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save model: {e}")

    def upload_model(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Model File", "", "Keras Model (*.h5)")
        if file_path:
            self.uploaded_model_path = file_path
            self.uploaded_model_name = os.path.basename(file_path)
            self.classify_result_label.setText(f"Uploaded model: <b>{self.uploaded_model_name}</b>")
            self.classify_button.setEnabled(True)
            # Optionally, add to model_choice dropdown as a special entry
            if self.model_choice.findText("Uploaded Model") == -1:
                self.model_choice.addItem("Uploaded Model")
                self.model_choice.setCurrentText("Uploaded Model")
        else:
            self.uploaded_model_path = None
            self.uploaded_model_name = None