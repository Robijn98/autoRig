import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QMainWindow,
    QApplication,
    QWidget,
    QPushButton
)

def custom_print(printMessage=''):
    print(printMessage)


app = QApplication(sys.argv)

window = QMainWindow()
window.setCentralWidget(QWidget())
window.setWindowTitle("My App")


main_layout = QVBoxLayout(window.centralWidget())

button = QPushButton("Press Me!")

button.setStyleSheet("""
    QPushButton {
        background-color: #4CAF50;
        color: white;
        border: 2px solid #4CAF50;
        border-radius: 5px;
        padding: 5px 10px;
    }

    QPushButton:hover {
        background-color: #45a049;
    }
""")


button.clicked.connect(lambda: custom_print('goodmorning'))  # Use clicked.connect here


main_layout.addWidget(button)
window.show()

# Start the event loop.
app.exec()




