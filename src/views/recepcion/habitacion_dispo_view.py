# views/recepcion/habitacion_dispo_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from db import get_conn

class HabitacionDispoView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        self.tabla = QTableWidget()
        btn = QPushButton("Ver habitaciones libres")
        btn.clicked.connect(self.cargar)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(self.tabla)
        self.setLayout(layout)

    def cargar(self):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_habitacion, nombre_estado
            FROM habitacion NATURAL JOIN estado
            WHERE LOWER(nombre_estado) = 'libre'
        """)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        conn.close()

        self.tabla.setColumnCount(len(cols))
        self.tabla.setHorizontalHeaderLabels(cols)
        self.tabla.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.tabla.setItem(i, j, QTableWidgetItem(str(val)))
