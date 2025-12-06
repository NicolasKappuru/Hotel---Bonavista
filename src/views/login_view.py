# views/login_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox
)
from PySide6.QtGui import QIntValidator


class LoginView(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        self.main = main_window

        self.setWindowTitle("Inicio de Sesión")

        self.input_doc = QLineEdit()
        self.input_doc.setValidator(QIntValidator())
        self.input_doc.setPlaceholderText("Número de documento")

        btn_login = QPushButton("Ingresar")
        btn_login.clicked.connect(self.login)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ingrese su número de documento:"))
        layout.addWidget(self.input_doc)
        layout.addWidget(btn_login)
        self.setLayout(layout)


    def login(self):
        doc = self.input_doc.text().strip()
        if not doc:
            QMessageBox.warning(self, "Campo requerido", "Ingrese documento.")
            return

        self.main.login_usuario(doc)
