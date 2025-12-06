from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

class AdministracionHome(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Administración - Panel Principal")
        titulo.setStyleSheet("font-size: 26px; font-weight: bold;")


        btn_insert_empleado = QPushButton("Insertar Empleado")
        btn_insert_empleado.clicked.connect(self.main.ir_empleado_insertar)

        btn_update_empleado = QPushButton("Actualizar Empleado")
        btn_update_empleado.clicked.connect(self.main.ir_empleado_actualizar)
         
        btn_consultar_empleado = QPushButton("Consultar Empleado")
        btn_consultar_empleado.clicked.connect(self.main.ir_empleado_consultar)
        
        btn_eliminar_empleado = QPushButton("Eliminar Empleado")
        btn_eliminar_empleado.clicked.connect(self.main.ir_empleado_eliminar)
        
        btn_servicios_consultar = QPushButton("Consultar Servicios")
        btn_servicios_consultar.clicked.connect(self.main.ir_servicios_consultar)

        btn_actualizar_servicios = QPushButton("Actualizar Servicios")
        btn_actualizar_servicios.clicked.connect(self.main.ir_servicios_actualizar)
                 
        btn_hab_reservadas = QPushButton("Habitaciones Más Reservadas")
        btn_hab_reservadas.clicked.connect(self.main.ir_habitaciones_mas_reservadas)
        
        btn_servicios_solicitados = QPushButton("Servicios Más Solicitados")
        btn_servicios_solicitados.clicked.connect(self.main.ir_servicios_mas_solicitados)

        btn_logout = QPushButton("Cerrar sesión")
        btn_logout.setStyleSheet("background-color: #c0392b; color: white; font-weight: bold;")
        btn_logout.clicked.connect(self.main.ir_login)
        
        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addSpacing(20)
        layout.addWidget(btn_insert_empleado)
        layout.addWidget(btn_update_empleado)
        layout.addWidget(btn_consultar_empleado)
        layout.addWidget(btn_eliminar_empleado)
        layout.addWidget(btn_servicios_consultar)
        layout.addWidget(btn_actualizar_servicios)
        layout.addWidget(btn_hab_reservadas)
        layout.addWidget(btn_servicios_solicitados)
        layout.addStretch()
        layout.addWidget(btn_logout)

        self.setLayout(layout)
