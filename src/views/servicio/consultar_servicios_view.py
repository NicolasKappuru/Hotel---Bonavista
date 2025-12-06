from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem
)
from db import get_conn


class ServiciosConsultarView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Consulta de Servicios")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(["ID Servicio", "Nombre", "Descripción", "Costo"])

        btn_recargar = QPushButton("Recargar")
        btn_recargar.clicked.connect(self.cargar_datos)

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_volver_home)

        botones = QHBoxLayout()
        botones.addWidget(btn_recargar)
        botones.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addWidget(self.tabla)
        layout.addLayout(botones)

        self.setLayout(layout)

        self.cargar_datos()

    def cargar_datos(self):
        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("SELECT servicio_id, nombre_servicio, descripcion, costo_servicio FROM servicio ORDER BY servicio_id")
            datos = cur.fetchall()

            self.tabla.setRowCount(0)
            for fila, (sid, nombre, descripcion, costo) in enumerate(datos):
                self.tabla.insertRow(fila)
                self.tabla.setItem(fila, 0, QTableWidgetItem(str(sid)))
                self.tabla.setItem(fila, 1, QTableWidgetItem(nombre))
                self.tabla.setItem(fila, 2, QTableWidgetItem(descripcion))
                self.tabla.setItem(fila, 3, QTableWidgetItem(str(costo)))

        except Exception as e:
            print("Error cargando servicios:", e)
        finally:
            conn.close()
