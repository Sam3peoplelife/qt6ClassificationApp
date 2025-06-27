# PyQt6 Application

This project is a PyQt6 application that serves as a template for building GUI applications using the PyQt6 framework.

## Project Structure

```
pyqt6-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── ui
│   │   └── main_window.py     # Main window UI definition
│   ├── widgets
│   │   └── custom_widget.py    # Custom widget implementation
│   └── resources
│       └── __init__.py        # Resource package
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pyqt6-app
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. 

## License

This project is licensed under the MIT License.