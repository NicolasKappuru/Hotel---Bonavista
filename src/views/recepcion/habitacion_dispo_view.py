# views/recepcion/habitacion_dispo_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
from db import get_conn

class HabitacionDispoView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window

        # Tabla
        self.tabla = QTableWidget()

        btn_back = QPushButton("Volver")
        btn_back.clicked.connect(self.main.ir_inicio_recepcion)
        
        h_top = QHBoxLayout()
        h_top.addStretch()         # para empujar el botón a la derecha o centrar si quieres
        h_top.addWidget(btn_back)

        layout = QVBoxLayout()
        layout.addLayout(h_top)
        layout.addWidget(self.tabla)
        self.setLayout(layout)


    def cargar(self):
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                h.numero_habitacion,
                c.nombre_categoria,
                c.costo_categoria,
                e.nombre_estado
            FROM habitacion h
            JOIN categoria c ON h.categoria_id = c.categoria_id
            JOIN estado e ON h.estado_id = e.estado_id
            WHERE h.estado_id = 1
            ORDER BY h.numero_habitacion;
        """)

        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        conn.close()

        self.tabla.setColumnCount(len(cols))
        self.tabla.setHorizontalHeaderLabels(cols)
        self.tabla.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                self.tabla.setItem(i, j, QTableWidgetItem(str(val)))
