# views/servicio/servicio_home.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class ServicioHome(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Servicios - Panel Principal")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold;")

        btn_hab_consultar = QPushButton("Consultar Estado de Habitación")
        btn_hab_consultar.clicked.connect(self.main.ir_habitacion_consultar)

        btn_hab_actualizar = QPushButton("Actualizar Estado de Habitación")
        btn_hab_actualizar.clicked.connect(self.main.ir_habitacion_actualizar)

        btn_reservas = QPushButton("Consultar Reservas")
        btn_reservas.clicked.connect(self.main.ir_reservas)

        btn_servicios_consultar = QPushButton("Consultar Servicios")
        btn_servicios_consultar.clicked.connect(self.main.ir_servicios_consultar)

        btn_servicio_asignar = QPushButton("Asignar Servicio a Reserva")
        btn_servicio_asignar.clicked.connect(self.main.ir_servicio_asignar)


        btn_logout = QPushButton("Cerrar sesión")
        btn_logout.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold;")
        btn_logout.clicked.connect(self.main.ir_login)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addSpacing(20)
        layout.addWidget(btn_hab_consultar)
        layout.addWidget(btn_hab_actualizar)
        layout.addWidget(btn_reservas)
        layout.addWidget(btn_servicios_consultar)
        layout.addWidget(btn_servicio_asignar)
        layout.addStretch()
        layout.addWidget(btn_logout)

        self.setLayout(layout)
