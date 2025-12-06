# views/recepcion/recepcion_home.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout

class RecepcionHome(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Recepción - Panel Principal")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold;")

        btn_clientes_insertar = QPushButton("Ingresar Clientes / Huéspedes")
        btn_clientes_insertar.clicked.connect(self.main.ir_cliente_insertar)


        btn_clientes_actualizar = QPushButton("Actualizar Clientes / Huéspedes")
        btn_clientes_actualizar.clicked.connect(self.main.ir_cliente_actualizar)

        btn_reservas = QPushButton("Consultar Reservas")
        btn_reservas.clicked.connect(self.main.ir_reservas)

        btn_habitaciones = QPushButton("Disponibilidad de Habitaciones")
        btn_habitaciones.clicked.connect(self.main.ir_disponibilidad)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addSpacing(20)
        layout.addWidget(btn_clientes_insertar)
        layout.addWidget(btn_clientes_actualizar)
        layout.addWidget(btn_reservas)
        layout.addWidget(btn_habitaciones)
        layout.addStretch()

        self.setLayout(layout)
