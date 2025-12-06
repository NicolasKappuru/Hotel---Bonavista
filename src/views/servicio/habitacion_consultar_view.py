# views/servicio/habitacion_consultar_view.py

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem
)
from PySide6.QtGui import QIntValidator

from db import get_conn


class HabitacionConsultarView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        titulo = QLabel("Consultar Estado de Habitación")
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Campo de búsqueda
        self.num_hab = QLineEdit()
        self.num_hab.setValidator(QIntValidator())
        self.num_hab.setPlaceholderText("Número de habitación")

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar)

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_servicio)

        h_busqueda = QHBoxLayout()
        h_busqueda.addWidget(QLabel("Número Habitación:"))
        h_busqueda.addWidget(self.num_hab)
        h_busqueda.addWidget(btn_buscar)

        # Tabla de resultados
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Número Habitación", "Categoría", "Estado"])
        self.tabla.setRowCount(0)

        h_botones = QHBoxLayout()
        h_botones.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addWidget(titulo)
        layout.addSpacing(15)
        layout.addLayout(h_busqueda)
        layout.addSpacing(10)
        layout.addWidget(self.tabla)
        layout.addLayout(h_botones)
        layout.addStretch()

        self.setLayout(layout)

    # -----------------------------------------
    #               BUSCAR
    # -----------------------------------------
    def buscar(self):
        num = self.num_hab.text().strip()
        if not num:
            QMessageBox.warning(self, "Error", "Ingrese un número de habitación.")
            return

        conn = get_conn()
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT h.numero_habitacion,
                       c.nombre_categoria,
                       e.nombre_estado
                FROM habitacion h
                JOIN categoria c ON h.categoria_id = c.categoria_id
                JOIN estado e ON h.estado_id = e.estado_id
                WHERE h.numero_habitacion = %s
            """, (num,))

            data = cur.fetchone()

            self.tabla.setRowCount(0)

            if not data:
                QMessageBox.information(self, "Sin resultados", "La habitación no existe.")
                return

            self.tabla.setRowCount(1)
            for i, valor in enumerate(data):
                self.tabla.setItem(0, i, QTableWidgetItem(str(valor)))

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()
